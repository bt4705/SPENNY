"""
Centralized configuration for Spenny.
Loads environment variables with python-dotenv, validates required variables, and exposes a Settings object.
"""
 import Path
import os
from typing import List, Tuple
from dotenv import load_dotenv

# Load .env
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(f".env file not found at {dotenv_path}")

def _get_env_var(name: str, required: bool = False) -> str:
    val = os.getenv(name)
    if required and not val:
        raise RuntimeError(f"Required environment variable '{name}' is not set")
    return val or ""

# Static defaults
SYMBOLS: List[str] = ["SPY", "QQQ"]
LOOP_SEC: float = 60.0
STOP_UPDATE_SEC: float = 5.0

STRATEGY_DATA_DIR: str = "data/strategy"
INGESTED_DATA_DIR: str = "data/ingested_text"

ATR_MULTIPLIER: float = 1.0
USE_AI_STOP: bool = True

# Default market windows (UTC hours)
MARKET_WINDOWS: List[Tuple[int, int]] = [(14, 20)]

# Dynamic overrides
DROPBOX_ACCESS_TOKEN: str = _get_env_var("DROPBOX_ACCESS_TOKEN", required=True)
_raw_folders = _get_env_var("DROPBOX_REMOTE_FOLDERS", required=True)
DROPBOX_REMOTE_FOLDERS: List[str] = [p.strip() for p in _raw_folders.split(";") if p.strip()]

_raw_windows = _get_env_var("MARKET_WINDOWS")
if _raw_windows:
    MARKET_WINDOWS = []
    for segment in _raw_windows.split(";"):
        if not segment.strip():
            continue
        start, end = segment.split(",")
        MARKET_WINDOWS.append((int(start.strip()), int(end.strip())))

LOG_LEVEL: str = _get_env_var("LOG_LEVEL") or "INFO"

class Settings:
    """Settings object for Spenny config."""
    def __init__(self):
        self.symbols = SYMBOLS
        self.loop_sec = LOOP_SEC
        self.stop_update_sec = STOP_UPDATE_SEC
        self.strategy_data_dir = STRATEGY_DATA_DIR
        self.ingested_data_dir = INGESTED_DATA_DIR
        self.atr_multiplier = ATR_MULTIPLIER
        self.use_ai_stop = USE_AI_STOP
        self.market_windows = MARKET_WINDOWS
        self.dropbox_access_token = DROPBOX_ACCESS_TOKEN
        self.dropbox_remote_folders = DROPBOX_REMOTE_FOLDERS
        self.log_level = LOG_LEVEL

    def __repr__(self):
        return (
            f"Settings(symbols={self.symbols}, loop_sec={self.loop_sec}, "
            f"stop_update_sec={self.stop_update_sec}, market_windows={self.market_windows}, "
            f"dropbox_remote_folders={self.dropbox_remote_folders}, log_level={self.log_level})"
        )

settings = Settings()
