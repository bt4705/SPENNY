import logging
import random

logger = logging.getLogger(__name__)

def get_account():
    return {"equity": 100_000, "balance": 100_000}

def get_position(symbol: str):
    return 0, 0.0

def place_order(symbol: str, qty: int, side: str, stop_px: float) -> str:
    logger.info(f"[BROKER] {side.upper()} {qty} {symbol} with stop {stop_px}")
    return f"local_{symbol}_{side}_{random.randint(1000,9999)}"

def update_stop(order_id: str, new_stop: float):
    logger.info(f"[BROKER] Updating stop for {order_id} to {new_stop}")
