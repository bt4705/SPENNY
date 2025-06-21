import openai
import logging
from ..config import LLAMA_API_KEY

openai.api_key = LLAMA_API_KEY
logger = logging.getLogger(__name__)

def suggest_stop(symbol: str, recent_close: float) -> float:
    prompt = (
        f"Given the recent close price of {{recent_close}} for {{symbol}}, "
        "provide a single float for a safe stop-loss price slightly below the current price."
    ).format(symbol=symbol, recent_close=recent_close)
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )
        text = resp.choices[0].message.content.strip()
        return float(text)
    except Exception as e:
        logger.error(f"LLAMA stop suggestion failed: {e}")
        return None
