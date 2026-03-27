Validate all transactions in `sample-transactions.json` without running the full pipeline.

## Steps

1. Check that `homework-6/sample-transactions.json` exists. If not, report an error and stop.

2. Run the validator in dry-run mode from the `homework-6/` directory:
   ```
   cd homework-6 && python agents/transaction_validator.py --dry-run
   ```

3. Parse the output and display a formatted validation report table:

   | Transaction ID | Amount    | Currency | Valid | Reason            |
   |---------------|-----------|----------|-------|-------------------|
   | TXN001        | 1500.00   | USD      | True  | OK                |
   | TXN006        | 200.00    | XYZ      | False | INVALID_CURRENCY  |
   | TXN007        | -100.00   | GBP      | False | INVALID_AMOUNT    |
   | ...           | ...       | ...      | ...   | ...               |

4. Show summary statistics:
   - **Total transactions**: N
   - **Valid**: N
   - **Invalid**: N
   - **Rejection reasons breakdown**: grouped by reason code

5. Note: This command only validates — it does NOT run the fraud detector or settlement processor, and does NOT write to `shared/` directories.
