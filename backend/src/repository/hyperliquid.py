import logging

load_dotenv()
logger = logging.getLogger('repository')

class HyperLiquid:

    def __init__(self, base_url: str = "https://www.hyperscan.com/api/v2", rpc_url: str = ""):
        self.base_url = base_url
        self.rpc_url = rpc_url
        self.timeout = 5    

    
    async def get_top_5_holders(self, token_address: str):
        
        """
        - this request will return top holders for a given token and shows given holder amount
        curl -X 'GET' \
        'https://www.hyperscan.com/api/v2/tokens/0x47bb061C0204Af921F43DC73C7D7768d2672DdEE/holders' \
        -H 'accept: application/json'
        """
        pass

    async def get_token_deployer_address(self, token_address: str):
        """
        - this request returns deployer address
        curl -X 'GET' \
            'https://www.hyperscan.com/api/v2/addresses/0x47bb061C0204Af921F43DC73C7D7768d2672DdEE' \
            -H 
        """
        pass
    
    async def get_token_info(self, token_address: str):
        """
        - this request returns token info for a given token addresss if a token is not found in db
        curl -X 'GET' \
            'https://www.hyperscan.com/api/v2/tokens/0x47bb061C0204Af921F43DC73C7D7768d2672DdEE' \
            -H 'accept: application/json'

        """
        pass
