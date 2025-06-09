from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_tokens():
    # idk how much use
    # call all timescale based methods that return
    # all tokens and their given symbols etc
    pass

@router.get("/holders/{token_address}")
async def get_token_holders(token_address: str):
    # call timescale method for fetching holders
    pass

@router.get("/holders/ts/{token_address}")
async def get_token_holders_ts(token_address: str):
    # call time-series based methods via timescale
    pass

@router.get("/{token_addres}")
async def get_token_data(token_addres: str):
    # return all data for a given token
    pass

