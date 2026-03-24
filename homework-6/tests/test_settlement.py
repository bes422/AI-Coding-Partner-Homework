"""Unit tests for the Settlement Processor Agent."""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from decimal import Decimal
from agents.settlement_processor import process_message, settle_transaction


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_data(status="validated", fraud_level="LOW", fraud_score=0, **overrides) -> dict:
    """Return a fraud-scored transaction data dict ready for settlement."""
    base = {
        "transaction_id": "TXN-TEST",
        "amount": "1000.00",
        "currency": "USD",
        "source_account": "ACC-1001",
        "destination_account": "ACC-2001",
        "status": status,
        "fraud_risk_level": fraud_level,
        "fraud_risk_score": fraud_score,
    }
    if status == "rejected":
        base["reason"] = overrides.pop("reason", "INVALID_CURRENCY")
        base.pop("fraud_risk_level", None)
        base.pop("fraud_risk_score", None)
    base.update(overrides)
    return base


def make_message(data: dict = None) -> dict:
    """Wrap data in a pipeline message."""
    if data is None:
        data = make_data()
    return {
        "message_id": "test-msg-003",
        "timestamp": "2026-03-16T10:00:00Z",
        "source_agent": "fraud_detector",
        "target_agent": "settlement_processor",
        "message_type": "transaction",
        "data": data,
    }


# ---------------------------------------------------------------------------
# settle_transaction tests
# ---------------------------------------------------------------------------

class TestSettleTransaction:
    def test_low_risk_settles(self):
        data = make_data(fraud_level="LOW", amount="1000.00")
        result = settle_transaction(data)
        assert result["final_status"] == "settled"

    def test_medium_risk_settles(self):
        data = make_data(fraud_level="MEDIUM", fraud_score=3, amount="25000.00")
        result = settle_transaction(data)
        assert result["final_status"] == "settled"

    def test_high_risk_blocked(self):
        data = make_data(fraud_level="HIGH", fraud_score=7, amount="75000.00")
        result = settle_transaction(data)
        assert result["final_status"] == "blocked"

    def test_blocked_contains_reason(self):
        data = make_data(fraud_level="HIGH", fraud_score=7)
        result = settle_transaction(data)
        assert "final_reason" in result
        assert "HIGH_FRAUD_RISK" in result["final_reason"]

    def test_rejected_transaction_passes_through(self):
        data = make_data(status="rejected", reason="INVALID_CURRENCY")
        result = settle_transaction(data)
        assert result["final_status"] == "rejected"
        assert result["final_reason"] == "INVALID_CURRENCY"

    def test_settlement_fee_calculation_0_1_percent(self):
        """Fee should be exactly 0.1% of amount using Decimal arithmetic."""
        data = make_data(fraud_level="LOW", amount="1000.00")
        result = settle_transaction(data)
        assert result["settlement_fee"] == "1.00"   # 1000 * 0.001 = 1.00
        assert result["net_amount"] == "999.00"

    def test_settlement_fee_large_amount(self):
        """$25,000 * 0.1% = $25.00 fee."""
        data = make_data(fraud_level="MEDIUM", fraud_score=3, amount="25000.00")
        result = settle_transaction(data)
        assert result["settlement_fee"] == "25.00"
        assert result["net_amount"] == "24975.00"

    def test_settlement_fee_uses_decimal(self):
        """Net amount should be a string representation of Decimal, not float."""
        data = make_data(fraud_level="LOW", amount="1500.00")
        result = settle_transaction(data)
        # Verify it's Decimal-safe by parsing back
        fee = Decimal(result["settlement_fee"])
        net = Decimal(result["net_amount"])
        amount = Decimal("1500.00")
        assert fee + net == amount

    def test_settlement_fee_rounding(self):
        """$9,999.99 * 0.001 = 9.99999 → rounds to 10.00 (ROUND_HALF_UP)."""
        data = make_data(fraud_level="LOW", amount="9999.99")
        result = settle_transaction(data)
        fee = Decimal(result["settlement_fee"])
        # 9999.99 * 0.001 = 9.99999 → rounds to 10.00
        assert fee == Decimal("10.00")

    def test_settled_result_contains_net_amount(self):
        data = make_data(fraud_level="LOW", amount="3200.00")
        result = settle_transaction(data)
        assert "net_amount" in result
        assert "settlement_fee" in result


# ---------------------------------------------------------------------------
# process_message tests
# ---------------------------------------------------------------------------

class TestProcessMessage:
    def test_writes_result_file(self, tmp_path):
        msg = make_message()
        process_message(msg, results_dir=str(tmp_path))
        result_file = tmp_path / "TXN-TEST.json"
        assert result_file.exists()

    def test_result_file_contains_valid_json(self, tmp_path):
        msg = make_message()
        process_message(msg, results_dir=str(tmp_path))
        with open(tmp_path / "TXN-TEST.json") as f:
            data = json.load(f)
        assert "data" in data
        assert data["data"]["final_status"] == "settled"

    def test_blocked_transaction_writes_result(self, tmp_path):
        data = make_data(
            transaction_id="TXN-HIGH",
            fraud_level="HIGH",
            fraud_score=7,
            amount="75000.00",
        )
        msg = make_message(data)
        process_message(msg, results_dir=str(tmp_path))
        result_file = tmp_path / "TXN-HIGH.json"
        assert result_file.exists()
        with open(result_file) as f:
            result = json.load(f)
        assert result["data"]["final_status"] == "blocked"

    def test_rejected_transaction_writes_result(self, tmp_path):
        data = make_data(status="rejected", reason="INVALID_CURRENCY")
        msg = make_message(data)
        process_message(msg, results_dir=str(tmp_path))
        result_file = tmp_path / "TXN-TEST.json"
        assert result_file.exists()

    def test_source_agent_updated(self, tmp_path):
        msg = make_message()
        result = process_message(msg, results_dir=str(tmp_path))
        assert result["source_agent"] == "settlement_processor"

    def test_target_agent_set_to_results(self, tmp_path):
        msg = make_message()
        result = process_message(msg, results_dir=str(tmp_path))
        assert result["target_agent"] == "results"

    def test_creates_results_dir_if_missing(self, tmp_path):
        nested_dir = str(tmp_path / "nested" / "results")
        msg = make_message()
        process_message(msg, results_dir=nested_dir)
        assert os.path.exists(nested_dir)
