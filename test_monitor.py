from config import TOUR_URL, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from url_generator import generate_month_urls
from parser import get_month_prices
from telegram import TelegramNotifier

from datetime import datetime, timedelta


def generate_test_dates():
    """Берём 3 дня для теста"""
    start = datetime(2026, 7, 1).date()

    return [
        (start + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(3)
    ]


def main():

    print("🚀 ТЕСТ МОНИТОРИНГА (Level Travel)\n")

    # 👉 ВАЖНО: теперь передаём dates
    dates = generate_test_dates()
    urls = generate_month_urls(TOUR_URL, dates)

    print(f"🔎 Тестируем {len(urls)} URL\n")

    prices = get_month_prices(urls)

    if not prices:
        print("❌ Нет данных")
        return

    print("\n📊 РЕЗУЛЬТАТ:")
    for p in prices:
        print(f"{p['price']} ₽ | {p['url']}")

    best = min(prices, key=lambda x: x["price"])

    print("\n🏆 ЛУЧШАЯ ЦЕНА:")
    print(best["price"], "₽")
    print(best["url"])

    bot = TelegramNotifier(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

    bot.send_message(
        f"🔥 ТЕСТ МОНИТОРИНГА\n\n"
        f"💰 Цена: {best['price']} ₽\n"
        f"📅 Дней проверено: {len(urls)}\n"
        f"🔗 {best['url']}"
    )


if __name__ == "__main__":
    main()