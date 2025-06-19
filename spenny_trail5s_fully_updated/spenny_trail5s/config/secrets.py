# config/secrets.py

import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Dropbox API token
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

# Ensure DROPBOX_REMOTE_FOLDERS is set
_raw_folders = os.getenv('DROPBOX_REMOTE_FOLDERS')
if not _raw_folders:
    raise EnvironmentError('Missing DROPBOX_REMOTE_FOLDERS in .env')
DROPBOX_REMOTE_FOLDERS = [p.strip() for p in _raw_folders.split(';') if p.strip()]

if not DROPBOX_ACCESS_TOKEN:
    raise EnvironmentError("Missing DROPBOX_ACCESS_TOKEN in .env")

# LLaMA / AI stop-loss key (optional if USE_AI_STOP=False)
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")

# Broker API endpoint & key
API_ENDPOINT = os.getenv("API_ENDPOINT")
if not API_ENDPOINT:
    raise EnvironmentError("Missing API_ENDPOINT in .env")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise EnvironmentError("Missing API_KEY in .env")

# Additional app-level credentials
APP_KEY = os.getenv("APP_KEY")
if not APP_KEY:
    raise EnvironmentError("Missing APP_KEY in .env")

APP_SECRET = os.getenv("APP_SECRET")
if not APP_SECRET:
    raise EnvironmentError("Missing APP_SECRET in .env")

# Enable AI-based stop-loss moves
USE_AI_STOP = os.getenv("USE_AI_STOP", "False").lower() in ("1", "true", "yes")

# Parse multiple Dropbox folders to ingest (semicolon-separated, root-relative)
_raw_folders = os.getenv("DROPBOX_REMOTE_FOLDERS")
if not _raw_folders:
    raise EnvironmentError("Missing DROPBOX_REMOTE_FOLDERS in .env")
DROPBOX_REMOTE_FOLDERS = [p.strip() for p in _raw_folders.split(";") if p.strip()]

# Parse market hours windows (semicolon-separated "start,end" UTC hours)
_raw_windows = os.getenv("MARKET_WINDOWS", "")
if _raw_windows:
    MARKET_WINDOWS = []
    for segment in _raw_windows.split(";"):
        if not segment.strip():
            continue
        start, end = segment.split(",")
        MARKET_WINDOWS.append((int(start.strip()), int(end.strip())))
else:
    # Fallback to default in config/settings.py
    from config.settings import MARKET_WINDOWS
