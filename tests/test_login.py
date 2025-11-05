import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playwright.sync_api import expect
from pages.login import LoginPage

def test_correct_login(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("ukr11@gmail.com", "Test12345!")
    expect(page).to_have_url("https://qa.ualand.space/auctions?size=5&status=ACTIVE_TENDERING&procedureType=all")
