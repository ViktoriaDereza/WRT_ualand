import pytest
from pages.login import LoginPage
from playwright.sync_api import sync_playwright
from config import BASE_URL, USER_NAME_ORGANIZER, USER_NAME_PARTICIPANT1, USER_NAME_PARTICIPANT2, PASSWORD, CSP_PAYLOAD, PARTICIPANT1_PROFILE_ID
from utils.date_generator import DataGenerator
import json

def pytest_collection_modifyitems(items):
    order = {
        "test_csp_created.py": 1,
        "test_csp_bid_created.py": 2,
        "test_csp_two_bid_created.py": 3,
        "test_csp_bid_approve.py": 4,
    }

    items.sort(
        key=lambda item: order.get(item.path.name, 999)
    )


# A "subscribe to our Telegram bot" promo dialog pops up on its own timer
# (~30s after login, independent of route) and can intercept clicks on
# whatever the test happens to be doing at that moment. Likewise, a notistack
# "your profile is activated" toast pops in asynchronously (independent of
# any action the test takes) and renders bottom-right, where it can overlap
# the last entries of an open dropdown - e.g. FAST_MANUAL in the auction
# subtype list - and swallow the click. add_style_tag() only affects the
# current document, so it doesn't survive a full page.goto() or a new tab
# (e.g. the tab BidCreate opens for the auction page). Registering this as a
# context-level init script instead re-injects the CSS into every document
# the context ever loads - including new tabs - so it's set up once per
# context, before login, and needs no further attention from page objects.
TELEGRAM_PROMO_NEUTRALIZE_SCRIPT = """
document.addEventListener('DOMContentLoaded', () => {
    const style = document.createElement('style');
    style.textContent = ".MuiDialog-container:has(a[href*='t.me/']) { pointer-events: none !important; }" +
        "[class*='notistack-MuiContent'] { pointer-events: none !important; }";
    document.head.appendChild(style);
});
"""


@pytest.fixture
def logged_in_admin(browser):
    context = browser.new_context()   # створюємо ізольований контекст
    context.add_init_script(TELEGRAM_PROMO_NEUTRALIZE_SCRIPT)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.open_adm()
    login_page.login_adm("admin@test.com", "Test12345")
    page.wait_for_url("**/land-admin/users/all", timeout=10000)
    yield page
    context.close()
@pytest.fixture (scope="module")
def logged_in_organizer(browser):
    context = browser.new_context()   # створюємо ізольований контекст
    context.add_init_script(TELEGRAM_PROMO_NEUTRALIZE_SCRIPT)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(f"{USER_NAME_ORGANIZER}", f"{PASSWORD}")
    page.wait_for_url("**/auctions?status=active_tendering", timeout=10000)
    yield page
    context.close()
@pytest.fixture
def logged_in_bidder1(browser):
    context = browser.new_context()   # створюємо ізольований контекст
    context.add_init_script(TELEGRAM_PROMO_NEUTRALIZE_SCRIPT)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("ukr@gmail.com", "Test12345!")
    yield page
    context.close()
@pytest.fixture
def logged_in_bidder2(browser):
    context = browser.new_context()
    context.add_init_script(TELEGRAM_PROMO_NEUTRALIZE_SCRIPT)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("ukr3@gmail.com", "Test12345!")
    yield page
    context.close()
@pytest.fixture(scope="module")
def request_context(playwright):
    ctx = playwright.request.new_context(base_url=BASE_URL)
    yield ctx
    ctx.dispose()
@pytest.fixture(scope="module")
def api_login(request_context):
        response = request_context.post("/auth/api/users/login", data={"email": USER_NAME_ORGANIZER, "password": PASSWORD})
        assert response.status == 200
        token = response.json().get("accessToken")
        assert token
        headers = {"Authorization": f"Bearer {token}"}
        yield request_context, headers
@pytest.fixture
def api_login_bidder1(request_context):
        response = request_context.post("/auth/api/users/login", data={"email": USER_NAME_PARTICIPANT1, "password": PASSWORD})
        assert response.status == 200
        token = response.json().get("accessToken")
        assert token
        headers = {"Authorization": f"Bearer {token}"}
        yield request_context, headers

@pytest.fixture
def api_login_bidder2(request_context):
        response = request_context.post("/auth/api/users/login", data={"email": USER_NAME_PARTICIPANT2, "password": PASSWORD} )
        assert response.status == 200
        token = response.json().get("accessToken")
        assert token
        headers = {"Authorization": f"Bearer {token}"}
        yield request_context, headers
@pytest.fixture(scope="module")
def api_auction_create(api_login):
    request_context, headers = api_login
    payload = {**CSP_PAYLOAD, "startedAt": DataGenerator.utc_time_plus_minutes_iso(35)}
    response = request_context.post("api/auctions",  data=json.dumps(payload), headers={**headers, "Content-Type": "application/json"})
    # print("RESPONSE BODY:", response.text())
    assert response.status == 200
    response_json = response.json()
    draft_id = response_json["id"]
    return draft_id
@pytest.fixture(scope="module")
def api_auction_publish(api_login, api_auction_create):
    request_context, headers = api_login
    draft_id = api_auction_create
    response = request_context.post(f"api/auctions/{draft_id}/publish", headers=headers)
    response_json = response.json()
    prozorroId = response_json["prozorroId"]
    yield prozorroId, draft_id
@pytest.fixture
def api_bid_create(api_login_bidder1, api_auction_publish):
    prozorroId, draft_id = api_auction_publish
    request_context, headers = api_login_bidder1
    response = request_context.post(
        "api/bids",
        data=json.dumps({"auctionId": draft_id, "userProfileId": PARTICIPANT1_PROFILE_ID, "initialAmount": 11000}),
        headers={**headers, "Content-Type": "application/json"})

    print("TEXT:", response.text())
    response_json = response.json()
    bid_id = response_json["id"]
    request_context.patch(f"api/bids/{bid_id}/publish", headers=headers)
    return bid_id

