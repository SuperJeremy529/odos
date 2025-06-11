from pydantic import BaseModel, Field
from typing import List, Optional

class QuoteRequest(BaseModel):
    tokenIn: str
    tokenOut: str
    amount: int

class SingleQuote(BaseModel):
    amountOut: str
    latencyMs: int
    route: Optional[str]

class QuoteResponse(BaseModel):
    input: QuoteRequest
    quotes: dict[str, SingleQuote]
    best: str

class BatchRequest(BaseModel):
    requests: List[QuoteRequest]