"""Temporary stub until you wire real order-placement logic."""

def trade_once(symbol: str, qty: int, side: str, stop: float):
    print(
        f"[hedgefund stub] would place {side.upper()} {qty} {symbol} "
        f"with stop @ {stop:.2f}"
    )
    # TODO: implement real trading call and return order-ID
    return None

