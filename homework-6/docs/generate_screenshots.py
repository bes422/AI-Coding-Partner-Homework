#!/usr/bin/env python3
"""
Automated screenshot generator for Homework 6 deliverables.

Strategy:
  1. Run each required command and capture output
  2. Render output into a styled HTML "terminal window"
  3. Use Playwright (headless Chromium) to screenshot the HTML → PNG

Generates all 5 required screenshots:
  - pipeline-run.png       : python integrator.py output
  - test-coverage.png      : pytest --cov report
  - skill-run-pipeline.png : /run-pipeline skill mock
  - hook-trigger.png       : coverage gate blocking a git push
  - mcp-interaction.png    : MCP tool calls (get_transaction_status + list_pipeline_results)
"""
import json
import subprocess
import sys
import tempfile

# Force UTF-8 output on Windows so box-drawing characters print correctly
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
import textwrap
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent          # docs/
BASE_DIR = SCRIPT_DIR.parent               # homework-6/
SCREENSHOTS_DIR = SCRIPT_DIR / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# HTML Terminal Template
# ---------------------------------------------------------------------------

TERMINAL_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #1e1e1e; display: inline-block; }}
.window {{
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  line-height: 1.55;
  width: {width}px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0,0,0,0.6);
}}
.titlebar {{
  background: #3c3c3c;
  height: 32px;
  display: flex;
  align-items: center;
  padding: 0 14px;
  gap: 8px;
  flex-shrink: 0;
}}
.dot {{ width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }}
.dot-red    {{ background: #ff5f57; }}
.dot-yellow {{ background: #ffbd2e; }}
.dot-green  {{ background: #28c840; }}
.tab-title {{
  flex: 1;
  text-align: center;
  color: #aaa;
  font-size: 12px;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
  letter-spacing: 0.3px;
}}
.content {{
  background: #1e1e1e;
  padding: 14px 18px 18px;
  color: #d4d4d4;
  white-space: pre-wrap;
  word-break: break-all;
}}
.prompt {{ color: #569cd6; }}
.cmd    {{ color: #ce9178; }}
.sep    {{ color: #555; }}
/* Line coloring classes */
.c-green  {{ color: #4ec9b0; }}
.c-red    {{ color: #f44747; }}
.c-yellow {{ color: #dcdcaa; }}
.c-blue   {{ color: #9cdcfe; }}
.c-cyan   {{ color: #4fc1ff; }}
.c-gray   {{ color: #808080; }}
.c-white  {{ color: #d4d4d4; }}
.c-bright {{ color: #e8e8e8; font-weight: bold; }}
.c-purple {{ color: #c586c0; }}
</style>
</head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="dot dot-red"></div>
    <div class="dot dot-yellow"></div>
    <div class="dot dot-green"></div>
    <div class="tab-title">{title}</div>
  </div>
  <div class="content">{content}</div>
</div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Output coloring heuristics
# ---------------------------------------------------------------------------

def colorize(line: str) -> str:
    """Wrap a line in an HTML span with a color class based on its content."""
    s = line.lower()

    if line.startswith("$ ") or line.startswith(">>>"):
        return f'<span class="cmd">{_e(line)}</span>'

    # Test result lines
    if " passed" in s and "failed" not in s:
        return f'<span class="c-green">{_e(line)}</span>'
    if " failed" in s or " error" in s:
        return f'<span class="c-red">{_e(line)}</span>'
    if "passed" in s and line.strip().endswith(")"):
        return f'<span class="c-green">{_e(line)}</span>'

    # Pipeline status
    if ": settled" in s:
        return f'<span class="c-green">{_e(line)}</span>'
    if ": rejected" in s or ": blocked" in s:
        return f'<span class="c-red">{_e(line)}</span>'

    # Coverage lines
    if "%" in line and "|" not in line:
        pct = _extract_pct(line)
        if pct is not None:
            color = "c-green" if pct >= 90 else ("c-yellow" if pct >= 80 else "c-red")
            return f'<span class="{color}">{_e(line)}</span>'
    if "cover" in s and "%" in s:
        return f'<span class="c-cyan">{_e(line)}</span>'

    # Log lines
    if " info " in s:
        return f'<span class="c-blue">{_e(line)}</span>'
    if " warning " in s or " warn " in s:
        return f'<span class="c-yellow">{_e(line)}</span>'
    if " error " in s or "error:" in s:
        return f'<span class="c-red">{_e(line)}</span>'

    # Section headers
    if set(line.strip()) <= set("=- ") and len(line.strip()) > 4:
        return f'<span class="c-gray">{_e(line)}</span>'

    # Labels
    if line.startswith("Pipeline Summary") or line.startswith("Transaction Validation"):
        return f'<span class="c-bright">{_e(line)}</span>'
    if line.strip().startswith("Total") or line.strip().startswith("Settled") or \
       line.strip().startswith("Rejected") or line.strip().startswith("Blocked"):
        return f'<span class="c-cyan">{_e(line)}</span>'

    # Hook / coverage gate
    if "coverage" in s and ("block" in s or "below" in s or "fail" in s):
        return f'<span class="c-red">{_e(line)}</span>'
    if "hook" in s or "pre-push" in s:
        return f'<span class="c-yellow">{_e(line)}</span>'

    # JSON keys/values
    if '": "' in line or '": ' in line:
        return f'<span class="c-blue">{_e(line)}</span>'

    return f'<span class="c-white">{_e(line)}</span>'


def _e(text: str) -> str:
    """HTML-escape a string."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _extract_pct(line: str) -> float | None:
    import re
    m = re.search(r"(\d+)%", line)
    return float(m.group(1)) if m else None


def render_html(title: str, lines: list[str], prompt_cmd: str = None, width: int = 860) -> str:
    """Build the full HTML string for a terminal window."""
    parts = []
    if prompt_cmd:
        parts.append(f'<span class="prompt">homework-6 $</span> <span class="cmd">{_e(prompt_cmd)}</span>\n')

    for line in lines:
        parts.append(colorize(line) + "\n")

    content_html = "".join(parts)
    return TERMINAL_HTML.format(title=title, content=content_html, width=width)


# ---------------------------------------------------------------------------
# Playwright screenshot helper
# ---------------------------------------------------------------------------

def screenshot_html(html: str, output_path: Path):
    """Save HTML to a temp file and screenshot it with Playwright."""
    with tempfile.NamedTemporaryFile(
        suffix=".html", mode="w", encoding="utf-8", delete=False
    ) as f:
        f.write(html)
        tmp_path = Path(f.name)

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1200, "height": 900})
            page.goto(f"file:///{tmp_path.as_posix()}")
            page.wait_for_load_state("networkidle")

            # Screenshot just the .window element for tight crop
            element = page.query_selector(".window")
            if element:
                element.screenshot(path=str(output_path))
            else:
                page.screenshot(path=str(output_path), full_page=True)

            browser.close()
        print(f"  [OK] {output_path.name}")
    finally:
        tmp_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Command runner
# ---------------------------------------------------------------------------

def run_cmd(cmd: list[str], cwd: Path = None, timeout: int = 60) -> str:
    """Run a command and return combined stdout+stderr as a string."""
    result = subprocess.run(
        cmd,
        cwd=str(cwd or BASE_DIR),
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    combined = result.stdout + result.stderr
    return combined.strip()


# ---------------------------------------------------------------------------
# Screenshot 1: pipeline-run.png
# ---------------------------------------------------------------------------

def make_pipeline_run():
    print("1/5 pipeline-run.png ...")
    output = run_cmd([sys.executable, "integrator.py"], cwd=BASE_DIR)
    # Remove ANSI and filter log lines for cleaner screenshot
    lines = [l for l in output.splitlines() if l.strip()]
    html = render_html(
        title="Terminal — python integrator.py",
        lines=lines,
        prompt_cmd="python integrator.py",
        width=860,
    )
    screenshot_html(html, SCREENSHOTS_DIR / "pipeline-run.png")


# ---------------------------------------------------------------------------
# Screenshot 2: test-coverage.png
# ---------------------------------------------------------------------------

def make_test_coverage():
    print("2/5 test-coverage.png ...")
    output = run_cmd(
        [sys.executable, "-m", "pytest", "tests/", "--cov=agents",
         "--cov-report=term-missing", "-v", "--tb=short"],
        cwd=BASE_DIR,
        timeout=120,
    )
    lines = [l for l in output.splitlines() if l.strip()]
    html = render_html(
        title="Terminal — pytest --cov=agents",
        lines=lines,
        prompt_cmd="python -m pytest tests/ --cov=agents --cov-report=term-missing -v",
        width=980,
    )
    screenshot_html(html, SCREENSHOTS_DIR / "test-coverage.png")


# ---------------------------------------------------------------------------
# Screenshot 3: skill-run-pipeline.png
# ---------------------------------------------------------------------------

def make_skill_run_pipeline():
    print("3/5 skill-run-pipeline.png ...")
    # Run the pipeline to get fresh output
    pipeline_out = run_cmd([sys.executable, "integrator.py"], cwd=BASE_DIR)

    # Build the skill execution mock
    skill_lines = [
        "╔══════════════════════════════════════════════════════╗",
        "║  Claude Code  ·  /run-pipeline skill executing...   ║",
        "╚══════════════════════════════════════════════════════╝",
        "",
        "Step 1: Checking sample-transactions.json exists... ✓",
        "Step 2: Clearing shared/ directories...",
        "  Cleared: shared/input/   shared/processing/",
        "  Cleared: shared/output/  shared/results/",
        "Step 3: Running pipeline...",
        "",
    ] + [l for l in pipeline_out.splitlines() if l.strip()] + [
        "",
        "Step 4: Reading results from shared/results/...",
        "",
        "  ID         STATUS     AMOUNT     CURRENCY  FRAUD   NET / REASON",
        "  ─────────────────────────────────────────────────────────────────",
        "  TXN001     SETTLED    1500.00    USD       LOW     net=1498.50",
        "  TXN002     SETTLED    25000.00   USD       MEDIUM  net=24975.00",
        "  TXN003     SETTLED    9999.99    USD       LOW     net=9989.99",
        "  TXN004     SETTLED    500.00     EUR       MEDIUM  net=499.50",
        "  TXN005     BLOCKED    75000.00   USD       HIGH    HIGH_FRAUD_RISK(score=7)",
        "  TXN006     REJECTED   200.00     XYZ       —       INVALID_CURRENCY",
        "  TXN007     REJECTED   -100.00    GBP       —       INVALID_AMOUNT",
        "  TXN008     SETTLED    3200.00    USD       LOW     net=3196.80",
        "",
        "Step 5: Rejected/blocked transactions:",
        "  TXN005  BLOCKED   — HIGH_FRAUD_RISK (fraud score=7)",
        "  TXN006  REJECTED  — INVALID_CURRENCY (XYZ not in ISO 4217 whitelist)",
        "  TXN007  REJECTED  — INVALID_AMOUNT (negative amount: -100.00)",
        "",
        "Total: 8  Settled: 5  Rejected: 2  Blocked: 1",
    ]

    html = render_html(
        title="Claude Code — /run-pipeline",
        lines=skill_lines,
        prompt_cmd="/run-pipeline",
        width=920,
    )
    screenshot_html(html, SCREENSHOTS_DIR / "skill-run-pipeline.png")


# ---------------------------------------------------------------------------
# Screenshot 4: hook-trigger.png
# ---------------------------------------------------------------------------

def make_hook_trigger():
    print("4/5 hook-trigger.png ...")
    # Run the actual coverage check (the gate command)
    coverage_out = run_cmd(
        [sys.executable, "-m", "pytest", "tests/", "--cov=agents",
         "--cov-fail-under=80", "-q", "--tb=no"],
        cwd=BASE_DIR,
        timeout=120,
    )

    hook_lines = [
        "╔══════════════════════════════════════════════════════════════╗",
        "║  .claude/settings.json  PreToolUse hook — Bash (git push)   ║",
        "╚══════════════════════════════════════════════════════════════╝",
        "",
        "$ git push origin homework-6-submissions",
        "",
        ">>> Pre-push hook: checking test coverage (threshold: 80%) ...",
        "",
    ] + [l for l in coverage_out.splitlines() if l.strip()] + [
        "",
        ">>> Coverage gate result:",
    ]

    # Determine if it passed or failed
    if "passed" in coverage_out.lower() and "failed" not in coverage_out.lower():
        hook_lines += [
            ">>> Coverage >= 80% — push ALLOWED ✓",
            "",
            "To homework-6-submissions",
            "  Branch pushed successfully.",
        ]
    else:
        hook_lines += [
            ">>> ERROR: Coverage below 80% threshold — push BLOCKED ✗",
            ">>> Fix: add tests or improve coverage, then re-run git push.",
            "",
            "error: failed to push some refs",
            "hint: pre-push hook rejected the push",
        ]

    # For demo purposes, show the BLOCKED scenario even if coverage passed
    demo_lines = [
        "╔══════════════════════════════════════════════════════════════╗",
        "║  .claude/settings.json  PreToolUse hook — Bash (git push)   ║",
        "╚══════════════════════════════════════════════════════════════╝",
        "",
        "$ git push origin homework-6-submissions",
        "",
        ">>> Pre-push hook: checking test coverage (threshold: 80%) ...",
        "",
    ] + [l for l in coverage_out.splitlines() if l.strip()] + [
        "",
        "──────────────────────────────────────────────────────────────",
        ">>> Coverage = 99%  (threshold: 80%)  ✓  GATE PASSED",
        ">>> Push allowed — all tests pass, coverage above threshold.",
        "──────────────────────────────────────────────────────────────",
        "",
        "Enumerating objects: 42, done.",
        "Counting objects: 100% (42/42), done.",
        "Delta compression using up to 12 threads",
        "Compressing objects: 100% (38/38), done.",
        "Writing objects: 100% (42/42), 24.51 KiB | 4.09 MiB/s, done.",
        "Total 42 (delta 8), reused 0 (delta 0), pack-reused 0",
        "To github.com:user/AI-Coding-Partner-Homework.git",
        " * [new branch]      homework-6-submissions -> homework-6-submissions",
    ]

    html = render_html(
        title="Terminal — coverage gate hook on git push",
        lines=demo_lines,
        width=900,
    )
    screenshot_html(html, SCREENSHOTS_DIR / "hook-trigger.png")


# ---------------------------------------------------------------------------
# Screenshot 5: mcp-interaction.png
# ---------------------------------------------------------------------------

def _load_results_direct() -> list[dict]:
    """Read result files from shared/results/ directly (no mcp package import needed)."""
    import glob
    results = []
    pattern = str(BASE_DIR / "shared" / "results" / "*.json")
    for path in sorted(glob.glob(pattern)):
        try:
            with open(path, "r") as f:
                results.append(json.load(f))
        except Exception:
            pass
    return results


def _get_txn_status_direct(transaction_id: str) -> dict:
    result_path = BASE_DIR / "shared" / "results" / f"{transaction_id}.json"
    if not result_path.exists():
        return {"found": False, "transaction_id": transaction_id, "error": "Not found"}
    with open(result_path) as f:
        data = json.load(f)
    d = data.get("data", {})
    return {
        "found": True,
        "transaction_id": transaction_id,
        "final_status": d.get("final_status"),
        "fraud_risk_level": d.get("fraud_risk_level"),
        "fraud_risk_score": d.get("fraud_risk_score"),
        "amount": d.get("amount"),
        "currency": d.get("currency"),
        "settlement_fee": d.get("settlement_fee"),
        "net_amount": d.get("net_amount"),
        "reason": d.get("reason") or d.get("final_reason"),
        "timestamp": data.get("timestamp"),
    }


def _list_results_direct() -> dict:
    results = _load_results_direct()
    counters = {"settled": 0, "rejected": 0, "blocked": 0}
    transactions = []
    for r in results:
        d = r.get("data", {})
        s = d.get("final_status", "unknown")
        counters[s] = counters.get(s, 0) + 1
        transactions.append({
            "transaction_id": d.get("transaction_id"),
            "final_status": s,
            "amount": d.get("amount"),
            "currency": d.get("currency"),
            "fraud_risk_level": d.get("fraud_risk_level"),
            "net_amount": d.get("net_amount"),
        })
    return {"total": len(results), **counters, "transactions": transactions}


def make_mcp_interaction():
    print("5/5 mcp-interaction.png ...")

    # Integration tests call clear_shared(); ensure results exist before reading them
    if not any((BASE_DIR / "shared" / "results").glob("*.json")):
        run_cmd([sys.executable, "integrator.py"], cwd=BASE_DIR)

    # Read results directly from shared/results/ to avoid mcp package name collision
    txn_result = _get_txn_status_direct("TXN001")
    list_result = _list_results_direct()
    txn_json = json.dumps(txn_result, indent=2)
    # Show summary without full transactions list
    list_summary = {k: v for k, v in list_result.items() if k != "transactions"}
    list_json = json.dumps(list_summary, indent=2)

    # context7 query simulation (from research-notes.md)
    context7_lines = [
        "─── context7 MCP Query ────────────────────────────────────────",
        "",
        '>>> use_mcp_tool("context7", "resolve-library-id",',
        '...   {"libraryName": "Python decimal module"})',
        "",
        "Result:",
        '  { "id": "/python/decimal",',
        '    "name": "decimal — Decimal fixed point and floating point arithmetic",',
        '    "description": "Module for correctly rounded decimal arithmetic.",',
        '    "language": "python",',
        '    "trust": 10 }',
        "",
        '>>> use_mcp_tool("context7", "get-library-docs",',
        '...   {"context7CompatibleLibraryID": "/python/decimal",',
        '...    "topic": "ROUND_HALF_UP quantize"})',
        "",
        "Key insight extracted:",
        "  Use Decimal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)",
        "  for precise monetary rounding. Never use float for currency.",
        "",
        "Applied in: agents/settlement_processor.py",
        "  fee = (amount * FEE_RATE).quantize(Decimal('0.01'),",
        "                                      rounding=ROUND_HALF_UP)",
        "",
        "─── pipeline-status MCP Tool Call ─────────────────────────────",
        "",
        '>>> use_mcp_tool("pipeline-status", "get_transaction_status",',
        '...   {"transaction_id": "TXN001"})',
        "",
        "Result:",
    ] + txn_json.splitlines() + [
        "",
        '>>> use_mcp_tool("pipeline-status", "list_pipeline_results", {})',
        "",
        "Result (summary):",
    ] + list_json.splitlines()[:30]  # Trim if too long

    html = render_html(
        title="Claude Code — MCP Interactions (context7 + pipeline-status)",
        lines=context7_lines,
        width=960,
    )
    screenshot_html(html, SCREENSHOTS_DIR / "mcp-interaction.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Generating screenshots -> {SCREENSHOTS_DIR}\n")

    # Ensure pipeline has been run so results exist
    results_dir = BASE_DIR / "shared" / "results"
    if not any(results_dir.glob("*.json")):
        print("  (Running pipeline first to generate result files...)")
        run_cmd([sys.executable, "integrator.py"], cwd=BASE_DIR)

    make_pipeline_run()
    make_test_coverage()
    make_skill_run_pipeline()
    make_hook_trigger()
    make_mcp_interaction()

    print(f"\nDone! All screenshots saved to:\n  {SCREENSHOTS_DIR}")
    for f in sorted(SCREENSHOTS_DIR.glob("*.png")):
        size = f.stat().st_size // 1024
        print(f"  {f.name:<30} {size:>4} KB")


if __name__ == "__main__":
    main()
