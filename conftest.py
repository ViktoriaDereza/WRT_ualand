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
# whatever the test happens to be doing at that moment. Likewise, notistack
# toasts (e.g. "your profile is activated", "Повідомлення з аукціону") pop in
# asynchronously (independent of any action the test takes) and can overlap
# form fields - e.g. FAST_MANUAL in the auction subtype list - and swallow
# the click. These toasts render with no close button in their DOM at all
# and never auto-dismiss, so there is nothing to click to get rid of them;
# pointer-events: none is the only reliable way to stop them intercepting
# clicks. notistack keeps its outer .notistack-SnackbarContainer itself
# non-interactive (pointer-events: none) but each toast is wrapped in its own
# per-instance div (an unstable, hash-suffixed class - not something to
# select by name) that resets pointer-events back to "all", and that reset
# is inherited by every layer below it (.notistack-CollapseWrapper, the
# MuiAlert content, ...) regardless of what those layers' own content does.
# The only stable hook for that per-instance wrapper is its position in the
# DOM: it's always a direct child of .notistack-SnackbarContainer. Targeting
# it by structure re-neutralizes pointer-events right where notistack turns
# it back on, and every layer beneath it inherits "none" again from there.
# add_style_tag() only affects the
# current document, so it doesn't survive a full page.goto() or a new tab
# (e.g. the tab BidCreate opens for the auction page). Registering this as a
# context-level init script instead re-injects the CSS into every document
# the context ever loads - including new tabs - so it's set up once per
# context, before login, and needs no further attention from page objects.
TELEGRAM_PROMO_NEUTRALIZE_SCRIPT = """
document.addEventListener('DOMContentLoaded', () => {
    const style = document.createElement('style');
    style.textContent = ".MuiDialog-container:has(a[href*='t.me/']) { pointer-events: none !important; }" +
        ".notistack-SnackbarContainer > div { pointer-events: none !important; }";
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
    assert response.status == 200, response.text()
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
    assert response.status == 200, response.text()
    response_json = response.json()
    bid_id = response_json["id"]
    patch_response = request_context.patch(f"api/bids/{bid_id}/publish", headers=headers)
    assert patch_response.status == 200, patch_response.text()
    return bid_id

