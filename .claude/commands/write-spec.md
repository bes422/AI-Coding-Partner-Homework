Generate a complete `specification.md` for an AI-powered banking transaction pipeline.

Follow this exact 5-section template and save the result as `homework-6/specification.md`.

## Template

```markdown
# Specification: [Project Name]

## 1. High-Level Objective
[One sentence describing the full pipeline and its purpose.]

## 2. Mid-Level Objectives
- [Testable requirement 1 — something you can write a unit test for]
- [Testable requirement 2]
- [Testable requirement 3]
- [Testable requirement 4]
- [Testable requirement 5]

## 3. Implementation Notes
- Monetary calculations: decimal.Decimal only, never float
- Currency validation: ISO 4217 whitelist (USD, EUR, GBP, JPY, CHF, CAD, AUD minimum)
- Logging: audit trail with timestamp (ISO 8601), agent name, transaction_id, outcome
- PII: mask account numbers in all log output (show only last 4 chars)
- Settlement fee: 0.1% of amount, rounded with ROUND_HALF_UP

## 4. Context
- **Beginning state**: `sample-transactions.json` exists with raw transaction records.
  No agent modules exist. No `shared/` directories exist.
- **Ending state**: All transactions processed. Results in `shared/results/`.
  Test coverage ≥ 90%. README and HOWTORUN complete.

## 5. Low-Level Tasks

### Task: Transaction Validator
**Prompt**: "[Exact prompt for Claude Code]"
**File to CREATE**: `agents/transaction_validator.py`
**Function to CREATE**: `process_message(message: dict) -> dict`
**Details**: [Validation rules, field checks, return format]

### Task: Fraud Detector
**Prompt**: "[Exact prompt for Claude Code]"
**File to CREATE**: `agents/fraud_detector.py`
**Function to CREATE**: `process_message(message: dict) -> dict`
**Details**: [Scoring rules, risk levels, pass-through behavior]

### Task: Settlement Processor
**Prompt**: "[Exact prompt for Claude Code]"
**File to CREATE**: `agents/settlement_processor.py`
**Function to CREATE**: `process_message(message: dict, results_dir: str = None) -> dict`
**Details**: [Settlement logic, fee calculation, result file format]
```

## Steps

1. Read `homework-6/specification-TEMPLATE-hint.md` to understand the template structure.
2. Read `homework-6/sample-transactions.json` to understand the input data shape.
3. Fill in the template with project-specific content for this banking pipeline.
4. Ensure all Mid-Level Objectives are testable (can be verified with a unit test).
5. Write the completed specification to `homework-6/specification.md`.
6. Confirm the file was created and show a summary of each section.
