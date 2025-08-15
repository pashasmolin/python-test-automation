import os
from dotenv import load_dotenv
from utils.logger import logger
import pytest
from app.web_selenium.driver import get_driver
from playwright.sync_api import Page
from app.web_playwright.browser import PlaywrightBrowser
from allure_commons.types import AttachmentType
import allure

# Load env variables once for the whole session
load_dotenv()
logger.info("Environment variables loaded via conftest")

# Toggle: capture screenshots on success only if this is True
CAPTURE_ON_SUCCESS = os.getenv("SCREENSHOTS_ON_SUCCESS", "false").lower() == "true"

# -------------------------------
# Selenium Fixtures 
# -------------------------------
@pytest.fixture
def driver():
    """Selenium WebDriver fixture"""
    # Get headless setting from environment (False by default on Mac)
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    drv = get_driver(headless=headless)
    yield drv
    drv.quit()

# -------------------------------
# Playwright Fixtures 
# -------------------------------
@pytest.fixture
def playwright_browser():
    """Playwright browser instance fixture"""
    headless = os.getenv("HEADLESS", "false").lower() == "true"
    browser = PlaywrightBrowser(headless=headless)
    yield browser
    browser.close()

@pytest.fixture
def playwright_page(playwright_browser):
    """Playwright page instance fixture"""
    yield playwright_browser.page

# -------------------------------
# Common Reporting Hooks
# -------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failure or success
    Handles both Selenium and Playwright tests
    """
    outcome = yield
    report = outcome.get_result()

    # Handle Selenium screenshots
    if "driver" in item.funcargs and report.when == "call":
        driver = item.funcargs["driver"]
        if report.failed:
            _attach_selenium_screenshot(driver, "Failure Screenshot [Selenium]")
        elif report.passed and CAPTURE_ON_SUCCESS:
            _attach_selenium_screenshot(driver, "Success Screenshot [Selenium]")

    # Handle Playwright screenshots
    if "playwright_page" in item.funcargs and report.when == "call":
        page = item.funcargs["playwright_page"]
        if report.failed or CAPTURE_ON_SUCCESS:
            _attach_playwright_screenshot(page, report)

def _attach_selenium_screenshot(driver, name):
    """Helper for Selenium screenshot attachment"""
    try:
        png = driver.get_screenshot_as_png()
        allure.attach(
            png,
            name=name,
            attachment_type=AttachmentType.PNG
        )
    except Exception as e:
        logger.warning(f"Failed to capture Selenium screenshot: {e}")

def _attach_playwright_screenshot(page, report):
    """Helper for Playwright screenshot attachment"""
    try:
        screenshot = page.screenshot(type="png")
        suffix = "Failure" if report.failed else "Success"
        allure.attach(
            screenshot,
            name=f"{suffix} Screenshot [Playwright]",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        logger.warning(f"Failed to capture Playwright screenshot: {e}")

# -------------------------------
# Optional: Hybrid Test Support
# -------------------------------
@pytest.fixture
def browser_context():
    """Provides both Selenium and Playwright contexts for comparison tests"""
    # Selenium setup
    selenium_driver = get_driver(headless=False)
    
    # Playwright setup
    playwright = PlaywrightBrowser(headless=False)
    
    yield {
        "selenium": selenium_driver,
        "playwright": playwright.page
    }
    
    # Cleanup
    selenium_driver.quit()
    playwright.close()