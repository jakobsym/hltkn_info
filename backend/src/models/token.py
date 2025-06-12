from pydantic import BaseModel
from datetime import date

class Tokens(BaseModel):
    pass

class TokenHolderResponse(BaseModel):
    name: str
    symbol: str
    address: str
    holders: int
    timestamp: date

class TokenResponse(BaseModel):
    name: str
    symbol: str
    address: str
    holders: int
    supply: int
    timestamp: date

# TODO: Make different responses for different timeframes?
# response for 6hour, 12hour, etc?
class TokenHolderTSReponse(BaseModel):
    pass