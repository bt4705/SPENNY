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

1. **Clone**  
   ```bash
   git clone https://github.com/yourusername/spenny.git
   cd spenny
   ```

2. **Create & activate a virtual environment**  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Copy & fill your `.env`**  
   ```bash
   cp .env.example .env
   # Edit .env with your DROPBOX_ACCESS_TOKEN, LLAMA_API_KEY,
   # DROPBOX_REMOTE_FOLDERS, API_ENDPOINT, API_KEY, APP_KEY, APP_SECRET,
   # USE_AI_STOP, MARKET_WINDOWS, etc.
   ```

4. **Install dependencies**  
   SPENNY’s code lives in the `spenny_trail5s/` subfolder, so point pip there:
   ```bash
   pip install -r spenny_trail5s/requirements.txt
   ```

## Usage

1. **Change into the code directory**  
   ```bash
   cd spenny_trail5s
   ```

2. **Run the bot**  
   ```bash
   python run.py
   ```
   - On startup it will download **all** your Dropbox folders (as configured in `DROPBOX_REMOTE_FOLDERS`), ingest them into `data/ingested_text/`, then begin the trading loop:
     - **Entry scans** every 60 s  
     - **Stop-loss updates** every 5 s (only if the stop actually moves)

## Configuration

- **`.env`** controls all your secrets:
  - `DROPBOX_ACCESS_TOKEN`  
  - `DROPBOX_REMOTE_FOLDERS` (e.g. `/GENERAL GRAPHS;/Spenny’s trading course;/DATA strategy`)  
  - `LLAMA_API_KEY`  
  - `API_ENDPOINT`, `API_KEY`, `APP_KEY`, `APP_SECRET`  
  - `USE_AI_STOP` (`true`/`false`)  
  - `MARKET_WINDOWS` (e.g. `14,20;22,2`)
- **`config/settings.py`** for:
  - `SYMBOLS`  
  - `LOOP_SEC` (entry interval)  
  - `STOP_UPDATE_SEC`  
  - ATR multiplier, data paths, etc.

## Directory Structure

```
spenny_trail5s/
├── run.py                 # Entry point: orchestrates ingestion & trading loops
├── .env.example           # Template for your environment vars
├── requirements.txt       # Packages for SPENNY’s Python code
├── config/
│   ├── settings.py        # Symbols, timings, risk parameters
│   └── secrets.py         # Loads/validates your .env keys
├── core/
│   ├── data.py            # Fetches 1m/5m/60m bars
│   ├── strategy.py        # Bull-flag & checklist logic
│   ├── risk.py            # ATR & position sizing
│   ├── zones.py           # Demand-zone detection
│   └── ingestion.py       # Dropbox download & OCR/text extraction
├── agents/
│   ├── market_hours.py    # Checks configurable market windows
│   └── llama_agent.py     # AI-driven stop-loss suggestions
├── execution/
│   ├── hedge_bridge.py    # REST API broker + local fallback
│   └── broker.py          # Mock/local order handling
└── data/
    ├── strategy/          # Populated from Dropbox on startup
    └── ingested_text/     # Generated .txt files from PDFs/images/docs
```

## License
MIT




