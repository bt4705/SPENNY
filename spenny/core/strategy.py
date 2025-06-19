import pandas as pd

def is_bull_flag(df: pd.DataFrame) -> bool:
    if len(df) < 20:
        return False
    recent = df.tail(20)
    close = recent['Close']
    volume = recent['Volume']
    uptrend = close.iloc[-1] > close.iloc[0] * 1.01
    pullback = close.iloc[-1] < close.max() * 0.98
    volume_surge = volume.iloc[-1] > volume.mean()
    return uptrend and pullback and volume_surge

def passes_checklist(m5, h1, zones) -> bool:
    if len(m5) < 10 or len(h1) < 10:
        return False
    trend_ok = h1['Close'].iloc[-1] > h1['Close'].mean()
    zone_close = any(abs(h1['Close'].iloc[-1] - z) < 1.0 for z in zones)
    vol_ok = m5['Volume'].iloc[-1] > m5['Volume'].mean()
    return trend_ok and zone_close and vol_ok
