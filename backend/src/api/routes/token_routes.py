import logging
from fastapi import APIRouter, HTTPException
from repository.timescale import TimescaleDB
# from models.token import Token

logger  = logging.getLogger("repository")
router = APIRouter()

@router.get("/holders/{token_address}")
async def get_token_holders(token_address: str):
    # call timescale method for fetching holders
    try:
        holders = await TimescaleDB.get_token_holders(token_address=token_address)
        if holders is None:
            #TODO: Try calling API directly instead, if not successful return 400 error
            raise HTTPException(status_code=404, detail="Token not found")
        return holders
    except Exception as e:
        raise HTTPException(status_code=500, detail="server error")
   

@router.get("/")
async def get_tokens():
    try:
        data = await TimescaleDB.get_tokens()
        if data is None:
            raise HTTPException(status_code=500, detail="unable to get tokens from db")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail="server error")


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

