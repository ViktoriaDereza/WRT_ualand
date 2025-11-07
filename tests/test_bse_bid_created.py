import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playwright.sync_api import expect
from pages.bse_bid_page import BidCreate


def test_bid_create(logged_in_bidder1, publish_auction):
    prozorroId = publish_auction["prozorroId"]
    page = BidCreate(logged_in_bidder1, prozorroId)
    page.open_bid_page()
    page.loc_take_part.click()
    page.select_from_dropdown(page.loc_drdwn_profile, page.loc_select_profile)
    page.input_field(page.loc_bid_price, "10000")
    page.loc_continue_btn.click()
    page.loc_first_chbox.check()
    page.loc_second_chbox.check()
    page.loc_publish_btn.click()
    expect(page.page).to_have_url("https://qa.ualand.space/my-applications")
    expect(page.page.locator(f"text={prozorroId}")).to_be_visible()



