import re
import time
import random

from datetime import datetime
from playwright.sync_api import sync_playwright


USER_AGENTS = [
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/135.0.0.0 Safari/537.36"
    ),
]


def extract_price(text):

    digits = re.sub(r"[^\d]", "", text)

    if not digits:
        return None

    return int(digits)


def get_month_prices(urls):

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        for chunk_start in range(0, len(urls), 10):

            chunk = urls[chunk_start:chunk_start + 10]

            print(
                f"\n========== Пакет "
                f"{chunk_start + 1}-{chunk_start + len(chunk)} =========="
            )

            context = browser.new_context(
                viewport={
                    "width": random.randint(1280, 1600),
                    "height": random.randint(720, 900)
                },
                locale="ru-RU",
                user_agent=random.choice(USER_AGENTS)
            )

            for url in chunk:

                page = context.new_page()

                try:

                    print(f"\nПроверяем: {url}")

                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=90000
                    )

                    page.mouse.move(
                        random.randint(100, 800),
                        random.randint(100, 600)
                    )

                    page.wait_for_timeout(
                        random.randint(1500, 3000)
                    )

                    no_price = page.locator(
                        "span.HotelPriceContent_priceTextNoPrice__dfnkt"
                    )

                    if no_price.count() > 0:

                        text = no_price.first.text_content()

                        if text and "Нет цены" in text:

                            print("Нет цены")

                            page.close()

                            pause = random.randint(1500, 4000)

                            print(
                                f"Ждем {pause / 1000:.1f} сек..."
                            )

                            time.sleep(pause / 1000)

                            continue

                    price_locator = page.locator(
                        "span.HotelPriceContent_priceText__UM8xn"
                    ).first

                    price_locator.wait_for(
                        state="visible",
                        timeout=15000
                    )

                    text = price_locator.text_content()

                    if not text:
                        raise Exception(
                            "Цена не найдена"
                        )

                    price = extract_price(text)

                    def extract_date_from_url(url: str):
                        try:
                            # start_date=2026-07-19
                            import re
                            match = re.search(r"start_date=(\d{4}-\d{2}-\d{2})", url)
                            if match:
                                return match.group(1)
                        except:
                            pass

                        return None

                    if not price:
                        raise Exception(
                            "Не удалось распарсить цену"
                        )

                    print(f"Цена: {price} ₽")

                    results.append({
                        "url": url,
                        "price": price,
                        "date": extract_date_from_url(url)
                    })

                except Exception as e:

                    print(f"Ошибка: {e}")

                finally:

                    page.close()

                pause = random.randint(1500, 4000)

                print(
                    f"Ждем {pause / 1000:.1f} сек..."
                )

                time.sleep(pause / 1000)

            context.close()

            if chunk_start + 10 < len(urls):

                big_pause = random.randint(10, 20)

                print(
                    f"\nПауза между пакетами "
                    f"{big_pause} сек..."
                )

                time.sleep(big_pause)

        browser.close()

    return results