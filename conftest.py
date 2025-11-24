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
@pytest.fixture
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
@pytest.fixture
def request_context(playwright):
    ctx = playwright.request.new_context(base_url=BASE_URL)
    yield ctx
    ctx.dispose()
@pytest.fixture
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
@pytest.fixture
def api_auction_create(api_login):
    request_context, headers = api_login
    response = request_context.post("api/v1.0/auctions",  data=json.dumps(CSP_PAYLOAD), headers={**headers, "Content-Type": "application/json"})
    # print("RESPONSE BODY:", response.text())
    assert response.status == 200
    response_json = response.json()
    draft_id = response_json["id"]
    return draft_id
@pytest.fixture
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



@pytest.fixture
def created_draft(logged_in_organizer):
    create_page = BseCreate(logged_in_organizer)
    draft_name = "Autotest Draft new"

    # Створення чернетки
    create_page.open_creating_page()
    create_page.select_from_dropdown(create_page.organizer_field, create_page.organizer_select)
    create_page.input_field(create_page.name, draft_name)
    create_page.select_from_dropdown(create_page.auction_type, create_page.type_select)
    create_page.select_from_dropdown(create_page.auction_subtype, create_page.subtype_select)
    create_page.input_field(create_page.lot_number, "1")
    create_page.input_field(create_page.description, "Опис аукціону")

    create_page.input_field(create_page.date, "19.11.2025_")
    create_page.input_field(create_page.time, "09:04")

    create_page.input_field(create_page.tender_attempt, "1")

    create_page.input_field(create_page.start_price, "10000")
    create_page.input_field(create_page.min_step, "2")
    # create_page.notification_close(create_page.close_notification)

    create_page.cav_selection(create_page.cav, create_page.select_cav, create_page.click_cav)
    create_page.input_field(create_page.quantity, "10")
    create_page.select_from_dropdown(create_page.measure, create_page.measure_select)

    create_page.input_field(create_page.lot_description, "lot description")
    create_page.select_from_dropdown(create_page.dropdown_country, create_page.select_country)
    create_page.select_from_dropdown(create_page.dropdown_region, create_page.select_region)
    create_page.input_field(create_page.town, "Черкаси")

    create_page.input_field(create_page.koatu, "3200000000")
    create_page.select_from_dropdown(create_page.reg_details, create_page.reg_details_select)
    create_page.bank_data.click()
    create_page.file_upload(create_page.upload_file)

    with logged_in_organizer.expect_response("**/api/v1.0/auctions") as response_info:
        create_page.draft_btn.click()

    response = response_info.value
    response_json = response.json()
    draft_id = response_json["id"]

    return {
        "page": create_page,
        "response": response,
        "draft_id": draft_id,
        "draft_name": draft_name
    }


@pytest.fixture
def publish_auction(api_auction_create, logged_in_organizer):
    draft_id = created_draft["draft_id"]
    publish_page = BseCreate(logged_in_organizer)
    publish_page.open(f"https://qa.ualand.space/auctions/{draft_id}")
    publish_page.loc_edite_btn.click()
    with publish_page.page.expect_response(f"**/api/v1.0/auctions/{draft_id}/publish") as response_info:
        publish_page.loc_publish_btn.click()
        response = response_info.value
        response_json = response.json()
        prozorroId = response_json["prozorroId"]
    return {
        "page": publish_page,
        "prozorroId": prozorroId,
        "response": response
    }
