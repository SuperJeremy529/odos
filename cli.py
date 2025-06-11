import typer
import json
import asyncio
from app.models import QuoteRequest, BatchRequest
from app.service.compare import RoutingStrategy

app = typer.Typer(help="Odos vs 1inch Benchmark CLI")

@app.command()
def run(token_in: str, token_out: str, amount: int):
    """
    Fetch and compare a single quote from Odos and 1inch.
    """
    req = QuoteRequest(
        tokenIn=token_in,
        tokenOut=token_out,
        amount=amount,
    )
    strategy = RoutingStrategy()
    result = asyncio.run(strategy.compare_quotes(req))
    typer.echo(result.json(indent=2))

@app.command()
def batch(file: str):
    """
    Read a JSON file of requests and perform batch benchmark.
    File format: [{"tokenIn":..., "tokenOut":..., "amount":..., "slippagePct":...}, ...]
    """
    data = json.load(open(file))
    reqs = [QuoteRequest(**item) for item in data]
    body = BatchRequest(requests=reqs)
    strategy = RoutingStrategy()
    results = asyncio.run(strategy.batch_compare(body))
    typer.echo(json.dumps([r.dict() for r in results], indent=2))

if __name__ == "__main__":
    app()