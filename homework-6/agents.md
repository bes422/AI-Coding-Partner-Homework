# Agents — AI-Powered Banking Transaction Pipeline

This file describes the four meta-agents that build and operate the banking pipeline, plus the three pipeline agents they produce.

---

## Meta-Agents (What You Build With Claude Code)

### Agent 1 — Specification Agent
**Role**: Produces `specification.md` from the template.
**Skill**: `/write-spec` slash command (`.claude/commands/write-spec.md`)
**Output**: `specification.md` with all 5 required sections.

### Agent 2 — Code Generation Agent
**Role**: Generates the full pipeline code (3 cooperating agents + integrator).
**MCP**: Uses `context7` to look up Python library docs during generation.
**Output**: `agents/` directory with validator, fraud detector, settlement processor; `integrator.py`.

### Agent 3 — Unit Test Agent
**Role**: Creates the test suite and enforces coverage standards.
**Hook**: Coverage gate in `.claude/settings.json` blocks `git push` if coverage < 80%.
**Skills**: `/run-pipeline`, `/validate-transactions`
**Output**: `tests/` directory with unit and integration tests.

### Agent 4 — Documentation Agent
**Role**: Generates README, HOWTORUN, and project documentation.
**Requirement**: README must include author name and ASCII pipeline diagram.
**Output**: `README.md`, `HOWTORUN.md`.

---

## Pipeline Agents (What the Meta-Agents Produce)

### Transaction Validator (`agents/transaction_validator.py`)

**Purpose**: First stage of the pipeline. Validates every incoming transaction.

**Validation rules**:
- Required fields: `transaction_id`, `amount`, `currency`, `source_account`, `destination_account`
- Amount must be a positive `Decimal` (never `float`)
- Currency must be in ISO 4217 whitelist: `{USD, EUR, GBP, JPY, CHF, CAD, AUD}`

**Outputs** (sets `data.status`):
- `"validated"` → passes to Fraud Detector
- `"rejected"` + `reason` field → passes to Settlement Processor for result logging

**File**: `agents/transaction_validator.py`
**Entry point**: `process_message(message: dict) -> dict`
**CLI**: `python agents/transaction_validator.py --dry-run`

---

### Fraud Detector (`agents/fraud_detector.py`)

**Purpose**: Second stage. Scores validated transactions for fraud risk.

**Scoring (cumulative)**:
| Trigger | Points |
|---------|--------|
| Amount > $10,000 | +3 |
| Amount > $50,000 | +4 additional (total +7 for >$50k) |
| Transaction hour 02:00–05:00 UTC | +2 |
| Cross-border (country ≠ US) | +1 |

**Risk levels**:
| Range | Level |
|-------|-------|
| 0–2 | LOW |
| 3–6 | MEDIUM |
| 7–10 | HIGH |

**Behavior**: Rejected transactions pass through unchanged (no scoring).

**File**: `agents/fraud_detector.py`
**Entry point**: `process_message(message: dict) -> dict`

---

### Settlement Processor (`agents/settlement_processor.py`)

**Purpose**: Final stage. Settles, blocks, or records rejected transactions; writes result files.

**Decision logic**:
| Input status | fraud_risk_level | Action | final_status |
|-------------|-----------------|--------|--------------|
| `rejected` | (n/a) | Write result | `rejected` |
| `validated` | `HIGH` | Block + write result | `blocked` |
| `validated` | `LOW` or `MEDIUM` | Settle + write result | `settled` |

**Settlement fee**: 0.1% of amount, rounded with `ROUND_HALF_UP`, stored as `Decimal` string.

**Output file**: `shared/results/{transaction_id}.json`

**File**: `agents/settlement_processor.py`
**Entry point**: `process_message(message: dict, results_dir: str = None) -> dict`

---

## File-Based Message Protocol

Agents communicate via JSON files through the `shared/` directory tree:

```
shared/
├── input/       ← integrator writes initial messages here
├── processing/  ← reserved for in-flight processing state
├── output/      ← validator and fraud detector write results here
└── results/     ← settlement processor writes final outcomes here
```

### Standard Message Format

```json
{
  "message_id": "<uuid4>",
  "timestamp": "2026-03-16T10:00:00Z",
  "source_agent": "transaction_validator",
  "target_agent": "fraud_detector",
  "message_type": "transaction",
  "data": {
    "transaction_id": "TXN001",
    "amount": "1500.00",
    "currency": "USD",
    "source_account": "ACC-1001",
    "destination_account": "ACC-2001",
    "status": "validated",
    "fraud_risk_score": 0,
    "fraud_risk_level": "LOW",
    "final_status": "settled",
    "settlement_fee": "1.50",
    "net_amount": "1498.50"
  }
}
```

---

## Pipeline Flow

```
sample-transactions.json
        │
        ▼
  [Integrator]  (wraps each txn in message format, writes to shared/input/)
        │
        ▼
[Transaction Validator]
    ├── rejected ──────────────────────────────▶ [Settlement Processor]
    │                                                     │
    └── validated ──▶ [Fraud Detector]                    │
                            │                             │
                            └── scored ──────────────▶ [Settlement Processor]
                                                          │
                                                          ▼
                                                   shared/results/
```

---

## Security & Compliance Notes

- **PII**: Account numbers are masked in all logs (only last 4 chars shown)
- **Audit trail**: Every log entry includes ISO 8601 timestamp, agent name, transaction ID, outcome
- **No float arithmetic**: All monetary values use `decimal.Decimal` with explicit rounding
- **Isolation**: Tests use `tmp_path` fixture — never touch real `shared/` directories
