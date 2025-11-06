from playwright.sync_api import Page


class BidCreate:
    def __init__(self, page: Page):
        self.page = page

        self.loc_drdwn_profile = page.locator('input[name="userProfileId"]')
        self.loc_select_profile = page.get_by_role("option", name="6 | Фізична особа | УчасникДругий")
        self.loc_bid_price = page.locator("xpath=//*[@id='root']/div/div[2]/div/main/div/div/div/div/div/div/div[3]/form/div/div[2]/div/div/div[3]/div/div/div")
        self.loc_continue_btn = page.get_by_role("button", name="Продовжити")
        self.loc_first_chbox = page.get_by_role("checkbox", name="Даю згоду на обробку персональних даних та приймаю умови")
        self.loc_second_chbox = page.get_by_role("checkbox", name="Ознайомлений з")
        self.loc_publish_btn = page.get_by_role("button", name="Опублікувати")

    def open_bid_page(self):
        self.my_account_btn.click()
        self.my_auction_link.click()
        self.create_auction_btn.click()
    def select_from_dropdown(self, dropdown_locator, option_locator):
         dropdown_locator.click()
         expect(option_locator).to_be_visible(timeout=5000)
         option_locator.click()

    def input_field(self, value_locator, value):
        value_locator.click()
        value_locator.fill(value)


