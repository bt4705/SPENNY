import pandas as pd
import logging
import yfinance as yf

logger = logging.getLogger(__name__)

def fetch_data(symbol: str):
    """Fetch 1m, 5m, and 60m candles for a symbol."""
    try:
        m1 = yf.download(tickers=symbol, interval="1m", period="2d", progress=False)
        m5 = yf.download(tickers=symbol, interval="5m", period="7d", progress=False)
        h1 = yf.download(tickers=symbol, interval="60m", period="60d", progress=False)
        if m1.empty or m5.empty or h1.empty:
            logger.warning(f"No data for {symbol}")
            return None
        return m1, m5, h1
    except Exception as e:
        logger.error(f"Data fetch error for {symbol}: {e}")
        return None
