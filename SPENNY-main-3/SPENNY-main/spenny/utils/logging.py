"""
Logging utilities for SPENNY trading system.
"""
import logging
import os
from datetime import datetime
from typing import Optional

def setup_logging(log_file: Optional[str] = None) -> None:
    """
    Configure logging for the application.
    
    Args:
        log_file: Optional path to log file. If None, logs to console only.
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = []
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    handlers.append(console_handler)
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=handlers
    )

def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Name of the logger
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

def log_exception(e: Exception, logger: logging.Logger) -> None:
    """
    Log an exception with full traceback.
    
    Args:
        e: The exception to log
        logger: The logger instance
    """
    logger.error(f"Exception occurred: {str(e)}", exc_info=True)
