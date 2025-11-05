# from pages.basePage import BasePage
from playwright.sync_api import expect
from playwright.sync_api import Page


class BseCreate:
    def __init__(self, page: Page):
        self.page = page
        # super().__init__(page)
        self.my_account_btn = page.get_by_role("button", name="Особистий кабінет")
        self.my_auction_link = page.get_by_role("link", name="Мої аукціони")
        self.create_auction_btn = page.get_by_role("button", name="Створити аукціон")
        self.organizer_field = page.get_by_label("", exact=True)
        self.organizer_select = page.get_by_role("option", name="ТОВ \"Буб\"")
        self.name = page.get_by_role("textbox", name="Введіть назву")
        self.lot_number = page.get_by_placeholder("Введіть номер лотa")

        self.description = page.locator("xpath=//*[@id='root']/div/div[2]/div/main/div/div/div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/textarea[1]")
        self.auction_type = page.get_by_role("button", name="Оберіть тип процедури")
        self.type_select = page.get_by_role("option", name="Продаж на \"англійському аукціоні\"")
        self.auction_subtype = page.get_by_role("button", name="USUAL")
        self.subtype_select = page.get_by_role("option", name="FAST_MANUAL", exact=True)

        self.date = page.locator("input[name=\"date\"]")
        self.time = page.locator("xpath=//*[@id='root']/div/div[2]/div/main/div/div/div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div[1]/div/div[3]/div/div[1]/div/input")
        self.tender_attempt = page.locator("xpath=//*[@id='root']/div/div[2]/div/main/div/div/div/div/div[3]/div/div/div/div[2]/div/div[2]/div/div[1]/div/div[4]/div/div[1]/div/input")

        self.start_price = page.locator('input[name="specificData.initialAmount"]')
        self.registry = page.locator('input[name="specificData.registrationAmount"]')
        self.guarantee = page.locator('input[name="specificData.guaranteeAmount"]')
        self.min_step = page.locator("xpath=//*[@id='root']/div/div[2]/div/main/div/div/div/div/div[3]/div/div/div/div[3]/div/div[2]/div[2]/div/div[1]/div/input")

        self.close_notification = page.locator("xpath=/html/body/div[2]/div[3]/div/button")

        self.cav = page.get_by_placeholder("Оберіть основний класифікатор")
        self.select_cav = page.get_by_role("treeitem", name="16000000-5").get_by_role("checkbox")
        self.click_cav = page.get_by_role("button", name="Обрати")

        self.lot_description = page.locator("xpath=//*[@id='root']/div[1]/div[2]/div/main/div/div/div/div/div[3]/div/div/div/div[4]/div/div[3]/div[4]/div/div[1]/div/textarea[1]")
        self.quantity = page.locator('input[name="specificData.lots.0.quantity"]')
        self.measure = page.locator("xpath=//*[@id='mui-component-select-specificData.lots.0.measureUnit']")
        self.measure_select = page.get_by_text("штуки")

        self.dropdown_country = page.locator("[id=\"mui-component-select-specificData.lots.0.address.country\"]")
        self.select_country = page.get_by_role("option", name="Україна")
        self.dropdown_region = page.get_by_role("button", name="Оберіть опцію")
        self.select_region = page.get_by_role("option", name="Запорізька область")
        self.town = page.get_by_role("textbox", name="Введіть назву").nth(1)

        self.koatu = page.locator("xpath=//*[@id='root']/div[1]/div[2]/div/main/div/div/div/div/div[3]/div/div/div/div[4]/div/div[3]/div[5]/div/div[8]/div/div[1]/div/input")
        self.reg_details = page.locator("xpath=//*[@id='mui-component-select-specificData.lots.0.registrationDetails.status']")
        self.reg_details_select = page.get_by_text("Не зареєстровано")
        self.bank_data = page.get_by_text("Заповнити реквізити з мого профілю")
        self.upload_file = page.locator("xpath=//*[@id='root']/div/div[2]/div/main/div/div/div/div/div[3]/div/div/div/div[6]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/div/div[1]/div/input")

        self.draft_btn = page.locator("xpath=//*[@id='saveAsDraft']")
        self.auct_mame = page.get_by_role("heading", name="BSE_plr")


    def open_creating_page(self):
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

    def file_upload(self, file_locator):
       # file_locator.click()
        file_locator.set_input_files("C:\\Users\\user\\Downloads\\Test_PDF.pdf")

    # def notification_close(self, locator, timeout=1000):
    #     try:
    #         locator.wait_for(state="visible", timeout=timeout)
    #         locator.click()
    #         print("Notification closed")
    #     except TimeoutError:
    #         pass

    def notification_close(self, locator, max_wait=5000, interval=200):
        """
        Надійно закриває попап/нотифікацію.
        locator: Playwright locator кнопки закриття
        max_wait: максимальний час очікування появи попапу (мс)
        interval: інтервал між перевірками (мс)
        Якщо попап не з’явився протягом max_wait — тест продовжується.
        """
        elapsed = 0
        while elapsed < max_wait:
            if locator.is_visible():
                locator.click()
                return
            self.page.wait_for_timeout(interval)  # чекаємо короткий проміжок
            elapsed += interval

    def cav_selection(self, locator, dropdown_locator, option_locator):
        locator.click()
        expect(dropdown_locator).to_be_visible(timeout=5000)
        dropdown_locator.check()
        option_locator.click()


