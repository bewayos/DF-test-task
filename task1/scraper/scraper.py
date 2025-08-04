from .http_client import HttpClient
from .link_extractor import LinkExtractor
from .product_parser import ProductParser
from .models import Product


class Scraper:
    def __init__(self, client: HttpClient):
        self.client = client
        self.link_extractor = LinkExtractor(client)
        self.product_parser = ProductParser(client)

    def get_all_products(self, category_url: str, category_name: str) -> list[Product]:
        products = []

        subcategories = self.link_extractor.get_subcategories(category_url)

        for subcat_url in subcategories:
            product_links = self.link_extractor.get_all_product_links(subcat_url, category_name)

            for info in product_links:
                product = self.product_parser.parse_product_page(info["url"], category_name, info)
                if product:
                    products.append(product)

        return products
