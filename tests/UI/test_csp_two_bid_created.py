import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playwright.sync_api import expect
from pages.base_bid_page import BidCreate
import pytest




@pytest.mark.parametrize("user_fixture", ["logged_in_bidder1", "logged_in_bidder2"])
def test_bids_created(api_auction_publish, request, user_fixture):
    page_obj = request.getfixturevalue(user_fixture)
    prozorroId, draft_id = api_auction_publish
    page = BidCreate(page_obj, prozorroId)
    page.open_bid_page()
    page.loc_take_part.scroll_into_view_if_needed()
    page.loc_take_part.click()
    page.select_from_dropdown(page.loc_drdwn_profile, page.loc_select_profile)
    page.input_field(page.loc_bid_price, "11000")
    page.loc_continue_btn.click()
    page.loc_first_chbox.check()
    page.loc_second_chbox.check()
    page.loc_publish_btn.click()
    expect(page.page).to_have_url("https://qa.ualand.space/my-applications")
    expect(page.page.locator(f"text={prozorroId}")).to_be_visible()
