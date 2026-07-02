from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def generate_month_urls(base_url: str, dates: list[str]):
    """
    Генерирует список URL с подстановкой разных start_date
    """

    parsed = urlparse(base_url)
    query = parse_qs(parsed.query)

    urls = []

    for date in dates:

        # копируем query, чтобы не мутировать оригинал
        new_query = query.copy()

        # подставляем дату
        new_query["start_date"] = [date]

        # собираем URL обратно
        encoded_query = urlencode(new_query, doseq=True)

        new_url = urlunparse(
            parsed._replace(query=encoded_query)
        )

        urls.append(new_url)

    return urls