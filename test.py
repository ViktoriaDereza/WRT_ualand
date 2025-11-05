# from playwright.sync_api import sync_playwright
#
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False, slow_mo=500)
#     page = browser.new_page()
#     page.goto("https://qa.ualand.space/")
#     page.screenshot(path="hp.png")
#     #go_to_auctions_button = page.get_by_role("link", name = "Вхід")
#     #go_to_auctions_button.click()
#
#     page.locator("button:has-text('Вхід')").click()
#
#     page.locator("input[aria-invalid='false'][type='text']").fill("test@gmail.com")
#
#     browser.close()