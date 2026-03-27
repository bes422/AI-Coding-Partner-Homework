# Research Notes — context7 Queries During Pipeline Development

This file documents the context7 MCP queries made while building the AI-Powered Banking Pipeline (Agent 2 — Code Generation phase).

---

## Query 1: Python `decimal` Module for Monetary Arithmetic

- **Search**: `"Python decimal module monetary arithmetic banking"`
- **context7 library ID**: `/python/decimal`
- **What I looked up**: How to use `decimal.Decimal` for precise monetary calculations, how `ROUND_HALF_UP` works, and how to avoid float precision errors in financial software.
- **Key insight applied**:
  - Used `Decimal(str(amount))` instead of `Decimal(float_value)` to avoid float contamination
  - Applied `ROUND_HALF_UP` via `.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` for the 0.1% settlement fee
  - Example: `fee = (Decimal("9999.99") * Decimal("0.001")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` → `Decimal("10.00")`
- **Code pattern adopted** (`agents/settlement_processor.py`):
  ```python
  from decimal import ROUND_HALF_UP, Decimal

  FEE_RATE = Decimal("0.001")
  fee = (amount * FEE_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
  net_amount = amount - fee
  ```

---

## Query 2: Python `uuid` Module for Unique Message IDs

- **Search**: `"Python uuid4 unique identifier generation"`
- **context7 library ID**: `/python/uuid`
- **What I looked up**: How to generate RFC 4122 UUID4 strings for `message_id` fields in the pipeline message format.
- **Key insight applied**:
  - `uuid.uuid4()` generates a random 128-bit UUID
  - Converting to string with `str(uuid.uuid4())` gives the standard hyphenated format (`"550e8400-e29b-41d4-a716-446655440000"`)
  - Each call to `uuid.uuid4()` is guaranteed to produce a unique ID — suitable for message deduplication
- **Code pattern adopted** (`integrator.py`):
  ```python
  import uuid

  def wrap_transaction(txn: dict) -> dict:
      return {
          "message_id": str(uuid.uuid4()),
          ...
      }
  ```

---

## Query 3: Python `logging` Module with ISO 8601 Timestamps

- **Search**: `"Python logging ISO 8601 timestamp format audit log"`
- **context7 library ID**: `/python/logging`
- **What I looked up**: How to configure Python's `logging` module to produce ISO 8601 formatted timestamps in the audit trail, consistent with the pipeline's `timestamp` fields.
- **Key insight applied**:
  - `datefmt="%Y-%m-%dT%H:%M:%S%z"` produces ISO 8601-compliant timestamps
  - Used `%(asctime)s` in the format string with this `datefmt` across all agent loggers
  - Chose `logging.INFO` as the default level with `logging.WARNING` for rejections and blocks
- **Code pattern adopted** (all agent files):
  ```python
  import logging

  logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s %(name)s %(levelname)s %(message)s",
      datefmt="%Y-%m-%dT%H:%M:%S%z",
  )
  logger = logging.getLogger(AGENT_NAME)
  ```

---

## Summary

| Query | Library | Key Pattern |
|-------|---------|-------------|
| Decimal arithmetic | `/python/decimal` | `ROUND_HALF_UP` for settlement fees, never use `float` |
| UUID generation | `/python/uuid` | `str(uuid.uuid4())` for unique `message_id` |
| ISO 8601 logging | `/python/logging` | `datefmt="%Y-%m-%dT%H:%M:%S%z"` for audit trail |
