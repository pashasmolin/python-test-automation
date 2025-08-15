from playwright.sync_api import sync_playwright
import sys
from utils.logger import logger

class PlaywrightBrowser:
    def __init__(self, headless=False):
        self.playwright = sync_playwright().start()
        self.browser = self._launch_browser(headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        
    def _launch_browser(self, headless):
        browser_type = "chromium"  # Can be parameterized
        launch_options = {
            "headless": headless,
            "args": ["--disable-gpu", "--disable-extensions"]
        }
        
        if sys.platform == 'linux':
            launch_options.update({
                "args": ["--no-sandbox", "--disable-dev-shm-usage"],
                "channel": "chrome"  # Use system Chrome on Linux
            })
        
        logger.info(f"Launching {browser_type} with options: {launch_options}")
        return getattr(self.playwright, browser_type).launch(**launch_options)
    
    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()