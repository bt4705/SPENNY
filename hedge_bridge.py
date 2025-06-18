"""Route trades through hedgefund engine; fall back to local broker."""
from hedgefund import trade_once
from broker    import place_order

def execute(symbol: str, qty: int, side: str, stop_px: float):
    try:
        oid = trade_once(symbol=symbol, qty=qty, side=side, stop=stop_px)
        print(f"hedgefund executed order ⇒ id {oid}")
        return oid
    except Exception as err:
        print("hedgefund error, using local broker:", err)
        return place_order(symbol, qty, side, stop_px)

