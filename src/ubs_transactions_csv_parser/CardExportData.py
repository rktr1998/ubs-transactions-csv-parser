import csv
from dataclasses import dataclass
from typing import List
from pathlib import Path
from .CardTransaction import CardTransaction

@dataclass
class CardExportData:
    """
    Parse a UBS card transaction CSV file to return a CardExportData object, which contains a list of CardTransaction objects.
    Beware that the UBS transactions CSV file is actually an invalid CSV: we discard the first line. It looks like this:

    sep=;
    Account number;Card number;Account/Cardholder;Purchase date;Booking text;Sector;Amount;Original currency;Rate;Currency;Debit;Credit;Booked
    3344 4554 5566;4455 6666 5544 3332;JOHN DOE;9.2.2019;ESPACO DO NORDESTE       JOAO PESSOA  BRA;Art supplies;3.0;BRL;0.151327;CHF;0.46;;9.2.2019
    3344 4554 5566;4455 6666 5544 3332;JOHN DOE;9.2.2019;MercadinhoAquario        IPOJUCA      BRA;Package stores - beer;5.0;BRL;0.153527;CHF;0.77;;9.2.2019
    ...
    """
    transactions: List[CardTransaction]

    @classmethod
    def from_csv(cls, path: Path) -> "CardExportData":
        """
        Parse a UBS card transaction CSV file to return a CardExportData object.
        """
        with path.open(encoding="utf-8") as f:
            lines = [line.strip() for line in f]
        
        # Verify header
        if len(lines) < 2:
            raise ValueError("CSV file is too short")
        
        if lines[1] != CardTransaction.CSV_HEADER:
            raise ValueError("Unexpected CSV header")
        
        # Skip first line (sep=;) and header line
        data_lines = lines[2:]
        
        transactions = []
        for line in data_lines:
            if line.strip():
                reader = csv.reader([line], delimiter=';', quotechar='"')
                row = next(reader)
                transaction = CardTransaction.from_csv_row(row)
                transactions.append(transaction)
        
        return cls(transactions=transactions)