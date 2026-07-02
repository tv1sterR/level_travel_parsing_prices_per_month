import json
import os

FILE_PATH = "prices.json"


def save_prices(prices):
    """
    Сохраняем текущие цены
    """
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(prices, f, ensure_ascii=False, indent=2)


def load_prices():
    """
    Загружаем прошлые цены
    """
    if not os.path.exists(FILE_PATH):
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        # защита от кривого формата
        if not isinstance(data, list):
            return []

        return data

    except Exception:
        return []


def compare_prices(old_prices, new_prices):
    """
    Сравнение цен между запусками
    """

    if not old_prices:
        print("\n🆕 Нет предыдущих данных для сравнения")
        return

    old_dict = {item["date"]: item for item in old_prices}

    changes = []

    for item in new_prices:
        date = item["date"]

        if date in old_dict:
            old_price = old_dict[date]["price"]
            new_price = item["price"]

            if old_price != new_price:
                diff = new_price - old_price

                changes.append({
                    "date": date,
                    "old": old_price,
                    "new": new_price,
                    "diff": diff
                })

    if not changes:
        print("\n✅ Изменений цен нет")
        return

    print("\n📊 ИЗМЕНЕНИЯ ЦЕН:")

    for c in changes:
        sign = "+" if c["diff"] > 0 else ""
        print(f"{c['date']}: {c['old']} → {c['new']} ({sign}{c['diff']})")