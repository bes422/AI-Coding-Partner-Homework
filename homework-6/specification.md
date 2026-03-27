# Specification: AI-Powered Multi-Agent Banking Transaction Pipeline

## 1. High-Level Objective

Build a 3-agent Python pipeline that validates, scores for fraud risk, and settles banking transactions using file-based JSON message passing through shared directories.

---

## 2. Mid-Level Objectives

1. **Transactions with invalid currency codes** (not in USD, EUR, GBP, JPY, CHF, CAD, AUD) are rejected by the Transaction Validator with status `"rejected"` and reason `"INVALID_CURRENCY"`, and a result file is written to `shared/results/`.

2. **Transactions with non-positive amounts** (zero or negative) are rejected by the Transaction Validator with status `"rejected"` and reason `"INVALID_AMOUNT"`.

3. **High-value transactions** receive cumulative fraud risk scoring: amounts above $10,000 add +3 pts; amounts above $50,000 add an additional +4 pts (total +7 for >$50k → HIGH risk). Transactions with `fraud_risk_level == "HIGH"` are blocked by the Settlement Processor with `final_status: "blocked"`.

4. **All agent operations are logged** with ISO 8601 timestamps, the agent name, transaction ID, and outcome. Account numbers are masked (last 4 digits only) in all log output.

5. **All 8 sample transactions** in `sample-transactions.json` produce a result file in `shared/results/` with the standard message format and a `final_status` field (`settled`, `rejected`, or `blocked`).

---

## 3. Implementation Notes

- **Monetary calculations**: `decimal.Decimal` only — never `float`. Use `ROUND_HALF_UP` for fee calculations.
- **Currency validation**: ISO 4217 whitelist: `{"USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD"}`.
- **Logging format**: `%(asctime)s %(name)s %(levelname)s %(message)s` with `datefmt="%Y-%m-%dT%H:%M:%S%z"` (ISO 8601).
- **PII**: Account numbers are masked in all log output — only the last 4 characters are shown (e.g., `ACC-1001` → `****1001`).
- **Message format**: Every pipeline message must carry `message_id` (UUID4), `timestamp` (ISO 8601), `source_agent`, `target_agent`, `message_type`, and `data`.
- **Settlement fee**: 0.1% of transaction amount, rounded to 2 decimal places.
- **Fraud scoring** (cumulative):
  - amount > $10,000 → +3 pts
  - amount > $50,000 → +4 pts (additional)
  - transaction hour 02:00–05:00 UTC → +2 pts
  - cross-border (country ≠ US) → +1 pt
  - Risk levels: LOW (0–2), MEDIUM (3–6), HIGH (7–10)

---

## 4. Context

- **Beginning state**: `sample-transactions.json` exists with 8 raw transaction records. No agent modules, no `shared/` directories, no results.
- **Ending state**: All 8 transactions processed; result files in `shared/results/`; test coverage ≥ 90%; `README.md` and `HOWTORUN.md` complete; MCP server queryable.

---

## 5. Low-Level Tasks

### Task: Transaction Validator

**Prompt**:
```
Context: Python banking pipeline. homework-6/ is the working directory. sample-transactions.json
contains 8 raw transaction records.
Task: Create agents/transaction_validator.py with a process_message(message: dict) -> dict function
that validates each transaction for required fields, positive Decimal amount, and ISO 4217 currency.
Rules: Use decimal.Decimal (never float). Mask account numbers in logs. Support --dry-run CLI flag.
Return status: "validated" or "rejected" with a reason field.
Output: File at agents/transaction_validator.py. Runnable as python agents/transaction_validator.py --dry-run.
```

**File to CREATE**: `agents/transaction_validator.py`
**Function to CREATE**: `process_message(message: dict) -> dict`
**Details**:
- Check required fields: `transaction_id`, `amount`, `currency`, `source_account`, `destination_account`
- Validate amount is a positive `Decimal`
- Validate currency against ISO 4217 whitelist
- Return message with `data.status = "validated"` or `"rejected"` + `data.reason` field
- Set `target_agent = "fraud_detector"` (validated) or `"settlement_processor"` (rejected)
- Support `--dry-run` CLI flag and `--input` path argument

---

### Task: Fraud Detector

**Prompt**:
```
Context: Python banking pipeline. Receives messages from transaction_validator with status "validated"
or "rejected". Validated messages must be scored for fraud risk.
Task: Create agents/fraud_detector.py with process_message(message: dict) -> dict that scores
validated transactions and passes rejected ones through unchanged.
Rules: Cumulative scoring: >$10k → +3pts, >$50k → +4pts additional, hour 02-05 UTC → +2pts,
non-US country → +1pt. Levels: LOW(0-2), MEDIUM(3-6), HIGH(7-10). Use Decimal for amounts.
Output: Message with fraud_risk_score (int) and fraud_risk_level (str) in data field.
```

**File to CREATE**: `agents/fraud_detector.py`
**Function to CREATE**: `process_message(message: dict) -> dict`
**Details**:
- Pass through messages with `status == "rejected"` unchanged
- Score validated transactions using cumulative rules above
- Add `fraud_risk_score` and `fraud_risk_level` to `data`
- Set `target_agent = "settlement_processor"` for all messages

---

### Task: Settlement Processor

**Prompt**:
```
Context: Python banking pipeline. Receives messages from fraud_detector. Must settle or block
transactions based on fraud risk, and write final results to shared/results/.
Task: Create agents/settlement_processor.py with process_message(message: dict, results_dir: str = None)
-> dict that settles LOW/MEDIUM risk transactions, blocks HIGH risk, passes through rejected.
Rules: Use Decimal(ROUND_HALF_UP) for 0.1% settlement fee. Write JSON result file per transaction.
Never use float for monetary values.
Output: JSON file in shared/results/{transaction_id}.json with final_status field.
```

**File to CREATE**: `agents/settlement_processor.py`
**Function to CREATE**: `process_message(message: dict, results_dir: str = None) -> dict`
**Details**:
- `status == "rejected"` → `final_status = "rejected"`, write result file
- `fraud_risk_level == "HIGH"` → `final_status = "blocked"`, write result file
- Otherwise → `final_status = "settled"`, calculate `settlement_fee` (0.1%), `net_amount`, write result file
- `results_dir` parameter allows test isolation with `tmp_path`
