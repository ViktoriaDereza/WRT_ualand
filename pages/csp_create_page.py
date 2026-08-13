import re
from pathlib import Path
from playwright.sync_api import expect
from playwright.sync_api import Page
from config import BASE_URL

TEST_PDF_PATH = Path(__file__).resolve().parent.parent / "test_data" / "files" / "test_document.pdf"


class CspCreate:
    def __init__(self, page: Page):
        self.page = page
        self.my_account_btn = page.get_by_role("button", name="Особистий кабінет")
        self.my_auction_link = page.get_by_role("link", name="Мої аукціони")
        self.create_auction_btn = page.get_by_role("link", name="Створити аукціон")
        self.organizer_field = page.get_by_text("Оберіть профіль", exact=False).locator("xpath=following::div[@role='combobox'][1]")
        self.organizer_select = page.get_by_role("option", name="ТОВ \"Буб\"")
        self.name = page.get_by_role("textbox", name="Введіть назву")
        self.lot_number = page.get_by_placeholder("Ведіть номер лотa")
        self.description = page.get_by_text("Опис аукціону", exact=False).locator("xpath=following::textarea[1]")
        self.auction_type = page.get_by_role("combobox", name="Оберіть тип процедури")
        self.type_select = page.get_by_role("option", name="Комерційні продажі на \"англійському аукціоні з переважним правом\"")
        self.auction_subtype = page.get_by_role("combobox", name="USUAL")
        self.subtype_select = page.get_by_role("option", name="FAST_MANUAL", exact=True)

        self.date = page.locator("input[name=\"date\"]")
        self.time = page.get_by_text("Час проведення аукціону", exact=False).locator("xpath=following::input[1]")
        self.tender_attempt = page.get_by_text("Лот виставляється", exact=False).locator("xpath=following::input[1]")

        self.start_price = page.locator('input[name="specificData.initialAmount"]')
        self.registry = page.locator('input[name="specificData.registrationAmount"]')
        self.guarantee = page.locator('input[name="specificData.guaranteeAmount"]')
        self.min_step = page.get_by_text("Мінімальний крок аукціону, %", exact=False).locator("xpath=following::input[1]")

        self.close_notification = page.locator("xpath=/html/body/div[2]/div[3]/div/button")
#priority data

        self.identifier_field = page.get_by_text("Ідентифікатори організації", exact=False).first.locator("xpath=following::div[@role='combobox'][1]")
        self.identifier_select = page.get_by_role("option", name="ЄДРПОУ")
        self.full_name = page.get_by_text("Повна юридична назва організації або ПІБ", exact=False).locator("xpath=following::input[1]")
        self.codEDRPOU = page.get_by_text("Код ЄДРПОУ або ІПН або паспорт", exact=False).first.locator("xpath=following::input[1]")
        self.region = page.get_by_text("Область", exact=False).first.locator("xpath=following::div[@role='combobox'][1]")
        self.region_select = page.get_by_role("option", name="Запорізька область")
        self.city = page.get_by_text("Населений пункт", exact=False).first.locator("xpath=following::input[1]")
        self.address = page.get_by_text(re.compile(r"^Адреса")).first.locator("xpath=following::input[1]")
        self.postal_code = page.get_by_text("Поштовий індекс", exact=False).first.locator("xpath=following::input[1]")
        self.from_f = page.get_by_text("Період з", exact=False).locator("xpath=following::input[1]")




        self.cav = page.get_by_placeholder("Оберіть основний класифікатор")
        self.select_cav = page.get_by_role("treeitem", name="16000000-5").get_by_role("checkbox")
        self.click_cav = page.get_by_role("button", name="Обрати")

        self.lot_description = page.get_by_text("Опис об'єкта", exact=False).locator("xpath=following::textarea[1]")
        self.quantity = page.locator('input[name="specificData.lots.0.quantity"]')
        self.measure = page.get_by_text("Одиниці виміру", exact=False).locator("xpath=following::div[@role='combobox'][1]")
        self.measure_select = page.get_by_role("option", name="штуки")

        self.dropdown_country = page.get_by_text(re.compile(r"^Країна")).nth(1).locator("xpath=following::div[@role='combobox'][1]")
        self.select_country = page.get_by_role("option", name="Україна")
        self.dropdown_region = page.get_by_text(re.compile(r"^Область")).nth(1).locator("xpath=following::div[@role='combobox'][1]")
        self.select_region = page.get_by_role("option", name="Запорізька область")
        self.town = page.get_by_text("Населений пункт", exact=False).nth(1).locator("xpath=following::input[1]")

        self.koatu = page.get_by_text("адміністративно-територіального устрою", exact=False).locator("xpath=following::input[1]")
        self.reg_details = page.get_by_text("Стан державної реєстрації об'єкту", exact=False).locator("xpath=following::div[@role='combobox'][1]")
        self.reg_details_select = page.get_by_text("Не зареєстровано")
        self.bank_data = page.get_by_text("Заповнити реквізити з мого профілю")
        self.add_doc = page.get_by_text("Додати документ", exact=False).locator("xpath=following::button[1]")
        self.upload_file = page.locator("input[type='file'][name='documents']")

        self.draft_btn = page.locator("xpath=//*[@id='saveAsDraft']")
        self.publish_btn = page.get_by_role("button", name="Опублікувати")


    def draft_link(self, draft_id: str, name: str):
        return self.page.locator(f'a[href="/my-auctions/{draft_id}"]', has_text=name)

    def open_myauction_page(self):
        self.url = f"{BASE_URL}/my-auctions"
        self.page.goto(self.url)

    def open(self, url):
        self.page.goto(url)
    def open_creating_page(self):
        self.my_account_btn.click()
        self.my_auction_link.click()
        self.create_auction_btn.click()


    def close_telegram_modal(self):
        close_btn = self.page.get_by_role("dialog").locator("button:has(svg[data-testid='CloseIcon'])")
        if close_btn.is_visible():
            close_btn.click()

    def select_from_dropdown(self, dropdown_locator, option_locator):
         self.close_telegram_modal()
         dropdown_locator.click()
         expect(option_locator).to_be_visible(timeout=5000)
         option_locator.click(force=True)

    def input_field(self, value_locator, value):
        self.close_telegram_modal()
        value_locator.click()
        value_locator.fill(value)

    def file_upload(self, file_locator):
        self.close_telegram_modal()
        assert TEST_PDF_PATH.exists(), f"Test PDF not found at {TEST_PDF_PATH}"
        file_locator.set_input_files(str(TEST_PDF_PATH))



    def cav_selection(self, locator, dropdown_locator, option_locator):
        self.close_telegram_modal()
        locator.click()
        expect(dropdown_locator).to_be_visible(timeout=5000)
        dropdown_locator.check()
        option_locator.click()


