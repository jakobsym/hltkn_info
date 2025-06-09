from fastapi import APIRouter
#from models.protocol import Protocol

router = APIRouter()

@router.get("/")
async def get_protocols():
    # return all protocols and their most recent 'TODAY' data
    pass

@router.get("/tvl/{protocol_name}")
async def get_tvl(protocol_name: str):
    # return most recent tvl
    pass

@router.get("/liq/{protocol_name}")
async def get_liq(protocol_name: str):
    # return most recent liquidity usd
    pass


@router.get("/tvl/ts/{protocol_name}")
async def get_tvl_ts(protocol_name: str):
    # return timeseries representation of tvl data
    pass


@router.get("/liq/ts/{protocol_name}")
async def get_liq_ts(protocol_name: str):
    # return timeseries representation of liquidity data
    return {}