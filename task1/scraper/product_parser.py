import logging
from lxml import html
from .models import Product

class ProductParser:
    def __init__(self, client):
        self.client = client

    def parse_product_page(self, url: str, category: str, base_info: dict) -> Product:
        response = self.client.get(url)
        if not response:
            return None

        tree = html.fromstring(response.content)

        try:
            name = tree.xpath('//h1[contains(@class, "rt-Heading")]/text()')[0].strip()
        except IndexError:
            name = base_info.get("name") or url.split("/")[-1].capitalize()

        try:
            paragraphs = tree.xpath('//p[contains(@class, "rt-Text")]/text()')
            description = " ".join(p.strip() for p in paragraphs if p.strip())
        except Exception as e:
            logging.warning(f"Description not found: {e}")
            description = base_info.get("description", "")

        median_price = self.parse_price(tree)

        return Product(
            name=name,
            category=category,
            median_price=median_price,
            description=description,
            url=url
        )

    def parse_price(self, tree: html.HtmlElement) -> str:
        try:
            price = tree.xpath('//span[contains(text(), "$") and contains(@class, "v-fw-700")]/text()')
            if price:
                return price[0].strip()
        except Exception as e:
            logging.warning(f"Price not found: {e}")
        return "Unknown"