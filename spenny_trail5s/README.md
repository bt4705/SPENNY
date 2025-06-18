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
2. **Create & activate a virtual environment**
   python3 -m venv .venv
   source .venv/bin/activate
3. **Copy & fill your .env**
   cp .env.example .env
# Edit .env with your DROPBOX_ACCESS_TOKEN, LLAMA_API_KEY,
# DROPBOX_REMOTE_FOLDERS, API_ENDPOINT, API_KEY, APP_KEY, APP_SECRET,
# USE_AI_STOP, MARKET_WINDOWS, etc.

4. **Install dependencies**
   pip install -r spenny_trail5s/requirements.txt

## Usage

1. **Change into the code directory**
   cd spenny_trail5s
2. **Run The Bot**
   python run.py
