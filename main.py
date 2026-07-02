from datetime import datetime, timedelta, date
import time
import traceback
from urllib.parse import urlparse, parse_qs

from config import TOUR_URL, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from url_generator import generate_month_urls
from parser import get_month_prices

from prices_json import save_history, compare_with_last
from graph import save_price_chart
from telegram import TelegramNotifier


def input_date(prompt):
    while True:
        try:
            return datetime.strptime(
                input(prompt + " (YYYY-MM-DD): ").strip(),
                "%Y-%m-%d"
            ).date()
        except ValueError:
            print("❌ Неверный формат даты")


def generate_dates(start, end):
    dates = []
    cur = start

    while cur <= end:
        dates.append(cur.strftime("%Y-%m-%d"))
        cur += timedelta(days=1)

    return dates


def extract_base_date(url: str):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    if "start_date" not in query:
        raise ValueError("В URL нет start_date")

    return datetime.strptime(query["start_date"][0], "%Y-%m-%d").date()


def run_cycle(bot, start, end):

    dates = generate_dates(start, end)
    urls = generate_month_urls(TOUR_URL, dates)

    print(f"\n🔎 Проверяем: {len(urls)} дат")

    prices = get_month_prices(urls)

    if not prices:
        print("❌ Нет данных")
        bot.send_message("❌ Нет данных по турам")
        return

    prices = sorted(prices, key=lambda x: x["price"])
    best = prices[0]

    print("\n📊 РЕЗУЛЬТАТ:")
    for p in prices:
        print(f"{p['date']} | {p['price']} ₽")

    print("\n🔥 МИНИМУМ:")
    print(f"{best['date']} | {best['price']} ₽")

    save_history(prices)
    changes = compare_with_last(prices)

    bot.send_full_report(prices, best)

    if changes:
        msg = "📉 <b>Изменения цен</b>\n\n"
        for c in changes:
            msg += f"{c['date']}: {c['old']} → {c['new']} ({c['diff']:+})\n"
        bot.send_message(msg)

    chart_file = save_price_chart(prices)

    if chart_file:
        print("📈 График создан:", chart_file)
        bot.send_photo(chart_file, caption="📊 График цен по датам")


def main(auto=True):

    print("\n🚀 Level Travel мониторинг\n")

    bot = TelegramNotifier(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)

    # ===== AUTO MODE =====
    if auto:

        base_date = extract_base_date(TOUR_URL)

        start = base_date - timedelta(days=5)
        end = base_date + timedelta(days=5)

        print(f"🤖 AUTO режим включён")
        print(f"📅 Базовая дата тура: {base_date}")
        print(f"📅 Окно поиска: {start} → {end}")

        while True:
            try:
                print("\n==============================")
                print(f"⏱ Запуск: {datetime.now()}")
                print("==============================")

                run_cycle(bot, start, end)

            except Exception as e:
                print("❌ Ошибка:", e)
                traceback.print_exc()
                bot.send_message(f"❌ Ошибка:\n{e}")

            print("\n⏳ Ждём 40 минут...\n")
            time.sleep(40 * 60)

    # ===== MANUAL MODE =====
    else:

        start = input_date("Дата С")
        end = input_date("Дата ПО")

        if end < start:
            print("❌ Ошибка: дата ПО меньше даты С")
            return

        run_cycle(bot, start, end)


if __name__ == "__main__":
    main(auto=True)