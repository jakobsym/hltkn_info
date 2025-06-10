import logging
import uvicorn
from config.logging_config import config_logging
from fastapi import FastAPI
from api.protocol_routes import router as protocols_router
from api.token_routes import router as tokens_router
from repository.timescale import TimescaleDB

# init logging
config_logging()
logger = logging.getLogger('api')

async def lifespan(app: FastAPI):
    try:
        await TimescaleDB.init_pool()
        logger.info("DB connection pool established")
        yield
    except Exception as e:
        logger.error(f"error init connection pool: {str(e)}")
    finally:
        await TimescaleDB.close_connection()
        logger.info("DB connection pool is closed")
        
app = FastAPI(title="hltkn_api", description="API interfacing timescaleDB data", version="0.0.1", lifespan=lifespan)
app.include_router(protocols_router, prefix="/protocol", tags=["protocols"])
app.include_router(tokens_router, prefix="/token", tags=["tokens"])

#TODO: WIP
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)