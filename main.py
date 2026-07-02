from config import TOUR_URL
from url_generator import generate_month_urls
from parser import get_month_prices

urls = generate_month_urls(TOUR_URL)

prices = get_month_prices(urls)

print("\n========================")
print("РЕЗУЛЬТАТ")
print("========================")

for item in prices:
    print(
        f"{item['price']} ₽ | {item['url']}"
    )

if prices:

    best = min(
        prices,
        key=lambda x: x["price"]
    )

    print("\n========================")
    print("МИНИМАЛЬНАЯ ЦЕНА")
    print("========================")

    print(f"{best['price']} ₽")
    print(best["url"])