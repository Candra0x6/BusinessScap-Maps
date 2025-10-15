"""
Configuration file for Google Maps Scraper
Adjust these settings according to your needs
"""

# Scraping Settings
HEADLESS_MODE = False  # Set to True to run browser in background
DELAY_BETWEEN_ACTIONS = 3  # Seconds to wait between actions
MAX_RESULTS_PER_KEYWORD = 50  # Maximum businesses to scrape per keyword
MAX_SCROLL_ATTEMPTS = 10  # Maximum times to scroll the results panel

# Browser Settings
WINDOW_SIZE = "1920,1080"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# Timeout Settings
PAGE_LOAD_TIMEOUT = 10  # Seconds to wait for page elements
IMPLICIT_WAIT = 10  # Seconds for implicit waits

# Output Settings
OUTPUT_DIRECTORY = "output"
LOG_FILE = "scraper_log.txt"
GENERATE_SUMMARY = True  # Generate summary report after scraping

# Retry Settings
MAX_RETRIES = 2  # Number of retry attempts for failed operations
RETRY_DELAY = 5  # Seconds to wait before retrying

# Data Fields
REQUIRED_FIELDS = [
    'Business Name',
    'Description',
    'Website',
    'Phone',
    'Google Maps Link'
]
