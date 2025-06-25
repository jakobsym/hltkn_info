from calendar import c
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class TokenDeployerResponseAPI(BaseModel):
    """
    - Token deployer address response from API
    """
    deployer_address: str

class TokenHolderResponse(BaseModel):
    """
    - Holder count response from (TimescaleDB or API)
    """
    holders: int
    timestamp: Optional[datetime]

class TokenResponse(BaseModel):
    """
    - Basic token info response from (TimescaleDB or API)
    """
    name: str
    symbol: str
    address: str
    holders: int
    supply: int
    timestamp: Optional[datetime] = None
    @field_validator('timestamp')
    @classmethod
    def parse_timestamp(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

class TokenResponseWithDeployer(TokenResponse):
    """
    - TokenResponse subclass which includes a deployer field
     """
    deployer: str

class TokenTopHoldersResponseAPI(BaseModel):
    """
    - Top token holders for a given token from API
    """
    address: str
    token_amount: float

class TokenHolderResponseRoute(BaseModel):
    """
    - Combined holder count + top holders response for Routes
    """
    items: TokenHolderResponse
    top_holders: Optional[list[TokenTopHoldersResponseAPI]]
   
class TokenResponseRoute(BaseModel):
    """
    - Full token info with top holders and deployer response for Routes
    """
    items: TokenResponseWithDeployer
    # - Not sure if top_holders should be included here
    #top_holders: list[TokenTopHoldersResponseAPI]
