from pydantic import BaseModel

class Company(BaseModel):
    scrip: str = None
    company_name: str = None
    status: str = None
    sector: str = None
    instrument: str = None
    email: str = None
    url: str = None