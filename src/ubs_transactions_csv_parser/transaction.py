from dataclasses import dataclass
from datetime import date, time
from decimal import Decimal
from .currency import Currency

@dataclass(frozen=True)
class Transaction:
    """
    Represents a single transaction, row, parsed from a UBS transactions CSV file.
    """
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
