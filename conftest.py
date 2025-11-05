import pytest
from pages.login import LoginPage

@pytest.fixture
def logged_in_organizer(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("ukr11@gmail.com", "Test12345!")
    return page