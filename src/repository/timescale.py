from contextlib import contextmanager
import os
class TimescaleDB:
    _instance = None
    _connection_pool = None

    # ensure only 1 connection pool is ever established
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TimescaleDB, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def init_pool(cls):
        """ check if connection active before establishing connection pool """
        pass

    @classmethod
    @contextmanager
    def get_connection(cls):
        """ Get connection from pool"""
        pass

    