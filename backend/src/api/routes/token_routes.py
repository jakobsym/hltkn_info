import logging
from fastapi import APIRouter, HTTPException
from repository.timescale import TimescaleDB
#from repository.hyperliquid import HyperLiquid
# from models.token import Token

logger  = logging.getLogger("repository")
router = APIRouter()
#hl_tokens = HyperLiquid("https://www.hyperscan.com/api/v2/tokens/")
#hl_addresses = HyperLiquid("https://www.hyperscan.com/api/v2/addresses/")


@router.get("/holders/{token_address}")
async def get_token_holders(token_address: str):
    holders = None
    # call timescale method for fetching holders
    try:
        holders = await TimescaleDB.get_token_holders(token_address=token_address)
        if holders is None:
            """
            holders = await hl_tokens.get_token_info(token_address=token_address)
            if holders is None:
                raise HTTPException(status_code=404, detail="Token not found")
            """
        return holders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"server error: {str(e)}")
   

@router.get("/")
async def get_tokens():
    try:
        data = await TimescaleDB.get_tokens()
        if data is None:
            raise HTTPException(status_code=500, detail="unable to get tokens from db")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"server error: {str(e)}")


@router.get("/{token_address}")
async def get_token_data(token_address: str):
    # return all data for a given token
    # if not found in timescale, calls hyperscan or similar API
    try:
        token_data = await TimescaleDB.get_token_data(token_address=token_address)
        if token_data is None:
            raise HTTPException(status_code=404, detail="token not found.")
        return token_data
    except Exception as e:
        raise HTTPException(status_code=500, detail="server error")


"""
@router.get("/holders/ts/{token_address}")
async def get_token_holders_ts(token_address: str):
    # call time-series based methods via timescale
    pass
"""

