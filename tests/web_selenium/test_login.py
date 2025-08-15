import allure
from app.web_selenium.login_page import LoginPage

@allure.feature("Login")
@allure.story("Valid User login")
def test_valid_login(driver):
    page = LoginPage(driver)
    page.load() 
    page.login("standard_user", "secret_sauce")
    assert "inventory" in driver.current_url