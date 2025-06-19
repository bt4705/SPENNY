import pandas as pd

class RiskManager:
    def __init__(self, starting_equity: float):
        self.starting_equity = starting_equity
        self.max_daily_loss = 0.03

    def daily_ok(self, current_equity: float) -> bool:
        return current_equity >= self.starting_equity * (1 - self.max_daily_loss)

    def position_size(self, stop_dist: float, equity: float, risk_per_trade: float = 0.01) -> int:
        risk_amt = equity * risk_per_trade
        if stop_dist <= 0:
            return 0
        return int(risk_amt / stop_dist)

def atr_stop(df: pd.DataFrame, mult: float = 1.0):
    if len(df) < 14:
        return None
    df = df.copy()
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = abs(df['High'] - df['Close'].shift())
    df['L-PC'] = abs(df['Low'] - df['Close'].shift())
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(14).mean()
    return round(df['ATR'].iloc[-1] * mult, 2)
