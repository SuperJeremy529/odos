import httpx
from app.models import QuoteRequest
from web3 import Web3
from app.utils import timed
from app.models import SingleQuote
from abc import ABC, abstractmethod
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ODOS_URL = 'https://api.odos.xyz/sor/quote/v2'
ONEINCH_URL = 'https://api.1inch.dev/swap/v6.1/1/quote'
ONEINCH_API_KEY = 'I8S9Quw8X3xFL1lXqJR595Aj2JJp14eH'


class BaseFetcher(ABC):
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=5)
        self.w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_KEY'))
    
    @abstractmethod
    async def fetch(self, req: QuoteRequest):
        raise NotImplementedError("Subclasses should implement this method.")

    @timed
    async def _get_quote(self, req: QuoteRequest):
        raw, route = await self.fetch(req)
        quote = SingleQuote(
            amountOut=str(raw),
            latencyMs=0,
            route=route
        )
        return quote




class OdosFetcher(BaseFetcher):
    async def fetch(self, req: QuoteRequest):
        params = {
            "chainId": 1,
            "inputTokens": [{
                'tokenAddress': req.tokenIn.lower(),
                'amount': str(req.amount)
            }],
            "outputTokens": [{
                'tokenAddress': req.tokenOut.lower(),
                'proportion': 1.0
            }],
        }
        resp = await self.client.post(ODOS_URL, json=params)
        data = resp.json()
        return int(data['outAmounts'][0])

class OneInchFetcher(BaseFetcher):
    async def fetch(self, req: QuoteRequest):

        headers = {
            "Authorization": "Bearer {}".format(ONEINCH_API_KEY),
            "Content-Type": "application/json"
        }
        params = {
            "src": req.tokenIn.lower(),
            "dst": req.tokenOut.lower(),
            "amount": str(req.amount)
        }

        resp = await self.client.get(ONEINCH_URL, headers=headers, params=params)
        data = resp.json()
        return int(data['dstAmount'])
