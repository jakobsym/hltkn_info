import logging
import uvicorn
from config.logging_config import config_logging
from fastapi import FastAPI

# init logging
config_logging()
logger = logging.getLogger('api')

app = FastAPI(title="hltkn_api", description="API for timescaleDB", version="0.0.1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)