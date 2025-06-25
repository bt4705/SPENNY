"""Unified runner for the API, SPENNY bot and optional hedge fund agent."""
import logging
import threading

try:
    from backend.api import app as api_app
except Exception:  # pragma: no cover - optional dependency
    api_app = None

try:
    from hedge_fund.main import main as hedge_main
except Exception:  # pragma: no cover - optional dependency
    hedge_main = None

from spenny.run import main as spenny_main


def run_api():
    if not api_app:
        logging.warning("API component not available")
        return
    import uvicorn
    uvicorn.run(api_app, host="0.0.0.0", port=8000)


def run_spenny():
    logging.info("Starting SPENNY agent...")
    spenny_main()


def run_hedge_fund():
    if not hedge_main:
        logging.warning("Hedge Fund component not available")
        return
    logging.info("Starting Hedge Fund agent...")
    hedge_main()


def main():
    logging.basicConfig(level=logging.INFO)
    threads = []
    if api_app:
        threads.append(threading.Thread(target=run_api, name="API"))
    threads.append(threading.Thread(target=run_spenny, name="SPENNY"))
    if hedge_main:
        threads.append(threading.Thread(target=run_hedge_fund, name="HEDGE"))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
