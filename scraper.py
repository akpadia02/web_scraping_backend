import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
import re


# ---------------- LOGGING ----------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------- CONSTANTS ----------------

URL = "https://commoditiescontrol.com/eagritrader/revamp/long_short_details.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

TIMEOUT = 15


# ---------------- HELPERS ----------------

def clean_text(text):
    """
    Remove extra spaces and newlines
    """
    return re.sub(r"\s+", " ", text).strip()


def get_latest_value(text):
    """
    Extract first number from multiple values
    Example: '312.2 307.3' → '312.2'
    """
    parts = text.split()
    return parts[0] if parts else ""


def extract_expiry(text):
    """
    Extract expiry month from name
    Example: 'gold exp: apr-26' → 'apr-26'
    """
    match = re.search(r"exp:\s*([a-zA-Z0-9-]+)", text)
    return match.group(1) if match else ""


# ---------------- SCRAPER ----------------

def scrape_commodities():

    logger.info("Starting scraping...")

    try:
        res = requests.get(URL, headers=HEADERS, timeout=TIMEOUT)
        res.raise_for_status()
        logger.info("Website loaded")

    except Exception as e:
        logger.error(f"Request failed: {e}")
        return {}


    soup = BeautifulSoup(res.text, "html.parser")

    table = soup.find("table")

    if not table:
        logger.error("No table found")
        return {}


    rows = table.find_all("tr")[1:]

    data = {}


    for row in rows:

        cols = row.find_all("td")

        if len(cols) < 5:
            continue


        try:
            raw_name = clean_text(cols[0].text)

            if not raw_name:
                continue


            # Remove expiry text completely from name
            # Remove expiry part like " exp: feb-26"
            name = re.sub(r"\s+exp:.*$", "", raw_name, flags=re.IGNORECASE).strip().lower()




            price = get_latest_value(clean_text(cols[1].text))
            change = get_latest_value(clean_text(cols[2].text))
            high = get_latest_value(clean_text(cols[3].text))
            low = get_latest_value(clean_text(cols[4].text))


            data[name] = {
                "price": price,
                "change": change,
                "high": high,
                "low": low,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }


        except Exception as e:
            logger.warning(f"Row skipped: {e}")
            continue


    logger.info(f"Scraping done. Records: {len(data)}")

    return data


# ---------------- API WRAPPER ----------------

def scrape_all():

    return scrape_commodities()
