import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playwright.sync_api import expect
from pages.admin_bid_approve import BidApprove
from config import BASE_URL_ADMIN


def test_bid_approve(logged_in_admin, api_bid_create):
    page = BidApprove(logged_in_admin, api_bid_create)
    page.open_bid_page()
    page.approve_bid()
    expect(page.page).to_have_url(f"{BASE_URL_ADMIN}/bids?type=all")


