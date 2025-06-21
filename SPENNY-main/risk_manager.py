# AI/risk_manager.py
import pandas as pd
import pandas_ta as ta

MAX_RISK_PCT   = 0.01   # 1 % equity per trade
DAILY_STOP_PCT = 0.05   # 5 % daily drawdown

class RiskManager:
    def __init__(self, start_equity: float):
        self.day_start_equity = start_equity

    # --- sizing --------------------------------------------------------
    def position_size(self, stop_distance: float, equity: float) -> int:
        risk_dollars = equity * MAX_RISK_PCT
        qty = int(risk_dollars / stop_distance)
        return max(qty, 1)

    # --- daily loss guard ---------------------------------------------
    def daily_ok(self, current_equity: float) -> bool:
        draw = (self.day_start_equity - current_equity) / self.day_start_equity
        return draw < DAILY_STOP_PCT

# --- ATR-based stop distance ------------------------------------------
def atr_stop(df_m5: pd.DataFrame, mult: float = 1.5) -> float:
    atr_val = ta.atr(df_m5["high"], df_m5["low"], df_m5["close"], length=14).iloc[-1]
    return float(atr_val * mult)