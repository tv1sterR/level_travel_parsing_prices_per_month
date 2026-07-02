from playwright.sync_api import sync_playwright

URL = "https://level.travel/hotels/15568-Labranda_Mares_Marmaris_Ex_Grand_Yazici_Mares_Hotel?ref_content=wishlist&start_date=2026-07-19&nights=7&search_type=package&adults=2&from=Moscow-RU"


def handle_response(response):
    try:

        if "search_calendar_start_date" in response.url:

            print("\nURL:")
            print(response.url)

            print("\nSTATUS:")
            print(response.status)

            print("\nBODY:")
            print(response.text())

    except Exception as e:
        print(e)


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.on("response", handle_response)

    page.goto(
        URL,
        wait_until="domcontentloaded"
    )

    page.wait_for_timeout(20000)

    browser.close()