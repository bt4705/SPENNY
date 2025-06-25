"""
Screen automation utilities for SPENNY trading system.
"""
import pyautogui
import pytesseract
import cv2
import numpy as np
from typing import Optional, Tuple
from datetime import datetime
import logging
from ..utils.logging import get_logger

logger = get_logger(__name__)

class ScreenAutomation:
    """
    Handles GUI-based trading operations.
    """
    def __init__(self, broker_window_title: str):
        self.broker_window_title = broker_window_title
        self.last_screenshot = None
        
    def locate_element(self, template_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        Locate an element on screen using image matching.
        
        Args:
            template_path: Path to the template image
            confidence: Minimum confidence threshold
            
        Returns:
            Tuple of (x, y) coordinates if found, None otherwise
        """
        try:
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
            
            # Load template
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            
            # Find template
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                return max_loc
            return None
            
        except Exception as e:
            logger.error(f"Error locating element: {str(e)}")
            return None
            
    def click_element(self, template_path: str) -> bool:
        """
        Click an element on screen.
        
        Args:
            template_path: Path to the template image
            
        Returns:
            True if click was successful, False otherwise
        """
        try:
            location = self.locate_element(template_path)
            if location:
                x, y = location
                pyautogui.click(x + 10, y + 10)  # Click slightly offset from top-left
                return True
            return False
        except Exception as e:
            logger.error(f"Error clicking element: {str(e)}")
            return False
            
    def read_text_from_region(self, region: Tuple[int, int, int, int]) -> str:
        """
        Read text from a specific region of the screen.
        
        Args:
            region: Tuple of (x, y, width, height)
            
        Returns:
            Text content of the region
        """
        try:
            screenshot = pyautogui.screenshot(region=region)
            text = pytesseract.image_to_string(screenshot)
            return text.strip()
        except Exception as e:
            logger.error(f"Error reading text: {str(e)}")
            return ""
            
    def wait_for_element(self, template_path: str, timeout: int = 10) -> bool:
        """
        Wait for an element to appear on screen.
        
        Args:
            template_path: Path to the template image
            timeout: Maximum wait time in seconds
            
        Returns:
            True if element appears within timeout, False otherwise
        """
        start_time = datetime.now()
        while (datetime.now() - start_time).total_seconds() < timeout:
            if self.locate_element(template_path):
                return True
            await asyncio.sleep(1)
        return False
