class CategoryParser:
    def __init__(self, page):
        self.page = page

    async def get_all_book_links(self, category_url: str) -> list[str]:
        links_set = set()
        next_url = category_url

        while next_url:
            await self.page.goto(next_url)
            book_anchors = self.page.locator("article.product_pod h3 a")
            count = await book_anchors.count()

            for i in range(count):
                relative = await book_anchors.nth(i).get_attribute("href")
                if not relative:
                    continue
                cleaned = relative.replace('../../../', '').replace('../../', '').replace('../', '')
                full_url = f"https://books.toscrape.com/catalogue/{cleaned}"
                links_set.add(full_url)

            next_button = self.page.locator("li.next a")
            if await next_button.count() > 0:
                next_href = await next_button.first.get_attribute("href")
                base = next_url.rsplit("/", 1)[0]
                next_url = f"{base}/{next_href}"
            else:
                next_url = None

        links = list(links_set)
        print(f"[CategoryParser] Found {len(links)} unique book links in {category_url}")
        return links
