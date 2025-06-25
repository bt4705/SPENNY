# AI/zones.py
import pandas as pd
import numpy as np
import pandas_ta as ta

def last_swing_lows(df_h1: pd.DataFrame, depth: int = 3) -> pd.Series:
    """Return lows where each low is the lowest in ±depth bars."""
    lows = df_h1["low"]
    mask = (lows.shift(depth) > lows) & (lows.shift(-depth) > lows)
    for d in range(1, depth):
        mask &= (lows.shift(d) > lows) & (lows.shift(-d) > lows)
    return lows[mask]

def demand_zones(df_h1: pd.DataFrame, max_zones: int = 2) -> list[float]:
    """
    Cluster most-recent swing-lows (H1) into ≤ max_zones price bands.
    Returns sorted list of zone prices (low → high).
    """
    lows = last_swing_lows(df_h1).sort_index(ascending=False)  # newest first
    if lows.empty:
        return []

    zones = []
    tol = np.median(df_h1["close"].tail(200)) * 0.002  # 0.2 % band width

    for price in lows.head(20):        # look back up to 20 swings
        placed = False
        for i, z in enumerate(zones):
            if abs(price - z) < tol:   # within the band → merge
                zones[i] = (z + price) / 2
                placed = True
                break
        if not placed:
            zones.append(price)
        if len(zones) == max_zones:
            break

    return sorted(zones)

