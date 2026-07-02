import requests


class TelegramNotifier:

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"

    # =========================
    # 📩 ОТПРАВКА СООБЩЕНИЙ
    # =========================
    def send_message(self, text: str):

        # Telegram лимит ~4096 символов
        chunks = [text[i:i + 3500] for i in range(0, len(text), 3500)]

        for chunk in chunks:
            try:
                r = requests.post(
                    f"{self.base_url}/sendMessage",
                    data={
                        "chat_id": self.chat_id,
                        "text": chunk,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": True
                    },
                    timeout=10
                )

                if r.status_code != 200:
                    print("❌ Telegram error:", r.text)

            except Exception as e:
                print("❌ Telegram exception:", e)

    # =========================
    # 🖼 ОТПРАВКА ФОТО (ГРАФИК)
    # =========================
    def send_photo(self, image_path, caption=None):
        try:
            with open(image_path, "rb") as photo:
                resp = requests.post(
                    f"{self.base_url}/sendPhoto",
                    data={
                        "chat_id": self.chat_id,
                        "caption": caption or ""
                    },
                    files={
                        "photo": photo
                    },
                    timeout=20
                )

            if not resp.ok:
                print("Telegram API error:", resp.text)

        except Exception as e:
            print("Telegram photo error:", e)

    # =========================
    # 📊 ПОЛНЫЙ ОТЧЁТ
    # =========================
    def send_full_report(self, prices, best):

        # ===== ТОП-5 =====
        top = sorted(prices, key=lambda x: x["price"])[:5]

        msg = "🔥 <b>ТОП-5 выгодных дат</b>\n\n"

        for i, p in enumerate(top, 1):
            msg += (
                f"{i}. 📅 {p['date']} — <b>{p['price']} ₽</b>\n"
            )

        self.send_message(msg)

        # ===== ВСЕ ЦЕНЫ =====
        msg = "✈️ <b>Все найденные цены</b>\n\n"

        for p in prices:
            msg += (
                f"📅 {p['date']}\n"
                f"💰 {p['price']} ₽\n"
                f"🔗 {p['url']}\n\n"
            )

        self.send_message(msg)

        # ===== ЛУЧШАЯ ЦЕНА =====
        best_msg = (
            "🏆 <b>Лучшая цена</b>\n\n"
            f"📅 {best['date']}\n"
            f"💰 <b>{best['price']} ₽</b>\n"
            f"🔗 {best['url']}"
        )

        self.send_message(best_msg)