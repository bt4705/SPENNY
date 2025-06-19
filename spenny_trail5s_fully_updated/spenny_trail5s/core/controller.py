from core.data import fetch_data
from core.strategy import is_bull_flag, passes_checklist
from core.risk import atr_stop, RiskManager
from core.zones import demand_zones
from core.ingestion import ingest_all_strategies
from execution.broker import get_account, get_position, update_stop
from execution.hedge_bridge import execute
from agents.llama_agent import suggest_stop
from config.settings import ATR_MULTIPLIER, USE_AI_STOP

stop_ids = {}
daily_rm = {}
_ingested = False

def evaluate_new_trades(symbol):
    global _ingested
    if not _ingested:
        ingest_all_strategies()
        _ingested = True

    data = fetch_data(symbol)
    if not data:
        return
    m1, m5, h1 = data

    if not is_bull_flag(m1):
        return

    qty, _ = get_position(symbol)
    if qty > 0:
        return

    zones = demand_zones(h1)
    if not zones or not passes_checklist(m5, h1, zones):
        return

    acct = get_account()
    equity = float(acct["equity"])
    rm = daily_rm.setdefault(symbol, RiskManager(equity))
    if not rm.daily_ok(equity):
        print(f"🛑 [{symbol}] daily loss limit reached")
        return

    stop_dist = atr_stop(m1)
    if not stop_dist:
        return

    size = rm.position_size(stop_dist, equity)
    if size == 0:
        return

    entry_price = m1["Close"].iloc[-1]
    stop_price = entry_price - stop_dist
    stop_ids[symbol] = execute(symbol, size, "buy", stop_price)

def update_open_trade(symbol):
    qty, _ = get_position(symbol)
    oid = stop_ids.get(symbol)
    if qty <= 0 or not oid:
        return

    data = fetch_data(symbol)
    if not data:
        return
    m1, _, _ = data
    current = m1["Close"].iloc[-1]

    if USE_AI_STOP:
        ai_stop = suggest_stop(symbol, current)
        new_stop = ai_stop if ai_stop else current - atr_stop(m1, mult=ATR_MULTIPLIER)
    else:
        new_stop = current - atr_stop(m1, mult=ATR_MULTIPLIER)

    # Only update if new_stop improves (higher stop for long)
    update_stop(oid, new_stop)
