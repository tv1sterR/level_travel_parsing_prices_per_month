from datetime import datetime
from datetime import timedelta
from urllib.parse import (
    urlparse,
    parse_qs,
    urlencode,
    urlunparse
)


def generate_month_urls(base_url: str):

    parsed = urlparse(base_url)

    query = parse_qs(parsed.query)

    start_date = query["start_date"][0]

    dt = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    first_day = dt.replace(day=1)

    urls = []

    current = first_day

    while current.month == dt.month:

        query["start_date"] = [
            current.strftime("%Y-%m-%d")
        ]

        new_query = urlencode(
            query,
            doseq=True
        )

        new_url = urlunparse(
            parsed._replace(query=new_query)
        )

        urls.append(new_url)

        current += timedelta(days=1)

    return urls