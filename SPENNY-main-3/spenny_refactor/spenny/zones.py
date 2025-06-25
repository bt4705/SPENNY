import pandas as pd

def demand_zones(df: pd.DataFrame) -> list:
    if len(df) < 30:
        return []
    lows = df['Low'].rolling(5).min()
    zones = []
    for i in range(5, len(df)):
        if df['Low'].iloc[i] == lows.iloc[i]:
            zones.append(df['Low'].iloc[i])
    unique = []
    for z in zones:
        if all(abs(z - u) > 0.5 for u in unique):
            unique.append(z)
    return unique
