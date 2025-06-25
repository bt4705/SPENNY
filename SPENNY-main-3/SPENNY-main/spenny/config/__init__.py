"""
Configuration module for SPENNY trading system.
"""
from .settings import Settings
from .validation import validate_settings

__all__ = ['Settings', 'validate_settings']
