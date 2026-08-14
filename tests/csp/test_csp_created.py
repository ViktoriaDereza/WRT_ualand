import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playwright.sync_api import expect
from pages.csp_create_page import CspCreate
from config import BASE_URL
from utils.date_generator import DataGenerator


def test_draft_created(logged_in_organizer):
    create_page = CspCreate(logged_in_organizer)
    draft_name = "Autotest Draft new"
    # Створення чернетки
    create_page.open_creating_page()
    create_page.select_from_dropdown(create_page.organizer_field, create_page.organizer_select)
    create_page.input_field(create_page.name, draft_name)
    create_page.select_from_dropdown(create_page.auction_type, create_page.type_select)
    create_page.select_from_dropdown(create_page.auction_subtype, create_page.subtype_select)
    create_page.input_field(create_page.lot_number, "1")
    create_page.input_field(create_page.description, "Опис аукціону")

    create_page.input_field(create_page.date, DataGenerator.current_date())
    create_page.input_field(create_page.time, DataGenerator.current_time_plus_any_minutes(45))

    create_page.input_field(create_page.tender_attempt, "1")

    create_page.input_field(create_page.start_price, "10000")
    create_page.input_field(create_page.min_step, "2")
    # create_page.notification_close(create_page.close_notification)
    create_page.select_from_dropdown(create_page.identifier_field, create_page.identifier_select)
    create_page.input_field(create_page.full_name, "Повне найменування організації")
    create_page.input_field(create_page.codEDRPOU, "12345678")
    create_page.select_from_dropdown(create_page.region, create_page.region_select)
    create_page.input_field(create_page.city, "Київ")
    create_page.input_field(create_page.address, "вул. Велика Васильківська, 1")
    create_page.input_field(create_page.postal_code, "01001")
    create_page.from_f.clear()


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
    create_page.add_doc.click()
    create_page.file_upload(create_page.upload_file)

    with logged_in_organizer.expect_response("**/api/auctions") as response_info:
        create_page.draft_btn.click()
    response = response_info.value
    response_json = response.json()
    draft_id = response_json["id"]
    create_page.open_myauction_page()
    draft_locator = create_page.page.locator(f"a:has-text('{draft_id}')")
    expect(draft_locator).to_be_visible()

def test_publish_auction(logged_in_organizer, api_auction_create):
    publish_page = CspCreate(logged_in_organizer)
    draft_id = api_auction_create
    publish_page.open(f"{BASE_URL}/edit-auction/{draft_id}")

    with logged_in_organizer.expect_response(f"**/api/auctions/{draft_id}/publish") as response_info:
        publish_page.publish_btn.click()
    response = response_info.value
    response_json = response.json()
    prozorroId = response_json["prozorroId"]
    draft_locator = publish_page.page.get_by_text(prozorroId, exact=True)
    expect(draft_locator).to_be_visible()
