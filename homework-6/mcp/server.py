"""
FastMCP server for the AI Banking Pipeline.

Exposes:
  - Tool: get_transaction_status(transaction_id) → current result from shared/results/
  - Tool: list_pipeline_results() → summary of all processed transactions
  - Resource: pipeline://summary → latest pipeline run summary as text
"""
import glob
import json
import os
from pathlib import Path

from fastmcp import FastMCP

# Resolve shared/results/ relative to this file's grandparent (homework-6/)
BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / "shared" / "results"

mcp = FastMCP("pipeline-status")


def _load_results() -> list[dict]:
    """Load all result JSON files from shared/results/."""
    results = []
    pattern = str(RESULTS_DIR / "*.json")
    for path in sorted(glob.glob(pattern)):
        try:
            with open(path, "r") as f:
                results.append(json.load(f))
        except (json.JSONDecodeError, OSError):
            pass
    return results


@mcp.tool()
def get_transaction_status(transaction_id: str) -> dict:
    """
    Return the current pipeline status for a given transaction ID.
    Reads from shared/results/{transaction_id}.json.
    """
    result_path = RESULTS_DIR / f"{transaction_id}.json"
    if not result_path.exists():
        return {
            "found": False,
            "transaction_id": transaction_id,
            "error": f"No result found for transaction {transaction_id}",
        }
    try:
        with open(result_path, "r") as f:
            data = json.load(f)
        txn_data = data.get("data", {})
        return {
            "found": True,
            "transaction_id": transaction_id,
            "final_status": txn_data.get("final_status"),
            "fraud_risk_level": txn_data.get("fraud_risk_level"),
            "fraud_risk_score": txn_data.get("fraud_risk_score"),
            "amount": txn_data.get("amount"),
            "currency": txn_data.get("currency"),
            "settlement_fee": txn_data.get("settlement_fee"),
            "net_amount": txn_data.get("net_amount"),
            "reason": txn_data.get("reason") or txn_data.get("final_reason"),
            "timestamp": data.get("timestamp"),
        }
    except (json.JSONDecodeError, OSError) as e:
        return {"found": False, "transaction_id": transaction_id, "error": str(e)}


@mcp.tool()
def list_pipeline_results() -> dict:
    """
    Return a summary of all processed transactions from shared/results/.
    Includes counts by final status and a list of all results.
    """
    results = _load_results()
    if not results:
        return {
            "total": 0,
            "settled": 0,
            "rejected": 0,
            "blocked": 0,
            "transactions": [],
            "message": "No results found. Run the pipeline first (python integrator.py).",
        }

    counters = {"settled": 0, "rejected": 0, "blocked": 0}
    transactions = []

    for r in results:
        data = r.get("data", {})
        final_status = data.get("final_status", "unknown")
        counters[final_status] = counters.get(final_status, 0) + 1
        transactions.append(
            {
                "transaction_id": data.get("transaction_id"),
                "final_status": final_status,
                "amount": data.get("amount"),
                "currency": data.get("currency"),
                "fraud_risk_level": data.get("fraud_risk_level"),
                "fraud_risk_score": data.get("fraud_risk_score"),
                "net_amount": data.get("net_amount"),
                "reason": data.get("reason") or data.get("final_reason"),
            }
        )

    return {
        "total": len(results),
        "settled": counters.get("settled", 0),
        "rejected": counters.get("rejected", 0),
        "blocked": counters.get("blocked", 0),
        "transactions": transactions,
    }


@mcp.resource("pipeline://summary")
def pipeline_summary() -> str:
    """Return the latest pipeline run summary as formatted text."""
    results = _load_results()

    if not results:
        return (
            "Pipeline Summary\n"
            "================\n"
            "No results available. Run: python integrator.py\n"
        )

    counters = {"settled": 0, "rejected": 0, "blocked": 0}
    lines = []

    for r in results:
        data = r.get("data", {})
        final_status = data.get("final_status", "unknown")
        counters[final_status] = counters.get(final_status, 0) + 1
        tid = data.get("transaction_id", "?")
        amount = data.get("amount", "?")
        currency = data.get("currency", "?")
        reason = data.get("reason") or data.get("final_reason", "")
        net = data.get("net_amount", "")
        detail = f"net={net}" if net else (f"reason={reason}" if reason else "")
        lines.append(f"  {tid:<10} {final_status.upper():<10} {amount} {currency}  {detail}")

    total = len(results)
    summary = (
        f"Pipeline Summary\n"
        f"{'=' * 50}\n"
        f"Total:    {total}\n"
        f"Settled:  {counters.get('settled', 0)}\n"
        f"Rejected: {counters.get('rejected', 0)}\n"
        f"Blocked:  {counters.get('blocked', 0)}\n"
        f"\nTransaction Details:\n"
        f"{'=' * 50}\n"
    )
    summary += "\n".join(lines) + "\n"
    return summary


if __name__ == "__main__":
    mcp.run()
