from scraper import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    subs = scraper.get_subcategories("https://www.vendr.com/categories/devops")
    for sub in subs:
        print(sub)
