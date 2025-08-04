from lxml import html
import logging
from .models import Product

class LinkExtractor:
    def __init__(self, client):
        self.client = client

    def get_subcategories(self, category_url: str) -> list[str]:
        response = self.client.get(category_url)
        if not response:
            return []

        tree = html.fromstring(response.content)
        links = tree.xpath('//a[contains(@href, "/categories/") and h2]/@href')

        subcategory_urls = []
        for href in links:
            href = href.split("?")[0]
            if href.startswith("/categories/"):
                full_url = "https://www.vendr.com" + href
                if full_url not in subcategory_urls:
                    subcategory_urls.append(full_url)

        logging.info(f"Found {len(subcategory_urls)} unique subcategories")
        return subcategory_urls

    def get_product_links(self, subcategory_url: str, category: str) -> list[dict]:
        response = self.client.get(subcategory_url)
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

            full_url = "https://www.vendr.com" + href.split("?")[0]
            results.append({
                "name": name[0].strip(),
                "url": full_url,
                "category": category,
                "description": description[0].strip() if description else ""
            })

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
            page += 1

        logging.info(f"[LinkExtractor] Total collected from {subcategory_url}: {len(all_results)}")
        return all_results
