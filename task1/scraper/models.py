from dataclasses import dataclass

@dataclass
class Product:
    name: str
    category: str
    median_price: str
    price_range: str
    description: str
    url: str