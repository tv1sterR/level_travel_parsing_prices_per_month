import matplotlib.pyplot as plt
import os
from datetime import datetime


def save_price_chart(prices):
    if not prices:
        return None

    # сортируем на всякий случай
    prices = sorted(prices, key=lambda x: x["date"])

    dates = [p["date"] for p in prices]
    values = [p["price"] for p in prices]

    min_price = min(values)
    max_price = max(values)
    avg_price = sum(values) / len(values)

    min_index = values.index(min_price)

    plt.figure(figsize=(13, 6))

    # ===== линия цены =====
    plt.plot(dates, values, marker="o", linewidth=2, label="Цена")

    # ===== минимум =====
    plt.scatter(
        dates[min_index],
        min_price,
        color="green",
        s=140,
        label="Минимум"
    )

    # ===== средняя линия =====
    plt.axhline(
        avg_price,
        color="orange",
        linestyle="--",
        linewidth=2,
        label=f"Средняя ({int(avg_price)} ₽)"
    )

    # ===== зона "выгодных дат" =====
    threshold = min_price * 1.05  # +5% от минимума

    plt.fill_between(
        dates,
        values,
        threshold,
        where=[v <= threshold for v in values],
        color="green",
        alpha=0.15,
        label="Выгодные даты"
    )

    # ===== подписи значений =====
    for x, y in zip(dates, values):
        plt.text(
            x,
            y,
            str(y),
            fontsize=8,
            ha="center",
            va="bottom"
        )

    # ===== оформление =====
    plt.title("Динамика цен (умный анализ)", fontsize=15)
    plt.xlabel("Дата вылета")
    plt.ylabel("Цена (₽)")
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.legend()

    plt.tight_layout()

    # ===== сохранение =====
    filename = f"price_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.abspath(filename)

    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()

    # ===== проверка файла =====
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        print("❌ Ошибка: график не сохранился")
        return None

    print("📈 График создан:", path)
    return path