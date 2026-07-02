import json
import os
from datetime import datetime

FILE = "prices.json"


def load_history():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # защита от старого формата
        if isinstance(data, list):
            return data
        return []

    except:
        return []


def save_history(prices):
    history = load_history()

    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "prices": prices
    }

    history.append(snapshot)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def get_last_snapshot():
    history = load_history()

    if not history:
        return None

    last = history[-1]

    # 🔥 защита от битых данных
    if not isinstance(last, dict):
        return None

    return last.get("prices", [])


def compare_with_last(current_prices):
    last = get_last_snapshot()

    if not last:
        return []

    last_map = {x["date"]: x["price"] for x in last if isinstance(x, dict)}

    changes = []

    for item in current_prices:
        date = item["date"]

        if date in last_map:
            diff = item["price"] - last_map[date]

            if diff != 0:
                changes.append({
                    "date": date,
                    "old": last_map[date],
                    "new": item["price"],
                    "diff": diff,
                    "url": item["url"]
                })

    return changes