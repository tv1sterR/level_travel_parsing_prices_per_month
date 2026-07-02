from datetime import datetime, timedelta

from config import TOUR_URL, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from url_generator import generate_month_urls
from parser import get_month_prices

from prices_json import save_prices, load_prices, compare_prices
from telegram import TelegramNotifier


def input_date(prompt):
    while True:
        try:
            date_str = input(prompt + " (YYYY-MM-DD): ").strip()
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("❌ Неверный формат даты. Пример: 2026-07-01")


def generate_dates(start_date, end_date):
    dates = []
    current = start_date

    while current <= end_date:
        dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    return dates


def main():

    print("\n🚀 Level Travel мониторинг цен\n")

    # ввод диапазона дат
    start_date = input_date("Введите дату С")
    end_date = input_date("Введите дату ПО")

    if end_date < start_date:
        print("❌ Ошибка: дата 'по' меньше даты 'с'")
        return

    print(f"\n📅 Период: {start_date} → {end_date}")

    # генерация дат
    dates = generate_dates(start_date, end_date)

    # генерация URL
    urls = generate_month_urls(TOUR_URL, dates)

    print(f"\n🔎 Всего проверок: {len(urls)}")

    # парсинг
    prices = get_month_prices(urls)

    print("\n========================")
    print("РЕЗУЛЬТАТ")
    print("========================")

    if not prices:
        print("❌ Нет данных")
        return

    for item in prices:
        print(f"{item['date']} | {item['price']} ₽ | {item['url']}")

    # лучшая цена сейчас
    best = min(prices, key=lambda x: x["price"])

    print("\n========================")
    print("МИНИМАЛЬНАЯ ЦЕНА")
    print("========================")

    print(f"{best['date']} | {best['price']} ₽")
    print(best["url"])

    # загрузка старых данных (защита от кривого JSON)
    old_prices = load_prices()

    if isinstance(old_prices, str):
        old_prices = []

    # сравнение
    compare_prices(old_prices, prices)

    # сохранение новых данных
    save_prices(prices)

    # Telegram уведомления
    bot = TelegramNotifier(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

    old_best = None

    if old_prices:
        try:
            old_best = min(old_prices, key=lambda x: x["price"])
        except Exception:
            old_best = None

    bot.send_price_report(prices, best, old_best)


if __name__ == "__main__":
    main()