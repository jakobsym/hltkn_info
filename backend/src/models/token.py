from calendar import c
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class Tokens(BaseModel):
    pass

class TokenHolderResponseAPI(BaseModel):
    holders: int
    timestamp: Optional[datetime]

class TokenDeployerResponseAPI(BaseModel):
    deployer_address: str

class TokenTopHoldersResponseAPI(BaseModel):
    address: str
    token_ammount: float

class TokenResponseAPI(BaseModel):
    name: str
    symbol: str
    address: str
    holders: int
    supply: int
    timestamp: Optional[datetime]
    @field_validator('timestamp')
    @classmethod
    def parse_timestamp(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

# TODO: Make different responses for different timeframes?
# response for 6hour, 12hour, etc?
class TokenHolderTSReponse(BaseModel):
    pass