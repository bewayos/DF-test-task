import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from browser.book_parser import BookParser
from browser.category_parser import CategoryParser

import asyncio
from playwright.async_api import async_playwright

CATEGORY_URL = "https://books.toscrape.com/catalogue/category/books/poetry_23/index.html"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()
        category_parser = CategoryParser(page)
        book_links = await category_parser.get_all_book_links(CATEGORY_URL)
        await page.close()

        print(f"Found books: {len(book_links)}")

        for link in book_links:
            if not link.endswith("/index.html"):
                print(f"[SKIP] Not a book page: {link}")
                continue

            book_page = await context.new_page()
            try:
                await book_page.goto(link)
                parser = BookParser(book_page)
                book = await parser.parse()
                print(book)
            except Exception as e:
                print(f"[ERROR] Failed to parse {link}: {e}")
            finally:
                await book_page.close()

        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
