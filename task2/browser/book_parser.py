from data_models.book import Book
from playwright.async_api import Page

class BookParser:
    def __init__(self, page: Page):
        self.page = page

    async def parse(self) -> Book:
        title = await self.page.locator("h1").text_content()

        price_locator = self.page.locator(".product_main .price_color")  
        price = await price_locator.first.text_content()


        rating_locator = self.page.locator(".product_main .star-rating")
        rating_class = await rating_locator.get_attribute("class")
        rating = rating_class.replace("star-rating", "").strip()


        availability_locator = self.page.locator(".product_main .instock.availability")
        availability = (await availability_locator.text_content()).strip()

        image_rel_url = await self.page.locator(".item.active img").get_attribute("src")
        image_url = image_rel_url.replace("../../", "https://books.toscrape.com/")

        description = await self.page.locator("#product_description ~ p").text_content()
        description = description.strip()

        category = await self.page.locator(".breadcrumb li:nth-last-child(2) a").text_content()

        rows = self.page.locator("table.table.table-striped tr")
        product_info = {}
        for i in range(await rows.count()):
            key = await rows.nth(i).locator("th").text_content()
            value = await rows.nth(i).locator("td").text_content()
            product_info[key] = value

        return Book(
            title=title,
            price=price,
            rating=rating,
            availability=availability,
            image_url=image_url,
            description=description,
            category=category,
            upc=product_info.get("UPC", ""),
            product_type=product_info.get("Product Type", ""),
            price_excl_tax=product_info.get("Price (excl. tax)", ""),
            price_incl_tax=product_info.get("Price (incl. tax)", ""),
            tax=product_info.get("Tax", ""),
            num_reviews=product_info.get("Number of reviews", "")
        )
