from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import os

def get_driver(headless=False):  # ← Make headless configurable
    options = Options()
    
    # Common settings for all platforms
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    # Platform-specific optimizations
    if sys.platform == 'linux':  # Ubuntu/EC2
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        profile_dir = "/tmp/chrome-profile-linux"
    else:  # MacOS
        profile_dir = "/tmp/chrome-profile-mac"

    # Headless mode control (only activate if requested AND on Linux)
    if headless and sys.platform == 'linux':
        options.add_argument("--headless")  # Standard headless for Linux
        options.add_argument("--remote-debugging-port=9222")

    # Profile management
    options.add_argument(f"--user-data-dir={profile_dir}")
    if os.path.exists(profile_dir):
        os.system(f"rm -rf {profile_dir}")
    
    return webdriver.Chrome(options=options)