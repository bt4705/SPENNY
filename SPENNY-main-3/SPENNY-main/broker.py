# AI/broker.py
"""
Thin wrapper around Alpaca’s REST API.
Handles:  *submit bracket*  *update stop*  *position lookup*
"""

import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

load_dotenv()  # pulls ALPACA_KEY / ALPACA_SECRET from .env

BASE_PAPER = "https://paper-api.alpaca.markets"
BASE_LIVE  = os.getenv("ALPACA_LIVE_BASE", BASE_PAPER)   # stays paper until you set the env

api = tradeapi.REST(
    os.getenv("ALPACA_KEY"),
    os.getenv("ALPACA_SECRET"),
    base_url=BASE_LIVE,
    api_version="v2"
)

# ----------------------------------------------------------------------
def get_account():
    return api.get_account()._raw

def get_position(symbol):
    """
    Returns (qty, avg_entry_price) as floats.
    If flat → (0, 0)
    """
    try:
        pos = api.get_position(symbol)
        return float(pos.qty), float(pos.avg_entry_price)
    except tradeapi.rest.APIError:
        return 0.0, 0.0

# ----------------------------------------------------------------------
def place_order(symbol, qty, side, stop_px):
    """
    Market entry + attached stop-loss (bracket class).
    Returns the stop-order ID so the caller can later tighten it.
    """
    o = api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type="market",
        time_in_force="gtc",
        order_class="bracket",
        stop_loss={"stop_price": round(stop_px, 2)}
    )
    stop_id = o.legs[1].id    # [0] = take‐profit (none here), [1] = stop
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    print(f"{ts}  🚀 Sent {side.upper()} {qty} {symbol}  | stop @ {stop_px:.2f}")
    return stop_id

def update_stop(order_id: str, new_stop: float):
    """
    Tighten existing stop-loss.  Alpaca replaces the child leg in-place.
    """
    api.replace_order(order_id, stop_price=round(new_stop, 2))
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"{ts}  🔧  Moved stop to {new_stop:.2f}")