"""Unit tests for the Fraud Detector Agent.

Scoring rules (cumulative):
  amount > $10,000  → +3 pts
  amount > $50,000  → +4 pts (in addition to the +3 above; total +7 for >$50k)
  unusual hour 02:00-05:00 UTC → +2 pts
  cross-border (country != US)  → +1 pt

Risk levels:
  LOW    0-2
  MEDIUM 3-6
  HIGH   7-10
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from agents.fraud_detector import process_message, score_transaction


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_data(**overrides) -> dict:
    """Return a minimal validated transaction data dict."""
    base = {
        "transaction_id": "TXN-TEST",
        "amount": "1000.00",
        "currency": "USD",
        "source_account": "ACC-1001",
        "destination_account": "ACC-2001",
        "status": "validated",
        "timestamp": "2026-03-16T10:00:00Z",
        "metadata": {"channel": "online", "country": "US"},
    }
    base.update(overrides)
    return base


def make_message(data: dict = None) -> dict:
    """Wrap data in a pipeline message."""
    if data is None:
        data = make_data()
    return {
        "message_id": "test-msg-002",
        "timestamp": "2026-03-16T10:00:00Z",
        "source_agent": "transaction_validator",
        "target_agent": "fraud_detector",
        "message_type": "transaction",
        "data": data,
    }


# ---------------------------------------------------------------------------
# score_transaction tests
# ---------------------------------------------------------------------------

class TestScoreTransaction:
    def test_low_risk_small_amount(self):
        """$1,500 USD, US, daytime → 0 pts = LOW."""
        data = make_data(amount="1500.00")
        score, level = score_transaction(data)
        assert score == 0
        assert level == "LOW"

    def test_medium_risk_high_value_25k(self):
        """$25,000 USD, US, daytime → +3 pts (>$10k) = MEDIUM."""
        data = make_data(amount="25000.00")
        score, level = score_transaction(data)
        assert score == 3
        assert level == "MEDIUM"

    def test_high_risk_very_high_value_75k(self):
        """$75,000 USD → +3 (>$10k) + +4 (>$50k) = 7 pts = HIGH."""
        data = make_data(amount="75000.00")
        score, level = score_transaction(data)
        assert score == 7
        assert level == "HIGH"

    def test_unusual_hour_adds_2_pts(self):
        """Transaction at 02:47 UTC adds 2 pts."""
        data = make_data(timestamp="2026-03-16T02:47:00Z")
        score, level = score_transaction(data)
        assert score == 2
        assert level == "LOW"  # 2 pts = LOW (0-2 boundary)

    def test_unusual_hour_boundary_02_included(self):
        """Hour 02:00 IS in the unusual window [02, 05)."""
        data = make_data(timestamp="2026-03-16T02:00:00Z")
        score, level = score_transaction(data)
        assert score == 2

    def test_unusual_hour_boundary_05_excluded(self):
        """Hour 05:00 is NOT in the unusual window."""
        data = make_data(timestamp="2026-03-16T05:00:00Z")
        score, level = score_transaction(data)
        assert score == 0

    def test_normal_hour_no_pts(self):
        """Hour 10:00 is normal."""
        data = make_data(timestamp="2026-03-16T10:00:00Z")
        score, level = score_transaction(data)
        assert score == 0

    def test_cross_border_adds_1_pt(self):
        """Non-US country (DE) adds 1 pt."""
        data = make_data(metadata={"channel": "api", "country": "DE"})
        score, level = score_transaction(data)
        assert score == 1
        assert level == "LOW"

    def test_us_country_no_cross_border_pts(self):
        """US country = no cross-border bonus."""
        data = make_data(metadata={"channel": "online", "country": "US"})
        score, level = score_transaction(data)
        assert score == 0

    def test_txn004_medium_eur_cross_border_unusual_hour(self):
        """TXN004: EUR 500 at 02:47 from DE → cross-border(1) + unusual_hour(2) = 3 = MEDIUM."""
        data = make_data(
            amount="500.00",
            currency="EUR",
            timestamp="2026-03-16T02:47:00Z",
            metadata={"channel": "api", "country": "DE"},
        )
        score, level = score_transaction(data)
        assert score == 3
        assert level == "MEDIUM"

    def test_amount_exactly_10000_not_flagged(self):
        """$10,000 does NOT trigger high-value flag (must be strictly > $10,000)."""
        data = make_data(amount="10000.00")
        score, level = score_transaction(data)
        assert score == 0

    def test_amount_10001_triggers_3_pts(self):
        data = make_data(amount="10001.00")
        score, level = score_transaction(data)
        assert score == 3

    def test_amount_exactly_50000_triggers_3_pts_only(self):
        """$50,000 triggers >10k rule (+3) but NOT the >50k rule (strictly > 50k)."""
        data = make_data(amount="50000.00")
        score, level = score_transaction(data)
        assert score == 3

    def test_amount_50001_triggers_7_pts(self):
        """$50,001 triggers both >10k (+3) AND >50k (+4) = 7 pts = HIGH."""
        data = make_data(amount="50001.00")
        score, level = score_transaction(data)
        assert score == 7
        assert level == "HIGH"

    def test_invalid_timestamp_no_crash(self):
        data = make_data(timestamp="not-a-date")
        score, level = score_transaction(data)
        assert isinstance(score, int)
        assert level in ("LOW", "MEDIUM", "HIGH")

    def test_invalid_amount_falls_back_to_zero(self):
        """Non-numeric amount should not crash — treated as 0 (no high-value score)."""
        data = make_data(amount="bad-amount")
        score, level = score_transaction(data)
        assert score == 0
        assert level == "LOW"

    def test_missing_metadata_no_crash(self):
        """Missing metadata should not add cross-border pts (defaults to US)."""
        data = make_data()
        data.pop("metadata", None)
        score, level = score_transaction(data)
        assert score == 0  # no cross-border bonus

    def test_txn005_equivalent_high_risk(self):
        """TXN005 equivalent: $75k USD, US, 10:00 → 7 pts = HIGH."""
        data = make_data(
            transaction_id="TXN005",
            amount="75000.00",
            timestamp="2026-03-16T10:00:00Z",
            metadata={"channel": "branch", "country": "US"},
        )
        score, level = score_transaction(data)
        assert score == 7
        assert level == "HIGH"


# ---------------------------------------------------------------------------
# process_message tests
# ---------------------------------------------------------------------------

class TestProcessMessage:
    def test_validated_message_gets_scored(self):
        msg = make_message()
        result = process_message(msg)
        assert "fraud_risk_score" in result["data"]
        assert "fraud_risk_level" in result["data"]

    def test_rejected_message_passes_through_unchanged(self):
        data = make_data(status="rejected", reason="INVALID_CURRENCY")
        # make_data for fraud detector doesn't include fraud fields by default
        msg = make_message(data)
        result = process_message(msg)
        assert "fraud_risk_score" not in result["data"]
        assert "fraud_risk_level" not in result["data"]
        assert result["data"]["status"] == "rejected"

    def test_target_agent_set_to_settlement(self):
        msg = make_message()
        result = process_message(msg)
        assert result["target_agent"] == "settlement_processor"

    def test_source_agent_updated(self):
        msg = make_message()
        result = process_message(msg)
        assert result["source_agent"] == "fraud_detector"

    def test_high_value_75k_flagged_high(self):
        """$75,000 → score 7 = HIGH."""
        data = make_data(transaction_id="TXN005", amount="75000.00")
        msg = make_message(data)
        result = process_message(msg)
        assert result["data"]["fraud_risk_score"] == 7
        assert result["data"]["fraud_risk_level"] == "HIGH"

    def test_low_value_1500_flagged_low(self):
        """TXN001: $1,500 USD US daytime → score 0 = LOW."""
        data = make_data(transaction_id="TXN001", amount="1500.00")
        msg = make_message(data)
        result = process_message(msg)
        assert result["data"]["fraud_risk_score"] == 0
        assert result["data"]["fraud_risk_level"] == "LOW"

    def test_message_id_preserved(self):
        msg = make_message()
        result = process_message(msg)
        assert result["message_id"] == "test-msg-002"

    def test_timestamp_updated(self):
        msg = make_message()
        result = process_message(msg)
        assert result["timestamp"] != "2026-03-16T10:00:00Z"
