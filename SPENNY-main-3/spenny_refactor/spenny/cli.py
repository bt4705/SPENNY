"""
CLI Entrypoint: trading loop for Spenny.
"""
import time
import logging
from spenny.config import settings
from spenny.execution.market_hours import is_market_open
from spenny.core.controller import evaluate_new_trades, update_open_trade

def main():
    logging.basicConfig(level=settings.log_level)
    logger = logging.getLogger(__name__)
    last_entry_time = 0.0
    try:
        while True:
            now = time.time()
            if is_market_open():
                # Update open trades
                for sym in settings.symbols:
                    update_open_trade(sym)
                # Evaluate new trades
                if now - last_entry_time >= settings.loop_sec:
                    for sym in settings.symbols:
                        evaluate_new_trades(sym)
                    last_entry_time = now
            time.sleep(settings.stop_update_sec)
    except Exception:
        logger.exception("Error in trading loop")
        raise

if __name__ == "__main__":
    main()
