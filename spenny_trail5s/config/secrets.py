import os
from dotenv import load_dotenv

load_dotenv()

DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
if not DROPBOX_ACCESS_TOKEN:
    raise EnvironmentError("Missing DROPBOX_ACCESS_TOKEN in .env")

LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
if not LLAMA_API_KEY:
    raise EnvironmentError("Missing LLAMA_API_KEY in .env")

# Load MARKET_WINDOWS from env if provided
raw_windows = os.getenv("MARKET_WINDOWS")
if raw_windows:
    # parse "14,20;22,2"
    parts = raw_windows.split(";")
    MARKET_WINDOWS = []
    for p in parts:
        start, end = p.split(",")
        MARKET_WINDOWS.append((int(start), int(end)))
else:
    from config.settings import MARKET_WINDOWS
