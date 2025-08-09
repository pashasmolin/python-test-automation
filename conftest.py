import os
from dotenv import load_dotenv
from utils.logger import logger
import pytest
from app.web.driver import get_driver
from allure_commons.types import AttachmentType
import allure
from app.web.driver import driver  # shared web driver fixture


# Load env variables once for the whole session
load_dotenv()
logger.info("Environment variables loaded via conftest")

# Toggle: capture screenshots on success only if this is True
CAPTURE_ON_SUCCESS = os.getenv("SCREENSHOTS_ON_SUCCESS", "false").lower() == "true"


@pytest.fixture
def driver():
    drv = get_driver()
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Let pytest execute other hooks first
    outcome = yield
    report = outcome.get_result()

    # Only access the driver if it's in the test function's arguments
    driver = item.funcargs.get("driver", None)

    if driver is not None and report.when == "call":
        # On failure: always capture
        if report.failed:
            _attach_screenshot(driver, "Failure Screenshot")
        elif report.passed and CAPTURE_ON_SUCCESS:
            _attach_screenshot(driver, "Success Screenshot")

def _attach_screenshot(driver, name):
    try:
        png = driver.get_screenshot_as_png()
        allure.attach(png, name=name, attachment_type=AttachmentType.PNG)
    except Exception as e:
        print(f"[WARN] Failed to capture screenshot: {e}")




