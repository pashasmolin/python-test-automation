import allure
import pytest
from app.web_playwright.login_page import LoginPage

@allure.feature("Login [Playwright]")
@allure.story("Valid User login")
def test_valid_login():
    login_page = LoginPage(headless=False)
    inventory_page = login_page.login("standard_user", "secret_sauce")
    assert inventory_page.is_loaded