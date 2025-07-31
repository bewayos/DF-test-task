from scraper import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    sub_url = "https://www.vendr.com/categories/devops/application-development"
    all_products = scraper.get_all_product_links(sub_url, "DevOps")

    for p in all_products:
        print(p)
