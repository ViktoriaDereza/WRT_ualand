import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playwright.sync_api import expect
from pages.csp_create_page import CspCreate
from config import AUCTION_NAME, BASE_URL

# def test_api_publish(api_login, api_auction_create):
#     request_context, headers = api_login
#     draft_id = api_auction_create
#     response = request_context.post(f"api/v1.0/auctions/{draft_id}/publish", headers=headers)
#     assert response.status == 200

def test_draft_created(logged_in_organizer, api_auction_create):
    draft_id = api_auction_create
    create_page = CspCreate(logged_in_organizer)
    create_page.open_myauction_page()
    draft_locator = create_page.page.locator(f"a:has-text('{draft_id}')")
    expect(draft_locator).to_be_visible()

def test_publish_auction(api_auction_publish, logged_in_organizer):
    publish_page = CspCreate(logged_in_organizer)
    prozorroId, draft_id = api_auction_publish
    draft_locator = publish_page.page.locator(f"a:has-text('{prozorroId}')")
    expect(draft_locator).to_be_visible()
