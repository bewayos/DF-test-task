import requests
import logging
from typing import Optional

from task1.config import DEFAULT_HEADERS

class HttpClient:
    def get(self, url: str) -> Optional[requests.Response]:
        try:
            logging.debug(f"GET {url}")
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
            response.raise_for_status()
            return response
        except Exception as e:
            logging.error(f"GET failed for {url}: {e}")
            return None
