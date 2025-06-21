"""
Core trading loop and signal evaluation logic for SPENNY.
"""
import asyncio
import logging
from typing import Dict, Any
from datetime import datetime
import pandas as pd
from ..strategy.signals import evaluate_entry_signal
from ..core.execution import Broker
from ..utils.logging import get_logger

logger = get_logger(__name__)

class TradingEngine:
    """
    Main trading engine that manages the trading loop and signal evaluation.
    """
    def __init__(self, broker: Broker, symbols: List[str], risk_params: Dict[str, float]):
        self.broker = broker
        self.symbols = symbols
        self.risk_params = risk_params
        self.active_positions = {}
        self.last_signal_timestamp = datetime.min
        
    async def evaluate_signals(self) -> Dict[str, Any]:
        """
        Evaluate entry signals for all symbols.
        
        Returns:
            Dictionary mapping symbols to their signal evaluation results
        """
        signals = {}
        for symbol in self.symbols:
            try:
                signal = await evaluate_entry_signal(symbol)
                signals[symbol] = signal
                logger.info(f"Signal evaluated for {symbol}: {signal}")
            except Exception as e:
                logger.error(f"Error evaluating signal for {symbol}: {str(e)}")
                signals[symbol] = None
        return signals
        
    async def execute_best_signal(self, signals: Dict[str, Any]) -> None:
        """
        Execute the best signal among all evaluated signals.
        
        Args:
            signals: Dictionary of symbol -> signal evaluation results
        """
        # Find the best signal
        best_signal = None
        best_score = float('-inf')
        best_symbol = None
        
        for symbol, signal in signals.items():
            if signal and signal['enter'] and signal['score'] > best_score:
                best_signal = signal
                best_score = signal['score']
                best_symbol = symbol
        
        if best_symbol:
            try:
                # Execute the trade
                entry_price = await self.broker.place_order(
                    symbol=best_symbol,
                    side='buy',
                    quantity=self.calculate_position_size(best_symbol)
                )
                
                # Place stop-loss
                stop_loss_price = self.calculate_stop_loss(entry_price, best_symbol)
                await self.broker.place_stop_loss(
                    symbol=best_symbol,
                    price=stop_loss_price
                )
                
                self.active_positions[best_symbol] = {
                    'entry_price': entry_price,
                    'stop_loss': stop_loss_price,
                    'timestamp': datetime.now()
                }
                
                logger.info(f"Entered position in {best_symbol} at {entry_price}")
            except Exception as e:
                logger.error(f"Error executing trade for {best_symbol}: {str(e)}")
                
    async def update_trailing_stops(self) -> None:
        """
        Update trailing stops for all active positions.
        """
        for symbol, position in self.active_positions.items():
            try:
                current_price = await self.broker.get_current_price(symbol)
                new_stop = self.calculate_trailing_stop(
                    position['entry_price'],
                    current_price,
                    position['stop_loss']
                )
                
                if new_stop > position['stop_loss']:
                    await self.broker.modify_stop_loss(symbol, new_stop)
                    position['stop_loss'] = new_stop
                    logger.info(f"Updated stop-loss for {symbol} to {new_stop}")
            except Exception as e:
                logger.error(f"Error updating stop-loss for {symbol}: {str(e)}")
                
    def calculate_position_size(self, symbol: str) -> float:
        """
        Calculate position size based on risk parameters.
        
        Args:
            symbol: The trading symbol
            
        Returns:
            Position size in units
        """
        account_value = self.broker.get_account_value()
        risk_amount = account_value * self.risk_params['RISK_PER_TRADE']
        
        # Get the current price (this should be implemented in the broker)
        current_price = self.broker.get_current_price(symbol)
        
        return risk_amount / (current_price * self.risk_params['STOP_LOSS_PERCENT'])
        
    def calculate_stop_loss(self, entry_price: float, symbol: str) -> float:
        """
        Calculate initial stop-loss price.
        
        Args:
            entry_price: The entry price of the trade
            symbol: The trading symbol
            
        Returns:
            Stop-loss price
        """
        return entry_price * (1 - self.risk_params['STOP_LOSS_PERCENT'])
        
    def calculate_trailing_stop(self, entry_price: float, current_price: float, current_stop: float) -> float:
        """
        Calculate trailing stop price.
        
        Args:
            entry_price: The entry price of the trade
            current_price: The current market price
            current_stop: The current stop-loss price
            
        Returns:
            New trailing stop price
        """
        max_price = max(entry_price, current_price)
        return max_price * (1 - self.risk_params['STOP_LOSS_PERCENT'])
        
    async def run(self) -> None:
        """
        Main trading loop that runs every 5 seconds.
        """
        while True:
            try:
                # Evaluate signals
                signals = await self.evaluate_signals()
                
                # Execute best signal
                await self.execute_best_signal(signals)
                
                # Update trailing stops
                await self.update_trailing_stops()
                
                # Wait for next cycle
                await asyncio.sleep(5)
                
            except KeyboardInterrupt:
                logger.info("Trading loop interrupted. Cleaning up...")
                break
            except Exception as e:
                logger.exception("Error in trading loop:")
                await asyncio.sleep(5)  # Wait before retrying
