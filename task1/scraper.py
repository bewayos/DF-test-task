from dataclasses import dataclass
from typing import Optional
from lxml import html
import requests
import logging

# Logging config
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


@dataclass
class Product:
    name: str
    category: str
    median_price: str
    description: str
    url: str


class Scraper:
    BASE_URL = "https://www.vendr.com"

    def _get_headers(self) -> dict:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        }

    def get(self, url: str) -> Optional[requests.Response]:
        try:
            logging.debug(f"GET {url}")
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            return response
        except Exception as e:
            logging.error(f"GET failed for {url}: {e}")
            return None

    def get_subcategories(self, category_url: str) -> list[str]:
        response = self.get(category_url)
        if not response:
            return []

        tree = html.fromstring(response.content)
        links = tree.xpath('//a[contains(@href, "/categories/") and h2]/@href')

        subcategory_urls = []
        for href in links:
            if "page=" in href:
                href = href.split("?")[0]

            if href.startswith("/categories/"):
                full_url = self.BASE_URL + href
                if full_url not in subcategory_urls:
                    subcategory_urls.append(full_url)

        logging.info(f"Found {len(subcategory_urls)} unique subcategories")
        return subcategory_urls

    def get_product_links(self, subcategory_url: str, category: str) -> list[dict]:
        response = self.get(subcategory_url)
        if not response:
            return []

        tree = html.fromstring(response.content)
        product_cards = tree.xpath('//a[contains(@href, "/marketplace/")]')

        results = []
        for card in product_cards:
            href = card.get("href")
            name = card.xpath('.//span[contains(@class, "_cardTitle")]/text()')
            description = card.xpath('.//span[contains(@class, "_description")]/text()')

            if not href or not name:
                continue

            full_url = self.BASE_URL + href.split("?")[0]
            results.append({
                "name": name[0].strip(),
                "url": full_url,
                "category": category,
                "description": description[0].strip() if description else ""
            })

        logging.info(f"Extracted {len(results)} products from page 1 of {subcategory_url}")
        return results

    def get_all_product_links(self, subcategory_url: str, category: str) -> list[dict]:
        page = 1
        all_results = []

        while True:
            paginated_url = f"{subcategory_url}?page={page}"
            products = self.get_product_links(paginated_url, category)
            if not products:
                break

            all_results.extend(products)
            logging.info(f"Page {page}: {len(products)} products")
            page += 1

        logging.info(f"Total collected from {subcategory_url}: {len(all_results)} products")
        return all_results

    def parse_product_page(self, url: str, category: str) -> Optional[Product]:
        response = self.get(url)
        if not response:
            return None

        tree = html.fromstring(response.text)

        try:
            name = tree.xpath('//h1[contains(@class, "rt-Heading")]/text()')[0].strip()
        except IndexError:
            name = url.split("/")[-1].capitalize()

        try:
            paragraphs = tree.xpath('//p[contains(@class, "rt-Text")]/text()')
            description = " ".join(p.strip() for p in paragraphs if p.strip())
        except Exception as e:
            logging.warning(f"Description not found: {e}")
            description = ""


        median_price = self.parse_price(tree)

        return Product(
            name=name,
            category=category,
            median_price=median_price,
            description=description,
            url=url
        )


    @staticmethod
    def parse_price(tree: html.HtmlElement) -> str:
        try:
            price = tree.xpath('//span[contains(text(), "$") and contains(@class, "v-fw-700")]/text()')
            if price:
                return price[0].strip()
        except Exception as e:
            logging.warning(f"Price not found: {e}")
        return "Unknown"


