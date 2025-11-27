import pytest
from pages.login import LoginPage
from pages.bse_create_page import BseCreate
from playwright.sync_api import sync_playwright
from config import BASE_URL, USER_NAME_ORGANIZER, USER_NAME_PARTICIPANT1, USER_NAME_PARTICIPANT2, PASSWORD, CSP_PAYLOAD, PARTICIPANT1_PROFILE_ID
import json



@pytest.fixture
def logged_in_admin(browser):
    context = browser.new_context()   # створюємо ізольований контекст
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.open_adm()
    login_page.login_adm("admin@test.com", "Test12345")
    yield page
    context.close()
@pytest.fixture (scope="module")
def logged_in_organizer(browser):
    context = browser.new_context()   # створюємо ізольований контекст
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("ukr11@gmail.com", "Test12345!")
    yield page
    context.close()
@pytest.fixture
def logged_in_bidder1(browser):
    context = browser.new_context()   # створюємо ізольований контекст
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("ukr@gmail.com", "Test12345!")
    yield page
    context.close()
@pytest.fixture
def logged_in_bidder2(browser):
    context = browser.new_context()
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
        response = request_context.post("/auth/api/v1.0/login", data={"email": USER_NAME_ORGANIZER, "password": PASSWORD})
        assert response.status == 200
        token = response.json().get("accessToken")
        assert token
        headers = {"Authorization": f"Bearer {token}"}
        yield request_context, headers
@pytest.fixture
def api_login_bidder1(request_context):
        response = request_context.post("/auth/api/v1.0/login", data={"email": USER_NAME_PARTICIPANT1, "password": PASSWORD})
        assert response.status == 200
        token = response.json().get("accessToken")
        assert token
        headers = {"Authorization": f"Bearer {token}"}
        yield request_context, headers

@pytest.fixture
def api_login_bidder2(request_context):
        response = request_context.post("/auth/api/v1.0/login", data={"email": USER_NAME_PARTICIPANT2, "password": PASSWORD} )
        assert response.status == 200
        token = response.json().get("accessToken")
        assert token
        headers = {"Authorization": f"Bearer {token}"}
        yield request_context, headers
@pytest.fixture(scope="module")
def api_auction_create(api_login):
    request_context, headers = api_login
    response = request_context.post("api/v1.0/auctions",  data=json.dumps(CSP_PAYLOAD), headers={**headers, "Content-Type": "application/json"})
    # print("RESPONSE BODY:", response.text())
    assert response.status == 200
    response_json = response.json()
    draft_id = response_json["id"]
    return draft_id
@pytest.fixture(scope="module")
def api_auction_publish(api_login, api_auction_create):
    request_context, headers = api_login
    draft_id = api_auction_create
    response = request_context.post(f"api/v1.0/auctions/{draft_id}/publish", headers=headers)
    response_json = response.json()
    prozorroId = response_json["prozorroId"]
    yield prozorroId, draft_id
@pytest.fixture
def api_bid_create(api_login_bidder1, api_auction_publish):
    prozorroId, draft_id = api_auction_publish
    request_context, headers = api_login_bidder1
    response = request_context.post(
        "api/v1.0/bids",
        data=json.dumps({"auctionId": draft_id, "userProfileId": PARTICIPANT1_PROFILE_ID, "initialAmount": 11000}),
        headers={**headers, "Content-Type": "application/json"})

    print("TEXT:", response.text())
    response_json = response.json()
    bid_id = response_json["id"]
    request_context.patch(f"api/v1.0/bids/{bid_id}/publish", headers=headers)
    return bid_id

