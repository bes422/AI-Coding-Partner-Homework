"""Unit tests for the Transaction Validator Agent."""
import sys
import os

# Ensure homework-6/ is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from agents.transaction_validator import (
    ISO_4217_WHITELIST,
    mask_account,
    process_message,
    validate_transaction,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_txn(**overrides) -> dict:
    """Return a minimal valid transaction dict with optional overrides."""
    base = {
        "transaction_id": "TXN-TEST",
        "amount": "1000.00",
        "currency": "USD",
        "source_account": "ACC-1001",
        "destination_account": "ACC-2001",
        "timestamp": "2026-03-16T10:00:00Z",
        "metadata": {"channel": "online", "country": "US"},
    }
    base.update(overrides)
    return base


def make_message(txn: dict = None) -> dict:
    """Wrap a transaction in a pipeline message."""
    if txn is None:
        txn = make_txn()
    return {
        "message_id": "test-msg-001",
        "timestamp": "2026-03-16T10:00:00Z",
        "source_agent": "integrator",
        "target_agent": "transaction_validator",
        "message_type": "transaction",
        "data": txn,
    }


# ---------------------------------------------------------------------------
# validate_transaction tests
# ---------------------------------------------------------------------------

class TestValidateTransaction:
    def test_valid_usd_transaction(self):
        txn = make_txn()
        is_valid, reason = validate_transaction(txn)
        assert is_valid is True
        assert reason == ""

    def test_valid_eur_transaction(self):
        txn = make_txn(currency="EUR", amount="500.00")
        is_valid, reason = validate_transaction(txn)
        assert is_valid is True

    def test_valid_gbp_transaction(self):
        txn = make_txn(currency="GBP", amount="750.00")
        is_valid, reason = validate_transaction(txn)
        assert is_valid is True

    def test_invalid_currency_xyz(self):
        txn = make_txn(currency="XYZ")
        is_valid, reason = validate_transaction(txn)
        assert is_valid is False
        assert reason == "INVALID_CURRENCY"

    def test_invalid_currency_empty(self):
        txn = make_txn(currency="")
        is_valid, reason = validate_transaction(txn)
        assert is_valid is False
        # Empty string treated as missing field
        assert reason == "MISSING_FIELD:currency"

    def test_negative_amount(self):
        txn = make_txn(amount="-100.00")
        is_valid, reason = validate_transaction(txn)
        assert is_valid is False
        assert reason == "INVALID_AMOUNT"

    def test_zero_amount(self):
        txn = make_txn(amount="0.00")
        is_valid, reason = validate_transaction(txn)
        assert is_valid is False
        assert reason == "INVALID_AMOUNT"

    def test_missing_transaction_id(self):
        txn = make_txn()
        del txn["transaction_id"]
        is_valid, reason = validate_transaction(txn)
        assert is_valid is False
        assert "MISSING_FIELD:transaction_id" == reason

    def test_missing_amount(self):
        txn = make_txn()
        del txn["amount"]
        is_valid, reason = validate_transaction(txn)
        assert is_valid is False
        assert "MISSING_FIELD:amount" == reason

    def test_missing_currency(self):
        txn = make_txn()
        del txn["currency"]
        is_valid, reason = validate_transaction(txn)
        assert is_valid is False
        assert "MISSING_FIELD:currency" == reason

    def test_missing_source_account(self):
        txn = make_txn()
        del txn["source_account"]
        is_valid, reason = validate_transaction(txn)
        assert is_valid is False
        assert "MISSING_FIELD:source_account" == reason

    def test_missing_destination_account(self):
        txn = make_txn()
        del txn["destination_account"]
        is_valid, reason = validate_transaction(txn)
        assert is_valid is False
        assert "MISSING_FIELD:destination_account" == reason

    def test_non_numeric_amount(self):
        txn = make_txn(amount="abc")
        is_valid, reason = validate_transaction(txn)
        assert is_valid is False
        assert reason == "INVALID_AMOUNT"

    def test_all_whitelisted_currencies(self):
        for currency in ISO_4217_WHITELIST:
            txn = make_txn(currency=currency)
            is_valid, _ = validate_transaction(txn)
            assert is_valid is True, f"Expected {currency} to be valid"


