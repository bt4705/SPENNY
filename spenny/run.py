import logging
import time

from .agents.market_hours import is_market_open
from .core.controller import evaluate_new_trades, update_open_trade
from .config import SYMBOLS, LOOP_SEC, STOP_UPDATE_SEC


logger = logging.getLogger(__name__)


def main():
    last_entry_time = 0.0
    logger.info("Starting trading loop")
    while True:
        try:
            now = time.time()
            if is_market_open():
                for sym in SYMBOLS:
                    update_open_trade(sym)

                if now - last_entry_time >= LOOP_SEC:
                    for sym in SYMBOLS:
                        evaluate_new_trades(sym)
                    last_entry_time = now
        except Exception:
            logger.exception("Unhandled error in trading loop")
        time.sleep(STOP_UPDATE_SEC)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
