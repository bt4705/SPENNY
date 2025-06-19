from datetime import datetime, timezone
from ..config import MARKET_WINDOWS

def is_market_open():
    now = datetime.now(timezone.utc)
    if now.weekday() >= 5:
        return False
    for start, end in MARKET_WINDOWS:
        if start <= now.hour < end:
            return True
    return False
