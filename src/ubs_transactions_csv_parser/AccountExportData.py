import csv
from datetime import date, time
from decimal import Decimal
from pathlib import Path
from typing import List
from dataclasses import dataclass
from .AccountTransaction import AccountTransaction
from .Currency import Currency

@dataclass(frozen=True)
class AccountExportData:
    account_number: str
    iban: str
    from_date: date
    until_date: date
    opening_balance: Decimal
    closing_balance: Decimal
    valued_in: Currency
    number_of_transactions: int
    transactions: List[AccountTransaction]

    @classmethod
    def from_csv(cls, path: Path) -> "AccountExportData":
        """
        Parse a UBS transaction CSV file to return a AccountExportData object, which contains the CSV metadata
        and a list of AccountTransaction objects.

        Beware that the UBS transactions CSV file is actually an invalid CSV: it has a first section with some metadata,
        then an empty line, and finally a second section with actual CSV data. As in the example below:

        Account number:;1234 12345678.12;
        IBAN:;CH20 0011 2233 4455 6677 B;
        From:;2025-01-01;
        Until:;2025-12-31;
        Opening balance:;1234.12;
        Closing balance:;12345.12;
        Valued in:;CHF;
        Numbers of transactions in this period:;365;

        Trade date;Trade time;Booking date;Value date;Currency;Debit;Credit;Individual amount;Balance;AccountTransaction no.;Description1;Description2;Description3;Footnotes;
        2025-01-01;00:11:22;2025-01-01;2025-01-01;CHF;-137.00;;;1370.17;4825794DP1572581029;"John Doe;Weissstrasse 19; 4001 Basel; CH";Standing order;"Reference no. ABB: 56 34523 88997 22445 25398 09132; Reason for payment: 01.01.2025 Langstrasse 137 Zurich; Account no. IBAN: CH45 4678 2354 6874 1253 9; Costs: Standing order domestic; AccountTransaction no. 4825794DP1572581029";;
        ...
        """
        with path.open() as f:
            lines = [line.strip() for line in f]
        
        if len(lines) < 10:
            raise ValueError("CSV file is too short to contain required metadata and transactions")

        # Parse metadata
        account_number = lines[0].split(";")[1]
        iban = lines[1].split(";")[1]
        from_date = date.fromisoformat(lines[2].split(";")[1])
        until_date = date.fromisoformat(lines[3].split(";")[1])
        opening_balance = Decimal(lines[4].split(";")[1])
        closing_balance = Decimal(lines[5].split(";")[1])
        valued_in = Currency(lines[6].split(";")[1])
        number_of_transactions = int(lines[7].split(";")[1])

        # Expect empty line
        if lines[8]:
            raise ValueError("Expected an empty line between metadata and transactions")
        
        # Check CSV header
        if lines[9] != AccountTransaction.CSV_HEADER:
            raise ValueError("Unexpected CSV header")

        # Parse transactions
        transactions = []
        for line in lines[10:]:
            reader = csv.reader([line], delimiter=';', quotechar='"')
            row = next(reader)
            transaction = AccountTransaction.from_csv_row(row)
            transactions.append(transaction)
        
        if len(transactions) != number_of_transactions:
            raise ValueError("Number of parsed transactions does not match the metadata")

        return cls(
            account_number=account_number,
            iban=iban,
            from_date=from_date,
            until_date=until_date,
            opening_balance=opening_balance,
            closing_balance=closing_balance,
            valued_in=valued_in,
            number_of_transactions=number_of_transactions,
            transactions=transactions,
        )
