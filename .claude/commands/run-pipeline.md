Run the multi-agent banking pipeline end-to-end.

## Steps

1. Check that `homework-6/sample-transactions.json` exists. If not, report an error and stop.

2. Clear all JSON files from the shared directories:
   - `homework-6/shared/input/`
   - `homework-6/shared/processing/`
   - `homework-6/shared/output/`
   - `homework-6/shared/results/`

3. Run the full pipeline from the `homework-6/` directory:
   ```
   cd homework-6 && python integrator.py
   ```

4. After the pipeline completes, read all JSON files from `homework-6/shared/results/` and show a summary table:

   | Transaction ID | Final Status | Amount | Currency | Fraud Risk | Net Amount / Reason |
   |---------------|-------------|--------|----------|------------|---------------------|
   | TXN001        | SETTLED      | 1500.00 | USD     | LOW        | net=1498.50         |
   | ...           | ...          | ...     | ...     | ...        | ...                 |

5. Report any transactions that were **rejected** (reason) or **blocked** (fraud score) separately, grouped by outcome.

6. Show final counts: Total processed, Settled, Rejected, Blocked.
