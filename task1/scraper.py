from dataclasses import dataclass
import requests
from lxml import html
import logging

# log settings
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")

@dataclass
class Product:
    name: str
    category: str
    price_range: str
    description: str


class Scraper:
    def get_subcategories(self, category_url: str) -> list[str]:
        """Returns a list URLs of all subcategories."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/122.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            }

            logging.debug(f"GET {category_url}")
            response = requests.get(category_url, headers=headers, timeout=10)
            response.raise_for_status()

            tree = html.fromstring(response.content)

            # Find all links that lead to deeper subcategories
            links = tree.xpath('//a[contains(@href, "/categories/") and h2]/@href')
            logging.debug(f"Found {len(links)} raw category links")

            subcategory_urls = []
            for href in links:
                logging.debug(f"Raw href: {href}")

                if "page=" in href:
                    href = href.split("?")[0]
                    logging.debug(f"Cleaned href: {href}")

                if href.startswith("/categories/"):
                    full_url = 'https://www.vendr.com' + href
                    logging.debug(f"Accepted: {full_url}")
                    if full_url not in subcategory_urls:
                        subcategory_urls.append(full_url)



            logging.info(f"Found {len(subcategory_urls)} unique subcategories")
            return subcategory_urls

        except Exception as e:
            logging.error(f"get_subcategories failed: {e}")
            return []

def get_product_links(self, subcategory_url: str, category: str) -> list[dict]:
    """
    Parses the 1st page of a subcategory.
    Returns a list of dictionaries with name, url, category
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        }

        logging.debug(f"GET {subcategory_url}")
        response = requests.get(subcategory_url, headers=headers, timeout=10)
        response.raise_for_status()

        tree = html.fromstring(response.content)

        product_cards = tree.xpath('//a[contains(@href, "/products/")]')
        logging.debug(f"Found {len(product_cards)} product links on page")

        results = []
        for card in product_cards:
            href = card.get("href")
            name = card.xpath('.//h2/text()') or card.xpath('.//span/text()')
            if not href or not name:
                continue

            full_url = "https://www.vendr.com" + href.split("?")[0]
            results.append({
                "name": name[0].strip(),
                "url": full_url,
                "category": category
            })

        logging.info(f"Extracted {len(results)} products from page 1 of {subcategory_url}")
        return results

    except Exception as e:
        logging.error(f"get_product_links failed: {e}")
        return []

