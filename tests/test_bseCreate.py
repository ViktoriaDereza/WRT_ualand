import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playwright.sync_api import expect
from pages.bseCreatePage import BseCreate
from playwright.sync_api import Page, expect

def test_create_auction(logged_in_organizer):
    create_page = BseCreate(logged_in_organizer)

    create_page.open_creating_page()
    create_page.select_from_dropdown(create_page.organizer_field, create_page.organizer_select)
    create_page.input_field(create_page.name, "BSE_plr")
    create_page.select_from_dropdown(create_page.auction_type, create_page.type_select)
    create_page.select_from_dropdown(create_page.auction_subtype, create_page.subtype_select)
    create_page.input_field(create_page.lot_number, "1")
    create_page.input_field(create_page.description, "Опис аукціону")

    create_page.input_field(create_page.date, "07.11.2025_")
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

    create_page.input_field(create_page.koatu, "3800000000")
    create_page.select_from_dropdown(create_page.reg_details, create_page.reg_details_select)
    create_page.bank_data.click()
    create_page.file_upload(create_page.upload_file)

    with logged_in_organizer.expect_response("**/api/v1.0/auctions") as response_info:
        create_page.draft_btn.click()
    response = response_info.value
    response_json = response.json()
    draft_id = response_json["id"]
    print(f"Status code: {response.status}")
    assert response.status == 200
    draft_locator = create_page.draft_link(draft_id, "BSE_plr")
    expect(draft_locator).to_have_attribute("href", f"/auctions/{draft_id}")





