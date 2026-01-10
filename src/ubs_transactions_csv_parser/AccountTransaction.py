from dataclasses import dataclass
from datetime import date, time
from decimal import Decimal
from .Currency import Currency

@dataclass(frozen=True)
class AccountTransaction:
    """
    Represents a single transaction, row, parsed from a UBS transactions CSV file.
    """
    CSV_HEADER = "Trade date;Trade time;Booking date;Value date;Currency;Debit;Credit;Individual amount;Balance;Transaction no.;Description1;Description2;Description3;Footnotes;"
    trade_date: date
    trade_time: time | None
    booking_date: date
    value_date: date
    currency: Currency
    debit: Decimal | None
    credit: Decimal | None
    individual_amount: Decimal | None
    balance: Decimal
    transaction_no: str
    description1: str
    description2: str
    description3: str
    footnotes: str

    def __hash__(self) -> int:
        return hash(self.transaction_no)
    
    @classmethod
    def from_csv_row(cls, row: list[str]) -> "AccountTransaction":
        """
        Parse a single CSV row into an AccountTransaction object.
        
        Args:
            row: A list of strings representing a parsed CSV row with 14+ columns
            
        Returns:
            AccountTransaction: The parsed transaction
            
        Raises:
            ValueError: If the row has fewer than 14 columns
        """
        if len(row) < 14:
            raise ValueError(f"CSV row has an unexpected number of columns: {len(row)} (expected at least 14)")
        
        trade_date = date.fromisoformat(row[0])
        trade_time = time.fromisoformat(row[1]) if row[1] else None
        booking_date = date.fromisoformat(row[2])
        value_date = date.fromisoformat(row[3])
        currency = Currency(row[4])
        debit = Decimal(row[5]) if row[5] else None
        credit = Decimal(row[6]) if row[6] else None
        individual_amount = Decimal(row[7]) if row[7] else None
        balance = Decimal(row[8])
        transaction_no = row[9]
        description1 = row[10]
        description2 = row[11]
        description3 = row[12]
        footnotes = row[13]

        return cls(
            trade_date=trade_date,
            trade_time=trade_time,
            booking_date=booking_date,
            value_date=value_date,
            currency=currency,
            debit=debit,
            credit=credit,
            individual_amount=individual_amount,
            balance=balance,
            transaction_no=transaction_no,
            description1=description1,
            description2=description2,
            description3=description3,
            footnotes=footnotes
        )
