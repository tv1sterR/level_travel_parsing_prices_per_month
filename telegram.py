import requests


class TelegramNotifier:

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{token}/sendMessage"

    def _send(self, text):

        try:
            requests.post(
                self.url,
                data={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True
                },
                timeout=10
            )
        except Exception as e:
            print(f"❌ Telegram error: {e}")

    def send_price_report(self, prices, best, old_best=None):

        # ===== 1. ВСЕ ТУРЫ =====
        msg = "✈️ <b>Отчёт по турам</b>\n\n"

        for item in prices:
            msg += (
                f"📅 <b>{item['date']}</b>\n"
                f"💰 {item['price']} ₽\n"
                f"🔗 {item['url']}\n"
                f"----------------------\n"
            )

        self._send(msg)

        # ===== 2. ЛУЧШАЯ ЦЕНА =====
        best_msg = (
            "🔥 <b>Лучшая цена</b>\n\n"
            f"📅 {best['date']}\n"
            f"💰 <b>{best['price']} ₽</b>\n"
            f"🔗 {best['url']}\n"
        )

        # сравнение с прошлым запуском
        if old_best:
            diff = best["price"] - old_best["price"]

            best_msg += (
                "\n📊 <b>Изменение</b>\n"
                f"Было: {old_best['price']} ₽\n"
                f"Разница: {diff:+} ₽\n"
            )

        self._send(best_msg)