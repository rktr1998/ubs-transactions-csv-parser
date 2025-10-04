from ubs_transactions_csv_parser import CsvExportData, Transaction
from pathlib import Path

# read test CSV file data
test_csv = CsvExportData.from_path(Path("src/tests/test_transactions.csv"))
assert len(test_csv.transactions) == 3
print(f"Found {len(test_csv.transactions)} transactions for account number: {test_csv.account_number}")

# check if the transactions are unique
assert len(test_csv.transactions) == len(set(test_csv.transactions))
print("All transactions are unique.")

# TODO: implement some tests...
