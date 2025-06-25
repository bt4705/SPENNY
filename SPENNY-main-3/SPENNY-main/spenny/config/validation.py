"""
Configuration validation for SPENNY trading system.
"""
from typing import Dict, List
from .settings import Settings


def validate_settings(settings: Settings) -> None:
    """
    Validate the trading settings.
    
    Args:
        settings: The settings object to validate
        
    Raises:
        ValueError: If any settings are invalid
    """
    # Validate risk parameters
    if settings.RISK_PER_TRADE <= 0:
        raise ValueError("RISK_PER_TRADE must be greater than 0")
        
    if settings.STOP_LOSS_PERCENT <= 0:
        raise ValueError("STOP_LOSS_PERCENT must be greater than 0")
        
    if settings.TAKE_PROFIT_PERCENT <= 0:
        raise ValueError("TAKE_PROFIT_PERCENT must be greater than 0")
        
    # Validate symbols
    if not settings.SYMBOLS:
        raise ValueError("SYMBOLS list cannot be empty")
        
    # Validate Dropbox folders
    if not settings.DROPBOX_REMOTE_FOLDERS:
        raise ValueError("DROPBOX_REMOTE_FOLDERS must be configured")
        
    # Validate API credentials
    if not settings.API_KEY or not settings.API_SECRET:
        raise ValueError("API credentials are required")
