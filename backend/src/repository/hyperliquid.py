import logging
import requests
from datetime import datetime
from models.token import TokenHolderResponse, TokenResponse

logger = logging.getLogger('repository')

class HyperLiquid:

    def __init__(self, base_url: str = "https://www.hyperscan.com/api/v2", rpc_url: str = ""):
        self.base_url = base_url
        self.rpc_url = rpc_url
        self.session = requests.Session()
        self.timeout = 5    

    async def get_token_info(self, token_address: str) -> TokenResponse:
        url = f"{self.base_url}{token_address}"
        
        try:
            res = self.session.get(
                url=url,
                timeout=self.timeout,
                headers={'accept':'application/json'}
            )
            if res.status_code == 200:
                data = res.json()
                return TokenResponse(
                    name=data['name'], 
                    symbol=data['symbol'],
                    address=token_address,
                    holders=int(data['holders']),
                    supply=int(data['total_supply']),
                    timestamp=datetime.now()
                )
        except Exception as e:
            logger.error(f"error making API call to: {url}\n {str(e)}")
            raise
        
    
    async def get_token_holders(self, token_address: str) -> TokenHolderResponse:
        url = f"{self.base_url}{token_address}"
        
        try:
            res = self.session.get(
                url=url,
                timeout=self.timeout,
                headers={'accept':'application/json'}
            )
            if res.status_code == 200:
                data = res.json()
                return TokenHolderResponse(holders=data['holders'], timestamp=datetime.now())
        except Exception as e:
            logger.error(f"error making API call to: {url}\n {str(e)}")
            raise
    

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

