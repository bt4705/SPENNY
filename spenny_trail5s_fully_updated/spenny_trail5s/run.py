from agents.market_hours import is_market_open
from core.controller import evaluate_new_trades, update_open_trade
from config.settings import SYMBOLS, LOOP_SEC, STOP_UPDATE_SEC
import time

if __name__ == "__main__":
    last_entry_time = 0.0

    while True:
        now = time.time()
        if is_market_open():
            # Trail stops every STOP_UPDATE_SEC
            for sym in SYMBOLS:
                update_open_trade(sym)

            # Evaluate new trades every LOOP_SEC
            if now - last_entry_time >= LOOP_SEC:
                for sym in SYMBOLS:
                    evaluate_new_trades(sym)
                last_entry_time = now

        time.sleep(STOP_UPDATE_SEC)
