"""Settlement Processor Agent — settles or blocks transactions based on fraud risk score."""
import json
import logging
import os
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal

AGENT_NAME = "settlement_processor"
FEE_RATE = Decimal("0.001")  # 0.1% settlement fee

# Default results directory (relative to this file's parent directory)
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RESULTS_DIR = os.path.join(_BASE_DIR, "shared", "results")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
logger = logging.getLogger(AGENT_NAME)


def settle_transaction(data: dict) -> dict:
    """
    Settle or block a transaction based on its validation status and fraud risk.

    Outcomes:
      - status == "rejected" → final_status = "rejected"
      - fraud_risk_level == "HIGH" → final_status = "blocked"
      - fraud_risk_level in {"LOW", "MEDIUM"} → final_status = "settled"
        with settlement_fee (0.1%) and net_amount calculated using Decimal
    """
    status = data.get("status", "")

    # Already rejected by the validator — forward to results
    if status == "rejected":
        data["final_status"] = "rejected"
        data["final_reason"] = data.get("reason", "VALIDATION_FAILED")
        return data

    fraud_level = data.get("fraud_risk_level", "LOW")
    transaction_id = data.get("transaction_id", "UNKNOWN")

    if fraud_level == "HIGH":
        data["final_status"] = "blocked"
        data["final_reason"] = f"HIGH_FRAUD_RISK (score={data.get('fraud_risk_score', 0)})"
        logger.warning(
            "BLOCKED txn=%s fraud_score=%s",
            transaction_id,
            data.get("fraud_risk_score"),
        )
    else:
        # Settle with fee
        amount = Decimal(str(data.get("amount", "0")))
        fee = (amount * FEE_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        net_amount = amount - fee

        data["final_status"] = "settled"
        data["settlement_fee"] = str(fee)
        data["net_amount"] = str(net_amount)

        logger.info(
            "SETTLED txn=%s amount=%s fee=%s net=%s %s",
            transaction_id,
            amount,
            fee,
            net_amount,
            data.get("currency"),
        )

    return data


def process_message(message: dict, results_dir: str = None) -> dict:
    """
    Process a message through the settlement processor.
    Writes result JSON to results_dir (defaults to shared/results/).
    Returns the updated message.
    """
    if results_dir is None:
        results_dir = DEFAULT_RESULTS_DIR

    data = message.get("data", {})
    transaction_id = data.get("transaction_id", "UNKNOWN")

    data = settle_transaction(data)

    result_message = {
        **message,
        "source_agent": AGENT_NAME,
        "target_agent": "results",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }

    # Write result file to shared/results/
    os.makedirs(results_dir, exist_ok=True)
    result_path = os.path.join(results_dir, f"{transaction_id}.json")
    with open(result_path, "w") as f:
        json.dump(result_message, f, indent=2)

    logger.info(
        "RESULT written txn=%s final_status=%s path=%s",
        transaction_id,
        data.get("final_status"),
        result_path,
    )

    return result_message
