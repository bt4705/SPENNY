"""
Configuration settings for SPENNY trading system.
"""
from dataclasses import dataclass
from typing import List, Dict
from dotenv import load_dotenv
import os

@dataclass
class Settings:
    """Application settings loaded from environment variables."""
    API_KEY: str
    API_SECRET: str
    DROPBOX_REMOTE_FOLDERS: Dict[str, str]
    SYMBOLS: List[str]
    RISK_PER_TRADE: float
    STOP_LOSS_PERCENT: float
    TAKE_PROFIT_PERCENT: float
    
    def __init__(self):
        load_dotenv()
        
        # Required environment variables
        required_vars = [
            'API_KEY',
            'API_SECRET',
            'DROPBOX_REMOTE_FOLDERS',
            'SYMBOLS',
            'RISK_PER_TRADE',
            'STOP_LOSS_PERCENT',
            'TAKE_PROFIT_PERCENT'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
        
        # Load settings
        self.API_KEY = os.getenv('API_KEY')
        self.API_SECRET = os.getenv('API_SECRET')
        self.DROPBOX_REMOTE_FOLDERS = {
            'data': os.getenv('DROPBOX_DATA_FOLDER'),
            'logs': os.getenv('DROPBOX_LOGS_FOLDER')
        }
        self.SYMBOLS = os.getenv('SYMBOLS', '').split(',')
        self.RISK_PER_TRADE = float(os.getenv('RISK_PER_TRADE'))
        self.STOP_LOSS_PERCENT = float(os.getenv('STOP_LOSS_PERCENT'))
        self.TAKE_PROFIT_PERCENT = float(os.getenv('TAKE_PROFIT_PERCENT'))
