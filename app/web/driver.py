from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def get_driver():
    options = Options()

    # Always run headless on EC2
    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")

    # Required for running inside EC2/Linux without GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")

    # Make sure Chrome uses a unique profile dir
    options.add_argument("--user-data-dir=/tmp/chrome-profile")

    service = Service("/usr/local/bin/chromedriver")  # path to chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver
