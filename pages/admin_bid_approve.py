import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playwright.sync_api import Page
from config import BASE_URL_ADMIN
class BidApprove:
    def __init__(self, page: Page, api_bid_create: str):
        self.page = page
        self.api_bid_create = api_bid_create
        self.url = f"{BASE_URL_ADMIN}/applications/{self.api_bid_create}"
        self.loc_approve = self.page.get_by_role("button", name="Активувати заявку")
    def open_bid_page(self):
        self.page.goto(self.url)

    def approve_bid(self):
        self.loc_approve.click()
