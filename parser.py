import re
from playwright.sync_api import sync_playwright


def get_month_prices(urls):

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        for url in urls:

            try:

                print(f"\nПроверяем: {url}")

                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                # Даём странице время загрузить данные
                page.wait_for_timeout(5000)

                price_locator = page.locator(
                    "span.HotelPriceContent_priceText__UM8xn"
                ).first

                text = price_locator.text_content()

                if not text:
                    raise Exception("Цена не найдена")

                price = int(
                    re.sub(
                        r"[^\d]",
                        "",
                        text
                    )
                )

                print(f"Цена: {price} ₽")

                results.append({
                    "url": url,
                    "price": price
                })

            except Exception as e:

                print(f"Ошибка: {e}")

        browser.close()

    return results