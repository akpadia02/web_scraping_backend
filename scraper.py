import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

URL = "https://bullions.co.in/"


def scrape_bullions():

    res = requests.get(URL, headers=HEADERS, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    data = {}

    table = soup.find("table")

    if not table:
        print("❌ Bullions table not found")
        return {}

    rows = table.find_all("tr")[1:]

    gold_prices = {}

    for row in rows:

        cols = row.find_all("td")

        if len(cols) >= 2:

            name = cols[0].text.strip().lower()
            price = cols[1].text.strip()

            # Collect gold types
            if "gold" in name:
                gold_prices[name] = price

            # Silver (sometimes appears)
            if "silver" in name:
                data["silver"] = {
                    "price": price,
                    "unit": "INR/kg"
                }

    # Add gold as one object
    if gold_prices:
        data["gold"] = {
            "types": gold_prices,
            "unit": "INR/10g"
        }

    print("✅ FINAL DATA:", data)

    return data
