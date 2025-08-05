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

STOP_SIGNAL = "__STOP__"

# Playwright default timeout
TIMEOUT = int(os.getenv("TIMEOUT", "10000"))  # in milliseconds

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5434"))
DB_NAME = os.getenv("DB_NAME", "books")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "yourpassword")

# Simulate crash in one scraper process for testing ProcessManager
SIMULATE_CRASH = os.getenv("SIMULATE_CRASH", "false").lower() == "true"