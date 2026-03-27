"""Transaction Validator Agent — validates transactions for required fields, amounts, and currency codes."""
import argparse
import json
import logging
import os
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

AGENT_NAME = "transaction_validator"

# ISO 4217 currency whitelist
ISO_4217_WHITELIST = {"USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD"}

# Required transaction fields
REQUIRED_FIELDS = ["transaction_id", "amount", "currency", "source_account", "destination_account"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
logger = logging.getLogger(AGENT_NAME)


def mask_account(account: str) -> str:
    """Mask account number for PII protection, showing only last 4 chars."""
    if not account:
        return "****"
    if len(account) <= 4:
        return "****"
    return "****" + account[-4:]


def validate_transaction(data: dict) -> tuple:
    """
    Validate a transaction dict.
    Returns (is_valid: bool, reason: str) where reason is empty string if valid.
    """
    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data or data[field] is None or data[field] == "":
            return False, f"MISSING_FIELD:{field}"

    # Validate currency against ISO 4217 whitelist
    currency = str(data.get("currency", "")).strip().upper()
    if currency not in ISO_4217_WHITELIST:
        return False, "INVALID_CURRENCY"

    # Validate amount is a positive Decimal
    try:
        amount = Decimal(str(data["amount"]))
    except (InvalidOperation, ValueError, TypeError):
        return False, "INVALID_AMOUNT"

    if amount <= Decimal("0"):
        return False, "INVALID_AMOUNT"

    return True, ""


def process_message(message: dict) -> dict:
    """
    Process a message through the transaction validator.
    Returns the message updated with validation status.
    """
    data = message.get("data", {})
    transaction_id = data.get("transaction_id", "UNKNOWN")

    is_valid, reason = validate_transaction(data)

    if is_valid:
        data["status"] = "validated"
        logger.info(
            "VALIDATED txn=%s src=%s dst=%s amount=%s %s",
            transaction_id,
            mask_account(data.get("source_account", "")),
            mask_account(data.get("destination_account", "")),
            data.get("amount"),
            data.get("currency"),
        )
    else:
        data["status"] = "rejected"
        data["reason"] = reason
        logger.warning(
            "REJECTED txn=%s reason=%s",
            transaction_id,
            reason,
        )

    return {
        **message,
        "source_agent": AGENT_NAME,
        "target_agent": "fraud_detector" if is_valid else "settlement_processor",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }


def main():
    parser = argparse.ArgumentParser(description="Transaction Validator Agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate transactions and report without side effects",
    )
    parser.add_argument(
        "--input",
        default="sample-transactions.json",
        help="Path to input transactions JSON file",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: {args.input} not found", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r") as f:
        transactions = json.load(f)

    results = []
    for txn in transactions:
        is_valid, reason = validate_transaction(txn)
        results.append(
            {
                "transaction_id": txn.get("transaction_id", "UNKNOWN"),
                "valid": is_valid,
                "reason": reason if not is_valid else "OK",
                "amount": txn.get("amount"),
                "currency": txn.get("currency"),
            }
        )

    total = len(results)
    valid_count = sum(1 for r in results if r["valid"])
    invalid_count = total - valid_count

    print(f"\n{'=' * 60}")
    print(f"Transaction Validation Report {'(DRY RUN) ' if args.dry_run else ''}")
    print(f"{'=' * 60}")
    print(f"Total:    {total}")
    print(f"Valid:    {valid_count}")
    print(f"Invalid:  {invalid_count}")
    print(f"\n{'ID':<10} {'Amount':<12} {'Currency':<10} {'Valid':<8} {'Reason'}")
    print("-" * 60)
    for r in results:
        print(
            f"{r['transaction_id']:<10} {str(r['amount']):<12} {str(r['currency']):<10} {str(r['valid']):<8} {r['reason']}"
        )
    print()


if __name__ == "__main__":
    main()
