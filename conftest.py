import os
from dotenv import load_dotenv
from utils.logger import logger
from app.web.driver import driver  # shared web driver fixture

# Load env variables once for the whole session
load_dotenv()
logger.info("Environment variables loaded via conftest")

def get_base_url():
    base_url = os.getenv("BASE_URL")
    if base_url:
        logger.info(f"Loaded BASE_URL: {base_url}")
    else:
        logger.warning("BASE_URL not found in .env, using default")
        base_url = "https://www.saucedemo.com"
    return base_url




