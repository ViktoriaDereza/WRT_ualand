from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url):
        self.page.goto(url)

    def fill(self, locator: str, value: str):
        self.page.fill(locator, value)

