import datetime as dt, os, pandas as pd
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
api = tradeapi.REST(
    os.getenv("ALPACA_KEY"),
    os.getenv("ALPACA_SECRET"),
    base_url=os.getenv("ALPACA_LIVE_BASE", "https://paper-api.alpaca.markets"),
    api_version="v2"
)

def fetch(symbol: str, timeframe: str, lookback: str) -> pd.DataFrame:
    end   = dt.datetime.utcnow()
    start = end - pd.Timedelta(lookback)
    bars  = api.get_bars(symbol, timeframe, start.isoformat(), end.isoformat()).df
    bars.index = pd.to_datetime(bars.index)
    return bars[['open', 'high', 'low', 'close']]

