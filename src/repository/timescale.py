import os
import asyncio
import asyncpg
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger('repository')

# designed in a way that only a single connection_pool, or instance of class ever exists
# through the use of cls-'class' variables and __new__
# denoting methods with @classmethod allow for class level changes to be made to cls variables
class TimescaleDB:
    _instance = None
    _connection_pool = None

    # ensure only 1 connection pool is ever established
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TimescaleDB, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    async def init_pool(cls, max_retry: int = 3, retry_delay: float = 5.0, min_size:int = 1, max_size:int  = 10):
        """ check if connection active before establishing connection pool """
        # pool already established
        if cls._connection_pool is not None:
            return

        attempts = 0
        while attempts < max_retry:
            try:
                cls._connection_pool = await asyncpg.create_pool(os.getenv("TIMESCALE_CONNECTION_STRING"), command_timeout=60, max_size=max_size, min_size=min_size)
                return
            except Exception as e:
                attempts += 1
                if attempts > max_retry:
                    logger.error(f"Maximum retries reached for initializing a connection pool: {str(e)}")
                    cls._connection_pool = None
                    raise
                else:
                    logger.info(f"retying in {retry_delay} seconds...")
                    await asyncio.sleep(delay=retry_delay)

    @classmethod
    @asynccontextmanager
    async def get_connection(cls):
        """ Get connection from pool"""
        if cls._connection_pool is None:
            logger.error(f"no valid connection pool established: {str(e)}")
            raise RuntimeError("connection pool is NOT established")

        connection = None
        try:
            async with cls._connection_pool.acquire() as connection:
                yield connection # returns connection to the calling method
        except Exception as e:
            logger.error("unable to acqurie connection to connection pool")
            raise

    @classmethod
    async def close_connection(cls):
        if cls._connection_pool is not None:
            await cls._connection_pool.close()
            cls._connection_pool = None



    """ Token related method """
    @classmethod
    async def get_token_holders(cls, token_address: str):
        pass
    
    @classmethod
    async def get_token_data(cls, token_address: str):
        pass

    @classmethod
    async def get_tokens(cls):
        pass



    """ Protocol related methods """
    @classmethod
    async def get_protocols(cls):
        pass

    @classmethod    
    async def get_protocol_tvl(cls, protocol_name: str):
        pass

    @classmethod
    async def get_protocol_liq(cls, protocol_name: str):
        pass 
