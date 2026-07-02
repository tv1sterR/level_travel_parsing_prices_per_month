import json

FILE = "prices.json"


def save_prices(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_prices():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def compare_prices(old, new):
    if not old:
        print("\n📦 Нет прошлых данных для сравнения")
        return

    old_map = {x["url"]: x["price"] for x in old}

    print("\n========================")
    print("ИЗМЕНЕНИЯ ЦЕН")
    print("========================")

    for item in new:
        url = item["url"]
        price = item["price"]

        if url in old_map:
            diff = price - old_map[url]

            if diff != 0:
                sign = "+" if diff > 0 else ""
                print(f"{url}")
                print(f"{old_map[url]} → {price} ({sign}{diff})\n")