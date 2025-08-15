import allure
from utils.config import get_base_url
from .browser import PlaywrightBrowser

class LoginPage(PlaywrightBrowser):
    def __init__(self, headless=False):
        super().__init__(headless)
        self.page.goto(get_base_url())
    
    @allure.step("Login with user: {username}")
    def login(self, username, password):
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")
        return InventoryPage(self.page)

class InventoryPage:
    def __init__(self, page):
        self.page = page
    
    @property
    def is_loaded(self):
        return "inventory" in self.page.url