"""
Unified agent for SPENNY trading system.

This script combines the trading agent, hedge fund integration,
and FastAPI server into a single process.
"""
import asyncio
import logging
from typing import Dict, Any
import uvicorn
from fastapi import FastAPI
from spenny.config.settings import Settings
from spenny.core.trading import TradingEngine
from spenny.core.execution import Broker
from spenny.utils.logging import setup_logging

# Configure logging
setup_logging(log_file="spenny.log")
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Global variables
trading_engine: TradingEngine = None

@app.on_event("startup")
async def startup_event():
    """Initialize the trading engine on startup."""
    global trading_engine
    settings = Settings()
    broker = Broker(settings.API_KEY, settings.API_SECRET)
    
    # Initialize trading engine
    trading_engine = TradingEngine(
        broker=broker,
        symbols=settings.SYMBOLS,
        risk_params={
            'RISK_PER_TRADE': settings.RISK_PER_TRADE,
            'STOP_LOSS_PERCENT': settings.STOP_LOSS_PERCENT,
            'TAKE_PROFIT_PERCENT': settings.TAKE_PROFIT_PERCENT
        }
    )
    
    # Start trading loop in a separate task
    asyncio.create_task(trading_engine.run())
    
    logger.info("Trading engine started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    global trading_engine
    if trading_engine:
        logger.info("Shutting down trading engine...")
        trading_engine = None

@app.get("/health")
async def health_check():
    """Check if the API is running."""
    return {"status": "healthy"}

@app.get("/positions")
async def get_positions():
    """Get current positions."""
    global trading_engine
    if not trading_engine:
        raise HTTPException(status_code=500, detail="Trading engine not initialized")
    
    return {
        "positions": list(trading_engine.active_positions.items())
    }

@app.get("/signals/{symbol}")
async def get_signal(symbol: str):
    """
    Get the current trading signal for a symbol.
    
    Args:
        symbol: The trading symbol
    """
    global trading_engine
    if not trading_engine:
        raise HTTPException(status_code=500, detail="Trading engine not initialized")
    
    try:
        signal = await trading_engine.evaluate_signals()
        return {
            "symbol": symbol,
            "signal": signal.get(symbol)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
