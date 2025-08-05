
import pytest
from selenium import webdriver
from app.web.login_page import LoginPage

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_valid_login(driver):
    page = LoginPage(driver)
    page.load() 
    page.login("standard_user", "secret_sauce")
    assert "inventory" in driver.current_url