from pydantic import BaseModel
from datetime import date
from typing import Optional

class Tokens(BaseModel):
    pass

class TokenHolderResponse(BaseModel):
    holders: int
    timestamp: Optional[date]

class TokenResponse(BaseModel):
    name: str
    symbol: str
    address: str
    holders: int
    supply: int
    timestamp: Optional[date]

# TODO: Make different responses for different timeframes?
# response for 6hour, 12hour, etc?
class TokenHolderTSReponse(BaseModel):
    pass