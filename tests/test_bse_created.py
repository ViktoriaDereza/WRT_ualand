import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pages.bse_create_page import BseCreate
from playwright.sync_api import expect


def test_draft_created(created_draft):
    create_page = created_draft["page"]
    response = created_draft["response"]
    draft_id = created_draft["draft_id"]
    draft_name = created_draft["draft_name"]

    assert response.status == 200

    draft_locator = create_page.draft_link(draft_id, draft_name)
    expect(draft_locator).to_be_visible()
def test_publish_auction(publish_auction, logged_in_organizer):
    publish_page = publish_auction["page"]
    prozorroId = publish_auction["prozorroId"]
    expect(publish_page.page.locator(f"text={prozorroId}")).to_be_visible()






