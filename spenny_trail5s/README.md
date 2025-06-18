# SPENNY Autonomous Trading Bot (Enhanced)

## Overview
SPENNY is a modular trading bot that:
- Ingests strategy docs from Dropbox (PDF, DOCX, images) into text
- Detects bull flag patterns on multiple timeframes (1m, 5m, 60m)
- Calculates risk-based positions
- Routes orders through hedge fund API with fallback
- Uses AI (LLaMA) to dynamically adjust stop-loss
- Operates during configurable market windows

## Setup

1. Clone:
   ```bash
   git clone https://github.com/yourusername/spenny.git
   cd spenny
   ```
2. Copy and fill `.env`:
   ```bash
   cp .env.example .env
   # Add your DROPBOX_ACCESS_TOKEN, LLAMA_API_KEY, DROPBOX_REMOTE_PATH, USE_AI_STOP, MARKET_WINDOWS
   ```
3. Install:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
```bash
python run.py
```
- The bot will download your strategy folder from Dropbox, ingest files, then start trading.

## Configuration
- `.env` controls secrets and market windows.
- `config/settings.py` for symbols and loop timing.

## Directory
- `run.py`: Entry point
- `config/`: settings & secrets
- `core/`: data, strategy, risk, zones, ingestion
- `agents/`: market hours & AI stop agent
- `execution/`: trade interfaces
- `data/strategy`: local folder (populated from Dropbox)
- `data/ingested_text`: ingested text output

## License
MIT
