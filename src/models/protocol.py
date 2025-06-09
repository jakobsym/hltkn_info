from typing import Optional
from pydantic import BaseModel


class Protocol(BaseModel):
    name: str
    tvl: float = Optional
    total_liq: float = Optional
