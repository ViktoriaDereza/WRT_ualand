from pages.basePage import BasePage



class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username = page.locator("input[type='text']")
        self.password = page.locator("input[type='password']")
        self.submit = page.get_by_role("button", name = "Увійти")

    def open(self):
        self.page.goto("https://qa.ualand.space/login")
    def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.submit.click()

