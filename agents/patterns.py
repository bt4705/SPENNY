"""Detect bull‑flag in latest CSV inside graph-ui/data."""
import glob, os, pandas as pd, pandas_ta as ta

def _latest_csv(folder='graph-ui/data'):
    files = glob.glob(f"{folder}/*.csv")
    return max(files, key=os.path.getmtime) if files else None

def latest_bars(folder='graph-ui/data'):
    f = _latest_csv(folder)
    return pd.read_csv(f, parse_dates=['datetime']).set_index('datetime') if f else pd.DataFrame()

def bull_flag(df: pd.DataFrame) -> bool:
    if df.empty or len(df) < 40:
        return False
    slope = ta.linreg(df.close, 20).iloc[-1]
    pull  = df.close.iloc[-1] < df.close.rolling(20).max().iloc[-1] * 0.97
    return slope > 0 and pull
