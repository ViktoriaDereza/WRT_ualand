import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pages.bse_create_page import BseCreate
from playwright.sync_api import Page, expect


def test_check_draft_created(created_draft):
    create_page = created_draft["page"]
    response = created_draft["response"]
    draft_id = created_draft["draft_id"]
    draft_name = created_draft["draft_name"]

    assert response.status == 200

    draft_locator = create_page.draft_link(draft_id, draft_name)
    expect(draft_locator).to_be_visible()
def test_publish_auction(created_draft, logged_in_organizer):
     draft_id = created_draft["draft_id"]
     publish_page = BseCreate(logged_in_organizer)
     publish_page.open(f"https://qa.ualand.space/auctions/{draft_id}")
     publish_page.loc_edite_btn.click()
     with publish_page.page.expect_response(f"**/api/v1.0/auctions/{draft_id}/publish") as response_info:
        publish_page.loc_publish_btn.click()
        response = response_info.value
        response_json = response.json()
        prozorroId = response_json["prozorroId"]
     expect(publish_page.page.locator(f"text={prozorroId}")).to_be_visible()






