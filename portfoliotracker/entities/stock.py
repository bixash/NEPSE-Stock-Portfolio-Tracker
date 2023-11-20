from pydantic import BaseModel


class Stock(BaseModel):
    scrip: str = None
    previous_closing: float = None
    trade_date: str = None
    closing_price: float = None
    difference_rs: float = None
    percent_change: float = None