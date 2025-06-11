import time
from web3 import Web3

# Decorator to measure latency
def timed(func):
    async def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = await func(*args, **kwargs)
        end = time.perf_counter_ns()
        latency = (end - start) // 1_000_000
        return result, latency
    return wrapper

# Estimate gas using Web3 eth_estimateGas
async def estimate_gas(client, tx_params):
    try:
        gas = await client.eth.estimate_gas(tx_params)
        return gas
    except Exception:
        return None

# Apply slippage to raw amountOut
def apply_slippage(raw: int, slippage_pct: float) -> int:
    return int(raw * (1 - slippage_pct / 100))