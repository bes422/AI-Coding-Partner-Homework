# How to Run — AI-Powered Banking Pipeline

## Prerequisites

- Python 3.11+
- Node.js 18+ (for context7 MCP)
- Git

---

## Step 1 — Install Dependencies

```bash
cd homework-6
pip install -r requirements.txt
```

This installs `fastmcp` (for the MCP server) and `pytest`/`pytest-cov` (for tests).

---

## Step 2 — Run the Full Pipeline

```bash
cd homework-6
python integrator.py
```

The integrator will:
1. Create `shared/input/`, `shared/processing/`, `shared/output/`, `shared/results/` if they don't exist
2. Clear any existing files from those directories
3. Process all 8 transactions from `sample-transactions.json`
4. Print a live status line for each transaction
5. Print a summary: total, settled, rejected, blocked

Result files will be in `shared/results/` (one JSON file per transaction).

---

## Step 3 — Validate Transactions (Dry Run)

To validate transactions without running the full pipeline:

```bash
cd homework-6
python agents/transaction_validator.py --dry-run
```

This prints a validation report showing which transactions would pass or fail validation, with rejection reasons — without writing any files.

---

## Step 4 — Run Tests

```bash
cd homework-6
python -m pytest tests/ -v
```

To run with coverage report:

```bash
cd homework-6
python -m pytest tests/ --cov=agents --cov-report=term-missing
```

Target: ≥ 90% coverage. The pre-push hook blocks pushes if coverage falls below 80%.

---

## Step 5 — Use Claude Code Skills

### Run the full pipeline via slash command:
In Claude Code, type:
```
/run-pipeline
```
This runs the pipeline end-to-end and shows a summary table.

### Validate transactions via slash command:
In Claude Code, type:
```
/validate-transactions
```
This validates all transactions in dry-run mode and shows a formatted table.

---

## Step 6 — Start the MCP Server

```bash
cd homework-6
python mcp/server.py
```

The FastMCP server exposes:
- `get_transaction_status("TXN001")` — query a single transaction result
- `list_pipeline_results()` — get a summary of all results
- `pipeline://summary` — resource with full pipeline run summary

Configure it in Claude Code via `homework-6/mcp.json`.

---

## Step 7 — View Results

All final results are in `homework-6/shared/results/`:

```bash
# List result files
ls homework-6/shared/results/

# View a specific result
cat homework-6/shared/results/TXN001.json
```

Each result file contains the full message with `final_status`, fraud scores, settlement fee, and net amount.

---

## Coverage Gate Hook

A pre-push hook is configured in `.claude/settings.json`. When you run `git push`, it automatically checks that test coverage is ≥ 80%. If coverage is below the threshold, the push is blocked with an error message.

To test the hook manually:
```bash
cd homework-6
python -m pytest tests/ --cov=agents --cov-fail-under=80
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'fastmcp'` | Run `pip install fastmcp` |
| `sample-transactions.json not found` | Run from `homework-6/` directory |
| Coverage below 80% on push | Check `python -m pytest tests/ --cov=agents --cov-report=term-missing` |
| MCP server not responding | Ensure `fastmcp` is installed: `pip show fastmcp` |
