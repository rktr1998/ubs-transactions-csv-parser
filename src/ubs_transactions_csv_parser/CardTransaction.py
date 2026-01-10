from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from .Currency import Currency

@dataclass(frozen=True)
class CardTransaction:
    """
    Represents a single card transaction, row, parsed from a UBS card transactions CSV file.
    """
    CSV_HEADER = "Account number;Card number;Account/Cardholder;Purchase date;Booking text;Sector;Amount;Original currency;Rate;Currency;Debit;Credit;Booked"
    account_number: str
    card_number: str
    account_cardholder: str
    purchase_date: date
    booking_text: str
    sector: str
    amount: Decimal
    original_currency: Currency
    rate: Decimal | None
    currency: Currency
    debit: Decimal | None
    credit: Decimal | None
    booked: bool

    def __hash__(self) -> int:
        return hash((self.card_number, self.purchase_date, self.amount, self.booking_text))
    
    @classmethod
    def from_csv_row(cls, row: list[str]) -> "CardTransaction":
        """
        Parse a single CSV row into a CardTransaction object.
        
        Args:
            row: A list of strings representing a parsed CSV row with 13+ columns
            
        Returns:
            CardTransaction: The parsed transaction
            
        Raises:
            ValueError: If the row has fewer than 13 columns
        """
        if len(row) < 13:
            raise ValueError(f"CSV row has an unexpected number of columns: {len(row)} (expected at least 13)")
        
        account_number = row[0]
        card_number = row[1]
        account_cardholder = row[2]
        purchase_date = date.fromisoformat(row[3])
        booking_text = row[4]
        sector = row[5]
        amount = Decimal(row[6])
        original_currency = Currency(row[7])
        rate = Decimal(row[8]) if row[8] else None
        currency = Currency(row[9])
        debit = Decimal(row[10]) if row[10] else None
        credit = Decimal(row[11]) if row[11] else None
        booked = bool(row[12])
        
        return cls(
            account_number=account_number,
            card_number=card_number,
            account_cardholder=account_cardholder,
            purchase_date=purchase_date,
            booking_text=booking_text,
            sector=sector,
            amount=amount,
            original_currency=original_currency,
            rate=rate,
            currency=currency,
            debit=debit,
            credit=credit,
            booked=booked
        )