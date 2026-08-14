from playwright.sync_api import Page, expect


class BidCreate:
    def __init__(self, page: Page, prozorroId: str):
        self.page = page
        self.prozorroId = prozorroId
        self.loc_search_field = page.get_by_placeholder("Ідентифікатор, назва, опис аукціону або об'єкта")
        self.loc_search_btn = page.get_by_text("Пошук", exact=True).first
        self.loc_auct_link = page.locator(f'a[href="/auctions/{prozorroId}"]').first


    def open_bid_page(self):
        self.loc_search_field.click()
        self.loc_search_field.fill(f"{self.prozorroId}")
        self.loc_search_btn.click()
        # Очікуємо відкриття нової вкладки після кліку по аукціону
        with self.page.context.expect_page() as new_page_info:
            self.loc_auct_link.click()
        # Зберігаємо нову сторінку як активну
        self.page = new_page_info.value
        self.page.wait_for_load_state()
        self.loc_take_part = self.page.get_by_role("button", name="Взяти участь")
        self.loc_drdwn_profile = self.page.get_by_role("combobox", name="Не визначено")
        self.loc_select_profile = self.page.get_by_role("option").first

        self.loc_bid_price = self.page.get_by_role("textbox", name="Не визначено")
        self.loc_continue_btn = self.page.get_by_role("button", name="Продовжити")
        self.loc_first_chbox = self.page.get_by_role("checkbox", name="Даю згоду на обробку персональних даних та приймаю умови Політики конфіденційнос")
        self.loc_second_chbox = self.page.get_by_role("checkbox", name="Ознайомлений з Регламентом роботи системи електронних торгів")
        self.loc_publish_btn = self.page.get_by_role("button", name="Опублікувати")
    def select_from_dropdown(self, dropdown_locator, option_locator):
         dropdown_locator.click()
         expect(option_locator).to_be_visible(timeout=5000)
         option_locator.click()

    def input_field(self, value_locator, value):
        value_locator.click()
        value_locator.fill(value)


