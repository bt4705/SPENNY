import logging

try:
    from hedgefund import trade_once
except ImportError:  # pragma: no cover - optional dependency
    trade_once = None

from ..execution.broker import place_order

logger = logging.getLogger(__name__)

def execute(symbol: str, qty: int, side: str, stop_px: float) -> str:
    if qty <= 0 or stop_px is None:
        logger.error(f"Invalid trade params: qty={qty}, stop_px={stop_px}")
        return "INVALID"
    if trade_once:
        try:
            oid = trade_once(symbol=symbol, qty=qty, side=side, stop=stop_px)
            logger.info(f"Hedge fund executed order ⇒ ID {oid}")
            return oid
        except Exception as err:
            logger.warning(f"Hedge fund failed, using local broker: {err}")

    return place_order(symbol, qty, side, stop_px)
