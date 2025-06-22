import os
import asyncio
import asyncpg
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from models.token import TokenHolderResponse, TokenResponse

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

        connection_str = os.getenv("TIMESCALE_CONNECTION_STRING")
        if connection_str == None:
            logger.error("connection string incorrectly configured")
            raise RuntimeError("Database connection string is not configured")
        
        attempts = 0
        while attempts < max_retry:
            try:
                cls._connection_pool = await asyncpg.create_pool(connection_str, command_timeout=60, max_size=max_size, min_size=min_size)
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
        """ Obtains a connection from connection pool """
        if cls._connection_pool is None:
            logger.error(f"no valid connection pool established")
            raise RuntimeError("connection pool is NOT established")

        connection = None
        try:
            async with cls._connection_pool.acquire() as connection:
                yield connection # returns connection to the calling method
        except Exception as e:
            logger.error(f"unable to acqurie connection to connection pool: {str(e)}")
            raise

    @classmethod
    async def close_connection(cls):
        if cls._connection_pool is not None:
            await cls._connection_pool.close()
            cls._connection_pool = None



    """ Token related methods """
    @classmethod
    async def get_token_data(cls, token_address: str) -> TokenResponse:
        """
        - Returns the most recent holder count record + all token data for a given token_address
        """
        
        try:
            async with cls.get_connection() as conn:
                res = await conn.fetchrow('''
                    SELECT t.token_symbol, t.token_name, t.token_address, tm.holders, t.supply
                    FROM tokens t 
                    JOIN token_metrics tm ON t.id = tm.token_id 
                    WHERE t.token_address = $1
                    ORDER BY tm.holders DESC LIMIT 1;
                    ''', token_address)

                if res is None:
                    return None
                token = TokenResponse(**dict(res))
                return token
        except Exception as e:
            logger.error(f"error retrieving token data from db: {str(e)}")
            raise
                
    @classmethod
    async def get_token_holders(cls, token_address: str) -> TokenHolderResponse:
        """
        - Returns most recent holder count for a given token
        """
        try:
            async with cls.get_connection as conn:
                res = await conn.fetchrow('''
                    SELECT tm.holders FROM token_metrics tm 
                    JOIN tokens t ON tm.token_id = t.id 
                    WHERE t.token_address = $1 
                    ORDER BY tm.holders DESC LIMIT 1;
                ''', token_address)

            if res is None:
                return None

            holders = TokenHolderResponse(**dict(res))
            return holders
            
        except Exception as e:
            logger.error(f"error retrieving token holders from db: {str(e)}")
            raise
        
    @classmethod
    async def get_tokens(cls):
        """
        - Returns a list of all tokens with current timescaleDB
        """
        try:
            async with cls.get_connection() as conn:
                res = await conn.fetch('''
                SELECT t.token_symbol, 
                    t.token_name, 
                    t.token_address, 
                    tm.holders, 
                    t.supply
                FROM tokens t 
                JOIN (
                    SELECT token_id, 
                        holders,
                        ROW_NUMBER() OVER (PARTITION BY token_id ORDER BY recorded_at DESC) as rn
                    FROM token_metrics
                ) tm ON t.id = tm.token_id AND tm.rn = 1
                ORDER BY t.token_symbol;
                ''')

                if res is None:
                    return None
                return res
        except Exception as e:
            logger.error(f"error retrieving tokens from db: {str(e)}")
            raise


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
