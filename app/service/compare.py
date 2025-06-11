from app.models import QuoteRequest, QuoteResponse, SingleQuote
from app.db import conn, c
from app.service.fetcher import BaseFetcher, OdosFetcher, OneInchFetcher
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RoutingStrategy:

    async def _get_quote(self, fetcher: BaseFetcher, req: QuoteRequest) -> tuple[SingleQuote, int]:
        """
        Helper function to fetch a quote and measure latency.
        """
        import time
        start = time.perf_counter()
        quote = await fetcher.fetch(req)
        latency = int((time.perf_counter() - start) * 1000)
        return quote, latency



    async def compare_quotes(self, req: QuoteRequest) -> QuoteResponse:
        odos_fetch = OdosFetcher()
        one_fetch = OneInchFetcher()

        (odos_q, odos_lat) = await self._get_quote(odos_fetch, req)
        (one_q, one_lat) = await self._get_quote(one_fetch, req)
        odos_response = SingleQuote(
            amountOut=str(odos_q),
            latencyMs=odos_lat,
            route="odos"
        )
        oneinch_response = SingleQuote(
            amountOut=str(one_q),
            latencyMs=one_lat,
            route="1inch"
        )
        logging.info(f"Fetched quotes: Odos={odos_q}, 1inch={one_q}")
        logging.info(f"Latencies: Odos={odos_lat}ms, 1inch={one_lat}ms")

        best = 'odos' if int(odos_q) >= int(one_q) else '1inch'
        c.execute(
            '''INSERT INTO history(tokenIn, tokenOut, amountIn,
                odosOut, oneinchOut, best, odosLatency, oneinchLatency)
            VALUES (?,?,?,?,?,?,?,?)''',
            (
                str(req.tokenIn), str(req.tokenOut), str(req.amount),
                str(odos_q), str(one_q), str(best),
                str(odos_lat), str(one_lat)
            )
        )
        conn.commit()

        return QuoteResponse(input=req, quotes={'odos': odos_response, '1inch': oneinch_response}, best=best)

    async def batch_compare(self, body):
        results = []
        for req in body.requests:
            res = await self.compare_quotes(req)
            results.append(res)
        return results
    
