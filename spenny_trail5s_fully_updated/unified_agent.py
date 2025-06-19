"""Unified SPENNY + Hedge Fund + API runner."""
import threading
import logging
from backend.api import app as api_app
from core.bot import SpennyBot  # adjust import per actual code
from hedge_fund.main import main as hedge_main  # adjust if path

def run_api():
    import uvicorn
    uvicorn.run(api_app, host='0.0.0.0', port=8000)

def run_spenny():
    logging.info('Starting SPENNY agent...')
    # call your SPENNY entrypoint, e.g., SpennyBot().run()
    import run as spenny_run
    spenny_run.main()

def run_hedge_fund():
    logging.info('Starting Hedge Fund agent...')
    hedge_main()

def main():
    logging.basicConfig(level=logging.INFO)
    threads = [
        threading.Thread(target=run_api, name='API'),
        threading.Thread(target=run_spenny, name='SPENNY'),
        threading.Thread(target=run_hedge_fund, name='HEDGE')
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
