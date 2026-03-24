"""Integrator — orchestrates the multi-agent banking transaction pipeline.

Pipeline flow:
  sample-transactions.json
        │
        ▼
  [Transaction Validator]  ──rejected──▶ shared/results/
        │ validated
        ▼
  [Fraud Detector]
        │ scored
        ▼
  [Settlement Processor]  ──blocked──▶ shared/results/
        │ settled
        ▼
    shared/results/
"""
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Ensure homework-6/ is on the path so agent imports work
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from agents.fraud_detector import process_message as detect_fraud
from agents.settlement_processor import process_message as settle
from agents.transaction_validator import process_message as validate

TRANSACTIONS_FILE = BASE_DIR / "sample-transactions.json"
SHARED_DIRS = [
    BASE_DIR / "shared" / "input",
    BASE_DIR / "shared" / "processing",
    BASE_DIR / "shared" / "output",
    BASE_DIR / "shared" / "results",
]


def setup_directories():
    """Create shared/ subdirectories if they don't exist."""
    for d in SHARED_DIRS:
        d.mkdir(parents=True, exist_ok=True)


def clear_shared():
    """Remove all JSON files from shared/ subdirectories."""
    for d in SHARED_DIRS:
        if d.exists():
            for f in d.glob("*.json"):
                f.unlink()


def wrap_transaction(txn: dict) -> dict:
    """Wrap a raw transaction dict in the standard pipeline message format."""
    return {
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_agent": "integrator",
        "target_agent": "transaction_validator",
        "message_type": "transaction",
        "data": dict(txn),
    }


def write_json(path: Path, obj: dict):
    """Write a dict as pretty-printed JSON to path."""
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


def run_pipeline(transactions_file: Path = None, results_dir: str = None):
    """
    Run the full banking pipeline for all transactions.

    Args:
        transactions_file: Path to sample-transactions.json (defaults to TRANSACTIONS_FILE)
        results_dir: Override for shared/results/ directory (used in tests)

    Returns:
        dict with keys: total, settled, rejected, blocked, results
    """
    if transactions_file is None:
        transactions_file = TRANSACTIONS_FILE
    if results_dir is None:
        results_dir = str(BASE_DIR / "shared" / "results")

    setup_directories()
    clear_shared()

    print(f"[Integrator] Loading transactions from {transactions_file}")
    with open(transactions_file, "r") as f:
        transactions = json.load(f)

    print(f"[Integrator] Processing {len(transactions)} transactions...\n")

    counters = {"total": 0, "settled": 0, "rejected": 0, "blocked": 0}
    all_results = []

    for txn in transactions:
        tid = txn.get("transaction_id", "UNKNOWN")

        # Wrap and write to shared/input/
        message = wrap_transaction(txn)
        write_json(BASE_DIR / "shared" / "input" / f"{tid}.json", message)

        # Step 1: Transaction Validator
        message = validate(message)
        write_json(BASE_DIR / "shared" / "output" / f"{tid}.json", message)

        # Step 2: Fraud Detector
        message = detect_fraud(message)
        write_json(BASE_DIR / "shared" / "output" / f"{tid}.json", message)

        # Step 3: Settlement Processor (writes to results_dir)
        message = settle(message, results_dir=results_dir)

        final_status = message["data"].get("final_status", "unknown")
        counters["total"] += 1
        counters[final_status] = counters.get(final_status, 0) + 1
        all_results.append(message)

        # Console output
        suffix = ""
        if final_status == "rejected":
            suffix = f" — {message['data'].get('reason', 'unknown')}"
        elif final_status == "blocked":
            suffix = f" — {message['data'].get('final_reason', '')}"
        elif final_status == "settled":
            suffix = f" — net={message['data'].get('net_amount')} {message['data'].get('currency')}"
        print(f"  {tid}: {final_status.upper()}{suffix}")

    # Summary
    result_files = list(Path(results_dir).glob("*.json"))
    print(f"\n{'=' * 60}")
    print("Pipeline Summary")
    print(f"{'=' * 60}")
    print(f"Total processed:  {counters['total']}")
    print(f"Settled:          {counters.get('settled', 0)}")
    print(f"Rejected:         {counters.get('rejected', 0)}")
    print(f"Blocked:          {counters.get('blocked', 0)}")
    print(f"Result files:     {len(result_files)}")
    print(f"{'=' * 60}\n")

    return {**counters, "results": all_results}


if __name__ == "__main__":
    run_pipeline()
