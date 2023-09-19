from pydantic import BaseModel



class Transaction(BaseModel):
    scrip: str = None
    transaction_date: str = None
    credit_quantity: int = None
    debit_quantity: int = None
    balance_after_transaction: int = None
    history_description: str = None
    unit_price: float = None