# Spenny Trading System

This repository contains a Python-based trading bot with both CLI and API entrypoints.

## Prerequisites

- Python 3.10 or higher
- `pip`

## Setup

1. Clone this repository and navigate into it:
   ```bash
   git clone <repo_url>
   cd spenny_refactor
   ```

2. Copy the example environment file and populate it with your credentials:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set:
   ```
   DROPBOX_ACCESS_TOKEN=<your Dropbox API token>
   DROPBOX_REMOTE_FOLDERS=folder1;folder2
   API_KEY=<your API key>
   # Optional overrides:
   LOG_LEVEL=INFO
   MARKET_WINDOWS=14,20
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### CLI (Trading Loop)
Run the continuous trading loop:
```bash
python -m spenny.cli
```

### API (FastAPI + Unified Agent)
Start the FastAPI server:
```bash
uvicorn spenny.api:app --reload
```

## Project Structure

```
spenny/
├── cli.py               # Entrypoint for trading loop
├── api.py               # Entrypoint for FastAPI + unified agent
├── config/              # Configuration loader and settings
│   └── __init__.py
├── core/                # Core trading logic (controller, risk, strategy, data)
├── agents/              # AI agent orchestration
├── execution/           # Market scheduling and execution bridge
├── ingestion/           # Data ingestion handlers
├── zones.py             # Zone definitions
└── tests/               # Unit tests
```

## Environment Example

Create a file named `.env.example` with the following content:

```
DROPBOX_ACCESS_TOKEN=
DROPBOX_REMOTE_FOLDERS=folder1;folder2
API_KEY=
LOG_LEVEL=INFO
MARKET_WINDOWS=14,20
```
