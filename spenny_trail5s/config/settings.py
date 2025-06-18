SYMBOLS = ["SPY", "QQQ"]
LOOP_SEC = 60
STOP_UPDATE_SEC = 5     # Stop-loss update interval (seconds)

# Data ingestion paths
STRATEGY_DATA_DIR = "data/strategy"
INGESTED_DATA_DIR = "data/ingested_text"

# Stop loss strategy
ATR_MULTIPLIER = 1.0    # ATR for fallback
USE_AI_STOP = True      # Use AI to suggest stop
# MARKET_WINDOWS: semicolon-separated "start,end" UTC hours, e.g., "14,20;22,2"
MARKET_WINDOWS = [(14, 20)]  # will be loaded from secrets

# Dropbox remote folder path
DROPBOX_REMOTE_PATH = ""
