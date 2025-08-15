# Python Test Automation Framework (Web/API)

## ⚡ Quick Setup

```bash
# 1. Clone repo
cd python-test-automation

# 2. Create and activate virtualenv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt
playwright install
playwright install-deps  # Linux only

# 4. Install Allure CLI
brew install allure  # Mac
# OR Linux:
sudo apt-add-repository ppa:qameta/allure && sudo apt update && sudo apt install allure

# 5. Run Selenium tests
HEADLESS=false SCREENSHOTS_ON_SUCCESS=false pytest tests/web_selenium/ --alluredir=./allure-results -v
allure serve ./allure-results

# 6. Run Playwrite tests
HEADLESS=false SCREENSHOTS_ON_SUCCESS=false pytest tests/web_playwright/ --alluredir=./allure-results -v
allure serve ./allure-results