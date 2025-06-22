import logging

load_dotenv()
logger = logging.getLogger('repository')

class HyperLiquid:
    _rpc_url = ""
    _hyperscan_base_url = "https://www.hyperscan.com/api/v2"
    
    """

    - contains methods that interact directly with hyperevm using web3py
    and calls to hyperevm specific APIs

    - this request returns deployer address
        curl -X 'GET' \
            'https://www.hyperscan.com/api/v2/addresses/0x47bb061C0204Af921F43DC73C7D7768d2672DdEE' \
            -H 'accept: application/json'

    - this request returns token info for a given token addresss if a token is not found in db
    curl -X 'GET' \
        'https://www.hyperscan.com/api/v2/tokens/0x47bb061C0204Af921F43DC73C7D7768d2672DdEE' \
        -H 'accept: application/json'

    """

    
    pass


