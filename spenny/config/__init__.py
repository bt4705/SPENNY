import os
from dotenv import load_dotenv

load_dotenv()


def _env(key: str, *, required: bool = True, default=None):
    value = os.getenv(key, default)
    if required and value is None:
        raise EnvironmentError(f"Missing {key} environment variable")
    return value

# Dropbox configuration
DROPBOX_ACCESS_TOKEN = _env("DROPBOX_ACCESS_TOKEN")
DROPBOX_REMOTE_FOLDERS = [p.strip() for p in _env("DROPBOX_REMOTE_FOLDERS").split(';') if p.strip()]

# Optional AI key
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")

# Broker / API credentials
API_ENDPOINT = _env("API_ENDPOINT")
API_KEY = _env("API_KEY")
APP_KEY = _env("APP_KEY")
APP_SECRET = _env("APP_SECRET")

USE_AI_STOP = os.getenv("USE_AI_STOP", "false").lower() in ("1", "true", "yes")


def _parse_windows(raw: str):
    windows = []
    for segment in raw.split(';'):
        if not segment.strip():
            continue
        start, end = segment.split(',')
        windows.append((int(start.strip()), int(end.strip())))
    return windows

_raw_windows = os.getenv("MARKET_WINDOWS", "")
if _raw_windows:
    MARKET_WINDOWS = _parse_windows(_raw_windows)
else:
    from .settings import MARKET_WINDOWS as DEFAULT_WINDOWS
    MARKET_WINDOWS = DEFAULT_WINDOWS

# Re-export other static settings
from .settings import *
