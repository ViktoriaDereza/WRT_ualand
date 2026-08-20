import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playwright.sync_api import expect
from pages.base_bid_page import BidCreate



def test_bids_created(logged_in_bidder1, api_auction_publish):
    prozorroId, draft_id = api_auction_publish
    page = BidCreate(logged_in_bidder1, prozorroId)
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
    #expect(page.page.locator(f"text={prozorroId}")).to_be_visible()
    expect(page.page.locator("body")).to_contain_text(prozorroId)


def test_invoice_pdf_download(logged_in_bidder2, api_auction_publish):
    # Uses bidder2 (rather than bidder1, already used by test_bids_created
    # above) so this test submits its own application against the shared
    # module-scoped auction instead of re-submitting bidder1's profile,
    # which the platform doesn't allow for the same auction.
    prozorroId, draft_id = api_auction_publish
    page = BidCreate(logged_in_bidder2, prozorroId)
    page.open_bid_page()
    page.loc_take_part.scroll_into_view_if_needed()
    page.loc_take_part.click()
    page.select_from_dropdown(page.loc_drdwn_profile, page.loc_select_profile)
    page.input_field(page.loc_bid_price, "11000")
    page.loc_continue_btn.click()
    page.check_and_verify(page.loc_first_chbox)
    page.check_and_verify(page.loc_second_chbox)
    page.loc_publish_btn.click()
    # The post-publish redirect to /my-applications occasionally takes
    # longer than the default 5s under QA-environment load; give it the
    # same generous allowance check_and_verify already uses above.
    expect(page.page).to_have_url("https://qa.ualand.space/my-applications", timeout=15000)
    expect(page.page.locator("body")).to_contain_text(prozorroId)

    application_link = page.page.get_by_role("link", name=prozorroId)
    view_application_btn = application_link.locator(
        "xpath=following::button[normalize-space()='Переглянути заяву'][1]"
    )
    view_application_btn.click()

    # The application modal has two "Сформувати рахунок" buttons (one for
    # the registration fee, one for the guarantee fee) - .first targets the
    # registration-fee invoice.
    generate_invoice_btn = page.page.get_by_role("button", name="Сформувати рахунок").first
    expect(generate_invoice_btn).to_be_visible()

    with page.page.expect_download() as download_info:
        generate_invoice_btn.click()
    download = download_info.value

    assert download.suggested_filename.lower().endswith(".pdf"), (
        f"Expected a PDF invoice, got filename: {download.suggested_filename}"
    )
    download_path = download.path()
    assert download_path is not None, "Download did not save to disk"
    assert download_path.stat().st_size > 0, "Downloaded invoice file is empty"
    with open(download_path, "rb") as f:
        assert f.read(5) == b"%PDF-", "Downloaded file is not a valid PDF"


