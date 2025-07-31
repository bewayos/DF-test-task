from scraper import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    sub_url = "https://www.vendr.com/categories/devops/application-development"
    products = scraper.get_product_links(sub_url, "DevOps")
    for p in products:
        print(p)
