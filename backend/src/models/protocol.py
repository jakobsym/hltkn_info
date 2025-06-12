from datetime import date
from typing import Optional
from pydantic import BaseModel


class Protocol(BaseModel):
    name: str
    tvl: float = Optional
    total_liq: float = Optional

class ProtocolTVLResponse(BaseModel):
    name: str
    tvl: float
    timestamp: datetime

class ProtocolLiquidityResponse(BaseModel):
    name: str
    liquidty: float
    timestamp: datetime

class ProtocolTVLTSResponse(BaseModel):
    pass

class ProtocolLiquidityTSResponse(BaseModel):
    pass