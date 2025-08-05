import os
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

def get_base_url():
    base_url = os.getenv("BASE_URL")
    if base_url:
        logger.info(f"Loaded BASE_URL: {base_url}")
    else:
        logger.warning("BASE_URL not found in .env, using default")
        base_url = "https://www.saucedemo.com"
    return base_url
