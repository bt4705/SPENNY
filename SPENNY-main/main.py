"""
Multi-symbol trading loop with 1 m · 5 m · 60 m data.

For every symbol in SYMBOLS:
1. Fetch 1m / 5m / 60m bars
2. Apply bull-flag + checklist
3. If flat  → place a bracket order
4. If long  → tighten the stop each minute
"""

import time
from datetime import datetime, timezone
import data_fetch as F, validations as V
from zones        import demand_zones
from risk_manager import RiskManager, atr_stop
from broker       import get_account, get_position, update_stop
from hedge_bridge import execute
from agents.market_hours import status as mkt_status
from agents.patterns      import latest_bars, bull_flag

# ─── configure here ──────────────────────────────────────────────
SYMBOLS      = ["SPY", "QQQ"]        # add / remove markets
CHECK_HOURS  = (14, 20)              # UTC market window (14-20 = 10-16 ET)
LOOP_SEC     = 60                    # run every minute
ATR_MULTIPLIER = 1.0                 # 1 × ATR for break-even & trail
# ─────────────────────────────────────────────────────────────────

stop_ids: dict[str, str | None] = {s: None for s in SYMBOLS}
daily_rm: dict[str, RiskManager] = {}

# ─────────────────────────────────────────────────────────────────
def tighten_stop(df_1m, stop_id, entry_px):
    """Break-even once price ≥ entry + ATR, then trail ATR."""
    dist = atr_stop(df_1m, mult=ATR_MULTIPLIER)
    if dist is None:
        return
    px = df_1m.close.iloc[-1]
    if px - entry_px >= dist:                     # past BE trigger
        update_stop(stop_id, px - dist)

# ─────────────────────────────────────────────────────────────────
def process_symbol(sym: str):
    if not mkt_status()['is_open']:
        return
    if not bull_flag(latest_bars()):
        return

    # ①  fetch 1 m · 5 m · 60 m
    m1  = F.fetch(sym, "1m",  "2d")
    m5  = F.fetch(sym, "5m",  "7d")
    h1  = F.fetch(sym, "60m", "60d")
    if m1.empty or m5.empty or h1.empty:
        return

    # ②  manage an existing long
    qty, avg = get_position(sym)
    if qty > 0 and stop_ids[sym]:
        tighten_stop(m1, stop_ids[sym], avg)
        return                                  # skip new entry logic

    # ③  new-trade gates
    zones = demand_zones(h1)
    if not zones or not V.checklist(m5, m5, h1, h1, h1, zones):
        return

    acct   = get_account(); eq = float(acct["equity"])
    rm     = daily_rm.setdefault(sym, RiskManager(eq))
    if not rm.daily_ok(eq):
        print(f"🛑 [{sym}] daily loss hit"); return

    atr_dist = atr_stop(m1)
    if atr_dist is None:
        return
    size = rm.position_size(atr_dist, eq)
    if size == 0:
        return

    stop_px = m1.close.iloc[-1] - atr_dist
    stop_ids[sym] = execute(sym, size, "buy", stop_px)

# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        utc = datetime.now(timezone.utc)
        if CHECK_HOURS[0] <= utc.hour < CHECK_HOURS[1]:
            for s in SYMBOLS:
                process_symbol(s)
        time.sleep(LOOP_SEC)

