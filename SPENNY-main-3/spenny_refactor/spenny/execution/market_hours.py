from datetime import datetime, timezone
<<<<<<<< HEAD:spenny_refactor/spenny/execution/market_hours.py
from spenny.config import MARKET_WINDOWS
========
from ..config import MARKET_WINDOWS
>>>>>>>> bd56ac96cb521d6e1bfc1fd1322b702719b9c910:spenny/agents/market_hours.py

def is_market_open():
    now = datetime.now(timezone.utc)
    if now.weekday() >= 5:
        return False
    for start, end in MARKET_WINDOWS:
        if start <= now.hour < end:
            return True
    return False
