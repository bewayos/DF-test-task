import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://books.toscrape.com")

# Category URLs (for manual queue or debug mode)
DEFAULT_CATEGORIES = [
    f"{BASE_URL}/catalogue/category/books/poetry_23/index.html",
    f"{BASE_URL}/catalogue/category/books/travel_2/index.html",
]

# Number of processes
NUM_PROCESSES = int(os.getenv("NUM_PROCESSES", "3"))

HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

# Playwright default timeout
TIMEOUT = int(os.getenv("TIMEOUT", "10000"))  # in milliseconds
