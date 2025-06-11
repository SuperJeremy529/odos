import pytest
import asyncio
from unittest.mock import AsyncMock
from app.models import QuoteRequest
from app.service.compare import RoutingStrategy

@pytest.mark.asyncio
async def test_compare_quotes(monkeypatch):
    # Arrange
    req = QuoteRequest(
        tokenIn="0x0000000000000000000000000000000000000000",
        tokenOut="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        amount=10**18
    )

    mock_odos = AsyncMock(return_value="3050000000")
    mock_oneinch = AsyncMock(return_value="3040000000")

    monkeypatch.setattr("app.service.fetcher.OdosFetcher.fetch", mock_odos)
    monkeypatch.setattr("app.service.fetcher.OneInchFetcher.fetch", mock_oneinch)

    strategy = RoutingStrategy()

    # Act
    response = await strategy.compare_quotes(req)

    # Assert
    assert response.best == "odos"
    assert response.quotes["odos"].amountOut == "3050000000"
    assert response.quotes["1inch"].amountOut == "3040000000"
    assert response.quotes["odos"].latencyMs >= 0
    assert response.quotes["1inch"].latencyMs >= 0