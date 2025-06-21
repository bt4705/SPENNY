# AI/validations.py
import pandas as pd
import pandas_ta as ta

# ------------------ low-level helpers ------------------------
def bullish_structure(df: pd.DataFrame) -> bool:
    ma200 = ta.sma(df["close"], 200).iloc[-1]
    macd  = ta.macd(df["close"]).iloc[-1]["MACDh_12_26_9"]
    return df["close"].iloc[-1] > ma200 and macd > 0

def body_percent(df: pd.DataFrame, n: int = 1) -> float:
    """Candle body ÷ full range (0…1)."""
    c = df["close"].iloc[-n]
    o = df["open"].iloc[-n]
    rng = df["high"].iloc[-n] - df["low"].iloc[-n] + 1e-9
    return abs(c - o) / rng

# ------------------ Type-1 and Type-2 ------------------------
def type1_validation(df15: pd.DataFrame) -> bool:
    """Break-of-Structure + FVG fill + small-body (≤ 50 %)."""
    swing_hi = df15["high"].iloc[-20:-5].max()
    bos      = df15["close"].iloc[-1] > swing_hi

    gap_mid  = (df15["high"].iloc[-3] + df15["low"].iloc[-2]) / 2
    gap_fill = df15["low"].iloc[-1] < gap_mid < df15["high"].iloc[-1]

    small_body = body_percent(df15, 1) < 0.5
    return bos and gap_fill and small_body

def type2_validation(df15: pd.DataFrame) -> bool:
    """Liquidity sweep of prior low + momentum candle (≥ 70 % body)."""
    sweep = df15["low"].iloc[-1] < df15["low"].iloc[-5:-1].min()
    mit   = body_percent(df15, 1) > 0.7
    return sweep and mit

# ------------------ higher-level checks ----------------------
def tapped_demand_zone(df15: pd.DataFrame, zones: list[float], tol=0.002) -> bool:
    lo = df15["low"].iloc[-1]
    return any(abs(lo - z) / z < tol for z in zones)

def ma_alignment(m5: pd.DataFrame, fast=9, slow=21) -> bool:
    return ta.sma(m5["close"], fast).iloc[-1] > ta.sma(m5["close"], slow).iloc[-1]

# ------------------ master checklist -------------------------
def checklist(m5, m15, h1, h4, d1, zones) -> bool:
    # 4-hour or Daily bias
    if not (bullish_structure(h4) or bullish_structure(d1)):
        return False
    # 1-hour bias
    if not bullish_structure(h1):
        return False
    # 15-minute context
    if not (
        bullish_structure(m15)
        and tapped_demand_zone(m15, zones)
        and (type1_validation(m15) or type2_validation(m15))
    ):
        return False
    # 5-minute trigger
    if not (bullish_structure(m5) and ma_alignment(m5)):
        return False
    return True

