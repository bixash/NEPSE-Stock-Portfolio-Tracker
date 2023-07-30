from pydantic import BaseModel


class Stock(BaseModel):
    scrip: str = None
    closing_price: float = None
    company_name: str = None
    previous_closing: float = None
    trade_date: str = None
    percent_change: float = None
    difference_rs: float = None