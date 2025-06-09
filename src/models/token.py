from pydantic import BaseModel

class Token(BaseModel):
    name: str
    symbol: str
    address: str
    holders: int
    supply: int