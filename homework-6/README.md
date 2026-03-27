# AI-Powered Multi-Agent Banking Transaction Pipeline

**Created by Mykhailo Bestiuk**

---

## What This System Does

This project implements an AI-powered multi-agent banking pipeline that processes financial transactions through three cooperating agents. Starting from a JSON file of raw transaction records, the system validates each transaction, scores it for fraud risk, and either settles or blocks it — writing a complete audit trail of result files.

The pipeline is orchestrated by an integrator that passes messages between agents using a file-based JSON communication protocol via shared directories. Each agent has a single, well-defined responsibility and communicates with the next agent through a standard message format that carries the full transaction history as it flows through the pipeline.

---

## Agent Responsibilities

- **Transaction Validator** (`agents/transaction_validator.py`): Checks required fields, validates that amounts are positive `Decimal` values, and verifies currency codes against the ISO 4217 whitelist. Rejects invalid transactions with a specific reason code.

- **Fraud Detector** (`agents/fraud_detector.py`): Scores validated transactions for fraud risk using cumulative rules — high amounts, unusual transaction hours (02:00–05:00 UTC), and cross-border transfers. Assigns LOW / MEDIUM / HIGH risk level.

- **Settlement Processor** (`agents/settlement_processor.py`): Settles LOW and MEDIUM risk transactions (applying a 0.1% fee via precise Decimal arithmetic), blocks HIGH risk transactions, and writes a final result file for every transaction (including rejected ones).

---

## Pipeline Architecture

```
sample-transactions.json
          │
          ▼
    [Integrator]
    (wraps each transaction in message format, writes to shared/input/)
          │
          ▼
[Transaction Validator]
    ├── status: rejected ─────────────────────────────────┐
    │   (INVALID_CURRENCY, INVALID_AMOUNT, MISSING_FIELD)  │
    │                                                       │
    └── status: validated ──▶ [Fraud Detector]             │
                                     │                     │
                              scores transaction           │
                              fraud_risk_score             │
                              fraud_risk_level             │
                                     │                     │
                                     ▼                     ▼
                          [Settlement Processor]           │
                          ├── HIGH risk → blocked          │
                          └── LOW/MEDIUM → settled         │
                                     │                     │
                                     └──────────┬──────────┘
                                                ▼
                                         shared/results/
                                    {transaction_id}.json
                                    (final_status, net_amount,
                                     settlement_fee, fraud_risk_*)
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| Monetary arithmetic | `decimal.Decimal` (stdlib) |
| Unique message IDs | `uuid.uuid4()` (stdlib) |
| Logging | `logging` with ISO 8601 timestamps (stdlib) |
| MCP server | `fastmcp` |
| Tests | `pytest` |
| Test coverage | `pytest-cov` |
| Agent communication | File-based JSON (shared directories) |
| context7 MCP | `@upstash/context7-mcp` (npx) |

---

## Project Structure

```
homework-6/
├── sample-transactions.json     # 8 input transactions
├── integrator.py                # Pipeline orchestrator
├── agents/
│   ├── transaction_validator.py # Agent 1: validates fields, currency, amount
│   ├── fraud_detector.py        # Agent 2: scores fraud risk
│   └── settlement_processor.py  # Agent 3: settles or blocks + writes results
├── shared/
│   ├── input/                   # Initial messages from integrator
│   ├── processing/              # Reserved for in-flight state
│   ├── output/                  # Inter-agent message exchange
│   └── results/                 # Final outcome files (one per transaction)
├── mcp/
│   └── server.py                # FastMCP server (query pipeline results)
├── mcp.json                     # MCP server configuration
├── tests/
│   ├── test_validator.py
│   ├── test_fraud_detector.py
│   ├── test_settlement.py
│   └── test_integration.py
├── specification.md
├── agents.md
├── research-notes.md
├── README.md
└── HOWTORUN.md
```

---

## Quick Start

```bash
cd homework-6
pip install -r requirements.txt
python integrator.py
```

Expected output:
```
[Integrator] Processing 8 transactions...
  TXN001: SETTLED — net=1498.50 USD
  TXN002: SETTLED — net=24975.00 USD
  TXN003: SETTLED — net=9989.99 USD
  TXN004: SETTLED — net=499.50 EUR
  TXN005: BLOCKED — HIGH_FRAUD_RISK (score=7)
  TXN006: REJECTED — INVALID_CURRENCY
  TXN007: REJECTED — INVALID_AMOUNT
  TXN008: SETTLED — net=3196.80 USD

Pipeline Summary: Total=8  Settled=5  Rejected=2  Blocked=1
```

See [HOWTORUN.md](HOWTORUN.md) for full step-by-step instructions.
