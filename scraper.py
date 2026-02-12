"""
================================================================================
FILE: scraper.py
RESPONSIBILITY:
    Web scraper for commodity market data from Indian commodities exchange.
    Fetches real-time prices of metals (gold, silver, copper) and other commodities.
    Parses HTML table data and extracts price, change, high, and low values.
    Provides clean data formatting and error handling with logging.
================================================================================
"""

# Import requests library for making HTTP requests to websites
import requests

# Import logging module for tracking scraper execution and errors
import logging

# Import BeautifulSoup for parsing HTML content
from bs4 import BeautifulSoup

# Import datetime to add timestamps to scraped data
from datetime import datetime

# Import regular expressions module for text pattern matching and cleaning
import re


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
# PURPOSE: Setup logging system to track scraper operations
# Log Format: timestamp | log level | message

logging.basicConfig(
    # Set minimum log level to INFO (shows INFO, WARNING, ERROR messages)
    level=logging.INFO,
    # Define log message format with timestamp, level, and message
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Create logger instance for this module
logger = logging.getLogger(__name__)


# ============================================================================
# CONSTANTS - SOURCE AND CONFIGURATION
# ============================================================================
# Target website URL for fetching commodity data
URL = "https://commoditiescontrol.com/eagritrader/revamp/long_short_details.php"

# HTTP headers to mimic a real browser request (bypass bot detection)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Request timeout in seconds (abort if server takes longer)
TIMEOUT = 15


# ============================================================================
# HELPER FUNCTIONS - TEXT PROCESSING AND DATA EXTRACTION
# ============================================================================

def clean_text(text):
    """
    FUNCTION: clean_text
    PURPOSE: Remove extra whitespace and newlines from text
    PARAMETER: text - raw text string that may contain extra spaces/newlines
    RETURNS: cleaned text string with normalized spacing
    LOGIC: Use regex to collapse multiple spaces into single space, then strip edges
    """
    # Replace multiple whitespace characters (spaces, tabs, newlines) with single space
    return re.sub(r"\s+", " ", text).strip()


def get_latest_value(text):
    """
    FUNCTION: get_latest_value
    PURPOSE: Extract first numeric value from text (for current price)
    PARAMETER: text - string that may contain multiple space-separated values
    RETURNS: first numeric value as string
    EXAMPLE: Input '312.2 307.3 310.5' returns '312.2'
    LOGIC: Split text by spaces and return first element if it exists
    """
    # Split text by whitespace to separate multiple values
    parts = text.split()
    # Return first value if list is not empty, otherwise return empty string
    return parts[0] if parts else ""


def extract_expiry(text):
    """
    FUNCTION: extract_expiry
    PURPOSE: Extract contract expiry month from commodity name
    PARAMETER: text - commodity name with embedded expiry info
    RETURNS: expiry month string
    EXAMPLE: Input 'gold exp: apr-26' returns 'apr-26'
    LOGIC: Use regex to match pattern "exp: XXX-XX" and extract the month part
    """
    # Search for pattern "exp: " followed by alphanumeric month-year format
    match = re.search(r"exp:\s*([a-zA-Z0-9-]+)", text)
    # Return matched group if found, otherwise return empty string
    return match.group(1) if match else ""


# ============================================================================
# MAIN SCRAPER FUNCTION
# ============================================================================

def scrape_commodities():
    """
    FUNCTION: scrape_commodities
    PURPOSE: Main scraping logic - fetch and parse commodity data from website
    RETURNS: Dictionary with commodity names as keys and price data as values
    STRUCTURE: {
        'gold': {'price': '55000', 'change': '100', 'high': '55500', 'low': '54800', 'updated_at': 'timestamp'},
        'silver': {...}
    }
    """
    
    # Log start of scraping operation
    logger.info("Starting scraping...")
    
    # TRY BLOCK: Attempt to fetch website data
    try:
        # Make HTTP GET request to the commodity data source with timeout
        res = requests.get(URL, headers=HEADERS, timeout=TIMEOUT)
        
        # Raise exception if HTTP status code indicates error (4xx, 5xx)
        res.raise_for_status()
        
        # Log successful website load
        logger.info("Website loaded")

    # EXCEPT BLOCK: Handle request errors (network issues, timeouts, invalid responses)
    except Exception as e:
        # Log the error with details
        logger.error(f"Request failed: {e}")
        # Return empty dictionary if request fails
        return {}

    
    # Parse HTML content using BeautifulSoup with html.parser
    soup = BeautifulSoup(res.text, "html.parser")
    
    # Find the HTML table containing commodity data
    table = soup.find("table")
    
    # Check if table was found in the HTML
    if not table:
        # Log error if no table exists
        logger.error("No table found")
        # Return empty dictionary
        return {}

    
    # Extract all rows from table, skip first row (header) with [1:]
    rows = table.find_all("tr")[1:]
    
    # Initialize empty dictionary to store commodity data
    data = {}
    
    
    # LOOP: Iterate through each row in the table
    for row in rows:
        
        # Find all table cells (td elements) in the current row
        cols = row.find_all("td")
        
        # Verify that row has at least 5 columns (name, price, change, high, low)
        if len(cols) < 5:
            # Skip this row if it doesn't have enough columns
            continue
        
        
        # TRY BLOCK: Extract and process data from this row
        try:
            # Extract and clean commodity name from first column
            raw_name = clean_text(cols[0].text)
            
            # Skip this row if commodity name is empty
            if not raw_name:
                continue
            
            
            # Remove expiry text completely from name using regex substitution
            # Example: "gold exp: feb-26" becomes "gold"
            name = re.sub(r"\s+exp:.*$", "", raw_name, flags=re.IGNORECASE).strip().lower()
            
            
            # Extract latest price value from second column
            price = get_latest_value(clean_text(cols[1].text))
            
            # Extract price change value from third column  
            change = get_latest_value(clean_text(cols[2].text))
            
            # Extract high price from fourth column
            high = get_latest_value(clean_text(cols[3].text))
            
            # Extract low price from fifth column
            low = get_latest_value(clean_text(cols[4].text))
            
            
            # Store extracted commodity data in dictionary with all metrics
            data[name] = {
                # Current trading price as string
                "price": price,
                # Price change value as string
                "change": change,
                # Highest price reached as string
                "high": high,
                # Lowest price reached as string
                "low": low,
                # Timestamp of when data was last updated
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        
        # EXCEPT BLOCK: Handle errors in data extraction for this row
        except Exception as e:
            # Log warning that this row was skipped due to error
            logger.warning(f"Row skipped: {e}")
            # Continue to next row without stopping the entire scrape
            continue
    
    
    # Log completion message with count of successfully scraped commodities
    logger.info(f"Scraping done. Records: {len(data)}")
    
    # Return final data dictionary containing all commodities
    return data


# ============================================================================
# API WRAPPER FUNCTION
# ============================================================================

def scrape_all():
    """
    FUNCTION: scrape_all
    PURPOSE: Wrapper function that calls the main scraper
    RETURNS: Commodity data dictionary
    USE CASE: Called by Flask app.py to fetch data for API endpoints
    """
    
    # Call main scraper function and return its result
    return scrape_commodities()
