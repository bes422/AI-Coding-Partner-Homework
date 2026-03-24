"""Fraud Detector Agent — scores transactions for fraud risk based on amount, timing, and geography."""
import logging
from datetime import datetime, timezone
from decimal import Decimal

AGENT_NAME = "fraud_detector"
HOME_COUNTRY = "US"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
logger = logging.getLogger(AGENT_NAME)


def score_transaction(data: dict) -> tuple:
    """
    Score a transaction for fraud risk.
    Returns (score: int, level: str) where level is LOW / MEDIUM / HIGH.

    Scoring rules:
      - amount > $50,000  → +4 pts
      - amount > $10,000  → +3 pts  (mutually exclusive with above)
      - unusual hour 02:00–05:00 UTC → +2 pts
      - cross-border (country != US) → +1 pt

    Risk levels:
      - LOW    : 0–2
      - MEDIUM : 3–6
      - HIGH   : 7–10
    """
    score = 0

    # High-value amount scoring
    try:
        amount = Decimal(str(data.get("amount", "0")))
    except Exception:
        amount = Decimal("0")

    # Cumulative high-value scoring (both rules can fire)
    if amount > Decimal("10000"):
        score += 3
    if amount > Decimal("50000"):
        score += 4  # additional 4 pts on top of the 3 above

    # Unusual hour: 02:00–05:00 UTC
    timestamp_str = data.get("timestamp", "")
    try:
        ts = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        if 2 <= ts.hour < 5:
            score += 2
    except (ValueError, AttributeError):
        pass

    # Cross-border transaction
    country = data.get("metadata", {}).get("country", HOME_COUNTRY)
    if country != HOME_COUNTRY:
        score += 1

    # Determine risk level
    if score >= 7:
        level = "HIGH"
    elif score >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level


def process_message(message: dict) -> dict:
    """
    Process a message through the fraud detector.
    Rejected transactions (from validator) are passed through unchanged.
    Validated transactions receive fraud_risk_score and fraud_risk_level fields.
    """
    data = message.get("data", {})

    # Pass through already-rejected transactions without scoring
    if data.get("status") == "rejected":
        return {
            **message,
            "source_agent": AGENT_NAME,
            "target_agent": "settlement_processor",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }

    transaction_id = data.get("transaction_id", "UNKNOWN")
    score, level = score_transaction(data)

    data["fraud_risk_score"] = score
    data["fraud_risk_level"] = level

    logger.info(
        "SCORED txn=%s score=%d level=%s amount=%s %s",
        transaction_id,
        score,
        level,
        data.get("amount"),
        data.get("currency"),
    )

    return {
        **message,
        "source_agent": AGENT_NAME,
        "target_agent": "settlement_processor",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }
