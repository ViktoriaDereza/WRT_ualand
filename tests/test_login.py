import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from playwright.sync_api import expect
from pages.login import LoginPage
from config import (
    BASE_URL,
    USER_NAME_ORGANIZER,
    USER_NAME_PARTICIPANT1,
    PASSWORD,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    INVALID_LOGIN_EMAIL,
    INVALID_LOGIN_EMAIL_2,
    INVALID_LOGIN_PASSWORD,
)



def test_login_organizer_success(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(USER_NAME_ORGANIZER, PASSWORD)
    page.wait_for_url("**/auctions?status=active_tendering", timeout=10000)
    expect(page.get_by_role("button", name="Особистий кабінет")).to_be_visible()


def test_login_bidder_success(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(USER_NAME_PARTICIPANT1, PASSWORD)
    page.wait_for_url("**/auctions?status=active_tendering", timeout=10000)
    expect(page.get_by_role("button", name="Особистий кабінет")).to_be_visible()


def test_login_admin_success(page):
    login_page = LoginPage(page)
    login_page.open_adm()
    login_page.login_adm(ADMIN_EMAIL, ADMIN_PASSWORD)
    page.wait_for_url("**/land-admin/users/all", timeout=10000)


def test_login_wrong_password(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(INVALID_LOGIN_EMAIL, INVALID_LOGIN_PASSWORD)
    expect(login_page.login_error).to_be_visible()
    assert "/login" in page.url


def test_login_nonexistent_email(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(INVALID_LOGIN_EMAIL_2, INVALID_LOGIN_PASSWORD)
    expect(login_page.login_error).to_be_visible()
    assert "/login" in page.url


def test_login_empty_credentials(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.submit.click()
    expect(page.get_by_text("Пошта введена некоректно, або вже зареєстрована")).to_be_visible()
    expect(page.get_by_text("Поле не може бути пустим")).to_be_visible()
    assert "/login" in page.url


def test_logout_organizer(page):
    # The account sidebar (and its logout icon) only renders at desktop
    # widths; the default Playwright viewport is narrower and hides it.
    page.set_viewport_size({"width": 1920, "height": 1080})
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(USER_NAME_ORGANIZER, PASSWORD)
    page.wait_for_url("**/auctions?status=active_tendering", timeout=10000)

    login_page.logout()
    page.wait_for_url("**/login", timeout=10000)

    page.goto(f"{BASE_URL}/my-auctions")
    page.wait_for_url("**/login", timeout=10000)


def test_session_persists_after_reload(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(USER_NAME_ORGANIZER, PASSWORD)
    page.wait_for_url("**/auctions?status=active_tendering", timeout=10000)

    page.reload()

    page.wait_for_url("**/auctions?status=active_tendering", timeout=10000)
    expect(page.get_by_role("button", name="Особистий кабінет")).to_be_visible()
