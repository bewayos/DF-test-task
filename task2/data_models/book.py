from dataclasses import dataclass

@dataclass
class Book:
    title: str
    price: str
    rating: str
    availability: str
    image_url: str
    description: str
    category: str
    upc: str
    product_type: str
    price_excl_tax: str
    price_incl_tax: str
    tax: str
    num_reviews: str
