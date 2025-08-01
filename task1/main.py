from scraper import Scraper, Product

if __name__ == "__main__":
    CATEGORY_URL = "https://www.vendr.com/categories/data-analytics-and-management"
    CATEGORY_NAME = "Data Analytics and Management"

    scraper = Scraper()
    subcategories = scraper.get_subcategories(CATEGORY_URL)

    if not subcategories:
        print("No subcategories found.")
        exit(1)

    print(f"Found {len(subcategories)} subcategories.")
    first_subcat = subcategories[0]
    print(f"Parsing products from: {first_subcat}")

    product_previews = scraper.get_all_product_links(first_subcat, CATEGORY_NAME)
    print(f"Found {len(product_previews)} products. Getting details for first 5...\n")

    for preview in product_previews[:5]:
        product = scraper.parse_product_page(preview['url'], preview['category'])
        print(product)
        print("-" * 40)
