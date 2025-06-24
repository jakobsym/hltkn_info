import logging
import requests
from datetime import datetime
from models.token import TokenHolderResponse, TokenResponse, TokenDeployerResponseAPI,TokenTopHoldersResponseAPI

logger = logging.getLogger('repository')

class HyperLiquid:

    def __init__(self, base_url: str = "https://www.hyperscan.com/api/v2", rpc_url: str = None):
        self.base_url = base_url
        self.rpc_url = rpc_url
        self.session = requests.Session()
        self.timeout = 5    

    async def get_token_info(self, token_address: str) -> TokenResponse:
        # base_url = https://www.hyperscan.com/api/v2/tokens/
        url = f"{self.base_url}{token_address}"
        
        try:
            res = self.session.get(
                url=url,
                timeout=self.timeout,
                headers={'accept':'application/json'}
            )
            if res.status_code == 200:
                data = res.json()
                return TokenResponseAPI(
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
        # base_url = https://www.hyperscan.com/api/v2/tokens/
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
    
    async def get_top_5_holders(self, token_address: str) -> list[TokenTopHoldersResponseAPI]:
        # base_url = https://www.hyperscan.com/api/v2/tokens/
        url = f"{self.base_url}{token_address}"
        top_holders = []
        try:
            res = self.session.get(
                url=url,
                timeout=self.timeout,
                headers={'accept':'application/json'}
            )
            if res.status_code == 200:
                data = res.json()
                # TODO: Maybe make into a function, as more logic should be associated
                # I.E: Only non-protocol addresses?
                for holder in data['items'][:5]:
                    top_holders.append(TokenTopHoldersResponseAPI(address=holder['address']['hash'], amount=holder['address']['value']))
            return top_holders
        except Exception as e:
            logger.error(f"error making API call to: {url}\n {str(e)}")
            raise

    async def get_token_deployer_address(self, token_address: str) -> TokenDeployerResponseAPI:
        # base_url = https://www.hyperscan.com/api/v2/addresses/
        url = f"{self.base_url}{token_address}"
        try:
            res = self.session.get(
                url=url,
                timeout=self.timeout,
                headers={'accept':'application/json'}
            )
            if res.status_code() == 200:
                data = res.json()
                return TokenDeployerResponseAPI(deployer_address=data['creator_address_hash'])    
        except Exception as e:
            logger.error(f"error making API call to: {url}\n {str(e)}")
            raise