# ---------------------------------------------------------------------------
# process_message tests
# ---------------------------------------------------------------------------

class TestProcessMessage:
    def test_valid_transaction_returns_validated_status(self):
        msg = make_message()
        result = process_message(msg)
        assert result["data"]["status"] == "validated"

    def test_valid_transaction_sets_target_agent(self):
        msg = make_message()
        result = process_message(msg)
        assert result["target_agent"] == "fraud_detector"

    def test_invalid_transaction_returns_rejected_status(self):
        msg = make_message(make_txn(currency="XYZ"))
        result = process_message(msg)
        assert result["data"]["status"] == "rejected"

    def test_invalid_transaction_sets_settlement_target(self):
        msg = make_message(make_txn(currency="XYZ"))
        result = process_message(msg)
        assert result["target_agent"] == "settlement_processor"

    def test_invalid_transaction_includes_reason(self):
        msg = make_message(make_txn(currency="XYZ"))
        result = process_message(msg)
        assert result["data"]["reason"] == "INVALID_CURRENCY"

    def test_message_preserves_message_id(self):
        msg = make_message()
        result = process_message(msg)
        assert result["message_id"] == "test-msg-001"

    def test_source_agent_updated(self):
        msg = make_message()
        result = process_message(msg)
        assert result["source_agent"] == "transaction_validator"

    def test_timestamp_updated(self):
        msg = make_message()
        result = process_message(msg)
        assert result["timestamp"] != "2026-03-16T10:00:00Z"  # updated to now


# ---------------------------------------------------------------------------
# mask_account tests
# ---------------------------------------------------------------------------

class TestMaskAccount:
    def test_masks_account_number(self):
        assert mask_account("ACC-1001") == "****1001"

    def test_short_account_fully_masked(self):
        assert mask_account("AB") == "****"

    def test_empty_account(self):
        assert mask_account("") == "****"

    def test_exactly_four_chars(self):
        assert mask_account("1234") == "****"


# ---------------------------------------------------------------------------
# main() CLI tests
# ---------------------------------------------------------------------------

class TestMain:
    def test_main_prints_report(self, capsys, monkeypatch, tmp_path):
        """main() should print a validation report to stdout."""
        import json
        txns_file = tmp_path / "txns.json"
        txns_file.write_text(json.dumps([
            {"transaction_id": "X001", "amount": "100.00", "currency": "USD",
             "source_account": "ACC-A", "destination_account": "ACC-B"},
            {"transaction_id": "X002", "amount": "50.00", "currency": "XYZ",
             "source_account": "ACC-C", "destination_account": "ACC-D"},
        ]))
        monkeypatch.setattr("sys.argv", ["validator", "--input", str(txns_file)])
        from agents.transaction_validator import main
        main()
        out = capsys.readouterr().out
        assert "X001" in out
        assert "X002" in out
        assert "INVALID_CURRENCY" in out
        assert "Total" in out

    def test_main_dry_run_flag(self, capsys, monkeypatch, tmp_path):
        """--dry-run flag shows DRY RUN in header."""
        import json
        txns_file = tmp_path / "txns.json"
        txns_file.write_text(json.dumps([
            {"transaction_id": "T001", "amount": "200.00", "currency": "EUR",
             "source_account": "ACC-1", "destination_account": "ACC-2"},
        ]))
        monkeypatch.setattr("sys.argv", ["validator", "--dry-run", "--input", str(txns_file)])
        from agents.transaction_validator import main
        main()
        out = capsys.readouterr().out
        assert "DRY RUN" in out

    def test_main_missing_file_exits(self, monkeypatch):
        """main() should exit with code 1 if input file doesn't exist."""
        monkeypatch.setattr("sys.argv", ["validator", "--input", "nonexistent_file.json"])
        import pytest
        from agents.transaction_validator import main
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
