from fastapi import FastAPI, HTTPException, Query
from app.models import QuoteRequest, BatchRequest, QuoteResponse
from app.service.compare import RoutingStrategy

app = FastAPI(title="Odos vs 1inch Benchmark with Slippage & Gas")

@app.get("/benchmark", response_model=QuoteResponse)
async def benchmark(
    tokenIn: str = Query(...),
    tokenOut: str = Query(...),
    amount: int = Query(...),
):
    req = QuoteRequest(tokenIn=tokenIn, tokenOut=tokenOut, amount=amount)
    try:
        routingStrategy = RoutingStrategy()
        return await routingStrategy.compare_quotes(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/benchmark/batch", response_model=list[QuoteResponse])
async def benchmark_batch(body: BatchRequest):
    routingStrategy = RoutingStrategy()
    if not body.requests:
        raise HTTPException(status_code=400, detail="No requests provided in batch")
    return await routingStrategy.batch_compare(body)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Service is running"}



