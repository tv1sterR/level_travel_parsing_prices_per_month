from playwright.sync_api import sync_playwright

URL = "https://level.travel/hotels/15568-Labranda_Mares_Marmaris_Ex_Grand_Yazici_Mares_Hotel?ref_content=wishlist&start_date=2026-07-19&nights=7&search_type=package&adults=2&from=Moscow-RU"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        URL,
        wait_until="domcontentloaded"
    )

    page.wait_for_timeout(15000)

    elements = page.locator("text=220").all()

    print("Найдено:", len(elements))

    browser.close()