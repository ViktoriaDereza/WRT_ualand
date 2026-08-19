from pages.base_page import BasePage
import re
from config import BASE_URL


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username = page.locator("input[type='text']")
        self.password = page.locator("input[type='password']")
        self.submit = page.get_by_role("button", name="Увійти")
        self.submit_adm = page.get_by_role("button", name="Вхід")
        self.login_error = page.get_by_text("Не коректно введена пошта або пароль").first
        self.logout_icon = page.locator('[data-testid="ExitToAppIcon"]')


    def open(self):
        self.page.goto(f"{BASE_URL}/login")
    def open_adm(self):
        self.page.goto(f"{BASE_URL}/land-admin/login")
    def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.submit.click()

    def login_adm(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.submit_adm.click()

    def logout(self):
        self.logout_icon.click()