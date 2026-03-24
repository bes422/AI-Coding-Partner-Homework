"""Integration tests for the full banking pipeline."""
import sys
import os
import json
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from pathlib import Path
from integrator import run_pipeline

SAMPLE_TRANSACTIONS_FILE = Path(__file__).parent.parent / "sample-transactions.json"


# ---------------------------------------------------------------------------
# Full pipeline integration tests
# ---------------------------------------------------------------------------

class TestFullPipeline:
    def test_all_8_transactions_produce_result_files(self, tmp_path):
        """All 8 sample transactions must produce a result file in results/."""
        results_dir = tmp_path / "results"
        run_pipeline(
            transactions_file=SAMPLE_TRANSACTIONS_FILE,
            results_dir=str(results_dir),
        )
        result_files = list(results_dir.glob("*.json"))
        assert len(result_files) == 8, (
            f"Expected 8 result files, got {len(result_files)}: "
            f"{[f.name for f in result_files]}"
        )

    def test_all_transaction_ids_in_results(self, tmp_path):
        """Each expected transaction ID has a corresponding result file."""
        results_dir = tmp_path / "results"
        run_pipeline(
            transactions_file=SAMPLE_TRANSACTIONS_FILE,
            results_dir=str(results_dir),
        )
        expected_ids = {
            "TXN001", "TXN002", "TXN003", "TXN004",
            "TXN005", "TXN006", "TXN007", "TXN008",
        }
        result_ids = {f.stem for f in results_dir.glob("*.json")}
        assert expected_ids == result_ids

    def test_invalid_currency_txn006_rejected(self, tmp_path):
        """TXN006 has currency XYZ → must be rejected."""
        results_dir = tmp_path / "results"
        run_pipeline(
            transactions_file=SAMPLE_TRANSACTIONS_FILE,
            results_dir=str(results_dir),
        )
        with open(results_dir / "TXN006.json") as f:
            result = json.load(f)
        assert result["data"]["final_status"] == "rejected"
        assert result["data"]["reason"] == "INVALID_CURRENCY"

    def test_negative_amount_txn007_rejected(self, tmp_path):
        """TXN007 has amount -100.00 → must be rejected."""
        results_dir = tmp_path / "results"
        run_pipeline(
            transactions_file=SAMPLE_TRANSACTIONS_FILE,
            results_dir=str(results_dir),
        )
        with open(results_dir / "TXN007.json") as f:
            result = json.load(f)
        assert result["data"]["final_status"] == "rejected"
        assert result["data"]["reason"] == "INVALID_AMOUNT"

    def test_high_value_txn005_blocked(self, tmp_path):
        """TXN005 is $75,000 USD → fraud score >= 7 → blocked."""
        results_dir = tmp_path / "results"
        run_pipeline(
            transactions_file=SAMPLE_TRANSACTIONS_FILE,
            results_dir=str(results_dir),
        )
        with open(results_dir / "TXN005.json") as f:
            result = json.load(f)
        # $75,000 > $50,000 (+4 pts) = HIGH risk → blocked
        assert result["data"]["fraud_risk_level"] == "HIGH"
        assert result["data"]["final_status"] == "blocked"

    def test_normal_txn001_settled(self, tmp_path):
        """TXN001 is $1,500 USD daytime US → LOW risk → settled."""
        results_dir = tmp_path / "results"
        run_pipeline(
            transactions_file=SAMPLE_TRANSACTIONS_FILE,
            results_dir=str(results_dir),
        )
        with open(results_dir / "TXN001.json") as f:
            result = json.load(f)
        assert result["data"]["fraud_risk_level"] == "LOW"
        assert result["data"]["final_status"] == "settled"
        assert "net_amount" in result["data"]
        assert "settlement_fee" in result["data"]

    def test_pipeline_returns_correct_counters(self, tmp_path):
        """run_pipeline should return correct counts: 5 settled, 2 rejected, 1 blocked."""
        results_dir = tmp_path / "results"
        counters = run_pipeline(
            transactions_file=SAMPLE_TRANSACTIONS_FILE,
            results_dir=str(results_dir),
        )
        assert counters["total"] == 8
        assert counters["rejected"] == 2   # TXN006 (XYZ) + TXN007 (-100)
        assert counters["blocked"] == 1    # TXN005 ($75,000)
        assert counters["settled"] == 5    # TXN001, TXN002, TXN003, TXN004, TXN008

    def test_result_files_contain_valid_json_structure(self, tmp_path):
        """Each result file must have the standard message fields."""
        results_dir = tmp_path / "results"
        run_pipeline(
            transactions_file=SAMPLE_TRANSACTIONS_FILE,
            results_dir=str(results_dir),
        )
        required_fields = {"message_id", "timestamp", "source_agent", "target_agent", "data"}
        for result_file in results_dir.glob("*.json"):
            with open(result_file) as f:
                result = json.load(f)
            assert required_fields.issubset(result.keys()), (
                f"{result_file.name} missing fields: {required_fields - result.keys()}"
            )

    def test_txn002_medium_risk_settled(self, tmp_path):
        """TXN002 is $25,000 USD → MEDIUM risk (score 3) → settled."""
        results_dir = tmp_path / "results"
        run_pipeline(
            transactions_file=SAMPLE_TRANSACTIONS_FILE,
            results_dir=str(results_dir),
        )
        with open(results_dir / "TXN002.json") as f:
            result = json.load(f)
        assert result["data"]["fraud_risk_level"] == "MEDIUM"
        assert result["data"]["final_status"] == "settled"

    def test_txn004_cross_border_unusual_hour_medium_risk(self, tmp_path):
        """TXN004: EUR 500 at 02:47 from DE → cross-border(1) + unusual_hour(2) = 3 = MEDIUM."""
        results_dir = tmp_path / "results"
        run_pipeline(
            transactions_file=SAMPLE_TRANSACTIONS_FILE,
            results_dir=str(results_dir),
        )
        with open(results_dir / "TXN004.json") as f:
            result = json.load(f)
        data = result["data"]
        assert data["fraud_risk_score"] == 3
        assert data["fraud_risk_level"] == "MEDIUM"
        assert data["final_status"] == "settled"
