import re
import time
import random

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

        # по 5 ссылок на один браузер
        for chunk_start in range(0, len(urls), 5):

            chunk = urls[chunk_start:chunk_start + 5]

            print(
                f"\n========== Пакет "
                f"{chunk_start + 1}-{chunk_start + len(chunk)} =========="
            )

            browser = p.chromium.launch(
                headless=False,
                slow_mo=random.randint(300, 800),
                args=[
                    "--disable-blink-features=AutomationControlled"
                ]
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

                    # имитация человека
                    page.mouse.move(
                        random.randint(100, 500),
                        random.randint(100, 500)
                    )

                    page.wait_for_timeout(
                        random.randint(7000, 15000)
                    )

                    # проверяем отсутствие цены
                    no_price = page.locator(
                        "span.HotelPriceContent_priceTextNoPrice__dfnkt"
                    )

                    if no_price.count() > 0:

                        text = no_price.first.text_content()

                        if text and "Нет цены" in text:

                            print("Нет цены")

                            continue

                    # основной селектор цены
                    price_locator = page.locator(
                        "span.HotelPriceContent_priceText__UM8xn"
                    ).first

                    price_locator.wait_for(
                        state="visible",
                        timeout=30000
                    )

                    text = price_locator.text_content()

                    if not text:
                        raise Exception("Цена не найдена")

                    price = extract_price(text)

                    if not price:
                        raise Exception("Не удалось распарсить цену")

                    print(f"Цена: {price} ₽")

                    results.append({
                        "url": url,
                        "price": price
                    })

                except Exception as e:

                    print(f"Ошибка: {e}")

                finally:

                    page.close()

                # обычная пауза между запросами
                pause = random.randint(8000, 20000)

                print(
                    f"Ждем {pause / 1000:.1f} сек..."
                )

                time.sleep(pause / 1000)

            browser.close()

            # длинная пауза между пакетами
            if chunk_start + 5 < len(urls):

                big_pause = random.randint(30, 60)

                print(
                    f"\nПауза между пакетами "
                    f"{big_pause} сек..."
                )

                time.sleep(big_pause)

    return results