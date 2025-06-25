"""
Broker execution wrapper for SPENNY trading system.
"""
import logging
from typing import Dict, Any
import alpaca_trade_api as tradeapi
from ..utils.logging import get_logger

logger = get_logger(__name__)

class Broker:
    """
    Broker wrapper for executing trades and managing orders.
    """
    def __init__(self, api_key: str, api_secret: str, paper: bool = True):
        self.api = tradeapi.REST(
            api_key,
            api_secret,
            'https://paper-api.alpaca.markets' if paper else 'https://api.alpaca.markets',
            api_version='v2'
        )
        
    def get_account_value(self) -> float:
        """Get the current account value."""
        account = self.api.get_account()
        return float(account.portfolio_value)
        
    async def place_order(self, symbol: str, side: str, quantity: float) -> float:
        """
        Place a market order.
        
        Args:
            symbol: The trading symbol
            side: 'buy' or 'sell'
            quantity: The quantity to trade
            
        Returns:
            The execution price
        """
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=quantity,
                side=side,
                type='market',
                time_in_force='gtc'
            )
            
            # Wait for order to be filled
            while True:
                filled_order = self.api.get_order(order.id)
                if filled_order.status == 'filled':
                    return float(filled_order.filled_avg_price)
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error placing order: {str(e)}")
            raise
            
    async def place_stop_loss(self, symbol: str, price: float) -> None:
        """
        Place a stop-loss order.
        
        Args:
            symbol: The trading symbol
            price: The stop-loss price
        """
        try:
            self.api.submit_order(
                symbol=symbol,
                qty=1,  # Will be adjusted based on position size
                side='sell',
                type='stop',
                time_in_force='gtc',
                stop_price=price
            )
        except Exception as e:
            logger.error(f"Error placing stop-loss: {str(e)}")
            raise
            
    async def modify_stop_loss(self, symbol: str, new_price: float) -> None:
        """
        Modify an existing stop-loss order.
        
        Args:
            symbol: The trading symbol
            new_price: The new stop-loss price
        """
        try:
            # Get all stop orders for this symbol
            orders = self.api.list_orders(
                status='open',
                limit=50
            )
            
            for order in orders:
                if order.type == 'stop' and order.symbol == symbol:
                    self.api.cancel_order(order.id)
                    await self.place_stop_loss(symbol, new_price)
                    break
        except Exception as e:
            logger.error(f"Error modifying stop-loss: {str(e)}")
            raise
            
    def get_current_price(self, symbol: str) -> float:
        """
        Get the current market price for a symbol.
        
        Args:
            symbol: The trading symbol
            
        Returns:
            The current market price
        """
        try:
            barset = self.api.get_barset(symbol, 'minute', limit=1)
            return float(barset[symbol][0].c)
        except Exception as e:
            logger.error(f"Error getting price: {str(e)}")
            raise
