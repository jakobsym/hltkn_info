import logging
import token
from fastapi import APIRouter, HTTPException
from backend.src.repository.postgresql import PostgresDB
from repository.hyperliquid import HyperLiquid
from models.token import TokenHolderResponse, TokenHolderResponseRoute, TokenResponseRoute, TokenResponseWithDeployer
# from models.token import Token

logger  = logging.getLogger("repository")
router = APIRouter()
hl_tokens = HyperLiquid("https://www.hyperscan.com/api/v2/tokens/")
hl_addresses = HyperLiquid("https://www.hyperscan.com/api/v2/addresses/")

@router.get("/holders/{token_address}")
async def get_token_holders(token_address: str) -> TokenHolderResponseRoute:
    holders = None
    
    try:
        holders = await PostgresDB.get_token_holders(token_address=token_address)
        if holders is None:
            holders = await hl_tokens.get_token_holders(token_address=token_address)
            if holders is None:
                raise HTTPException(status_code=404, detail="token not found")
        top_holders = await hl_tokens.get_top_5_holders(token_address=token_address)
        holder_response = TokenHolderResponseRoute(data=holders, top_holders=top_holders)
        return holder_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"server error: {str(e)}")


@router.get("/{token_address}")
async def get_token_data(token_address: str) -> TokenResponseRoute:
    token_data = None

    try:
        token_data = await PostgresDB.get_token_data(token_address=token_address)
        if token_data is None:
            token_data = await hl_tokens.get_token_info(token_address=token_address)
            if token_data is None:
                raise HTTPException(status_code=404, detail="token not found.")
        data = await hl_addresses.get_token_deployer_address(token_address=token_address)
        deployer_address = data.deployer_address if data else None # extract deployer_address

        token_data_dict = dict(token_data)
        token_data_dict['deployer'] = deployer_address

        token_response = TokenResponseRoute(items=TokenResponseWithDeployer(**token_data_dict))
        return token_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"server error: {str(e)}")
   

@router.get("/")
async def get_tokens():
    try:
        data = await PostgresDB.get_tokens()
        if data is None:
            raise HTTPException(status_code=500, detail="unable to get tokens from db")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"server error: {str(e)}")

"""
@router.get("/holders/ts/{token_address}")
async def get_token_holders_ts(token_address: str):
    # call time-series based methods via timescale
    pass
"""

