import asyncio
from multiprocessing import Process, Queue
from typing import Any

from playwright.async_api import async_playwright
from browser.book_parser import BookParser
from browser.category_parser import CategoryParser
from data_models.book import Book

class ScraperProcess(Process):
    """
    ScraperProcess is a separate process for processing one or more categories
    It initializes its own Playwright browser, takes tasks from task_queue, and puts the result into results_queue.
    """

    def __init__(self, task_queue: Queue, results_queue: Queue):
        super().__init__()
        self.task_queue = task_queue
        self.results_queue = results_queue

    def run(self) -> None:
        asyncio.run(self.scrape_loop())

    async def scrape_loop(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            while not self.task_queue.empty():
                category_url = self.task_queue.get()
                print(f"[{self.name}] Processing: {category_url}")

                try:
                    category_parser = CategoryParser(page)
                    book_links = await category_parser.get_all_book_links(category_url)

                    for link in book_links:
                        if not link.endswith("/index.html"):
                            continue

                        book_page = await context.new_page()
                        try:
                            await book_page.goto(link)
                            parser = BookParser(book_page)
                            book: Book = await parser.parse()
                            self.results_queue.put(book)
                        except Exception as e:
                            print(f"[{self.name}] Error parsing {link}: {e}")
                        finally:
                            await book_page.close()

                except Exception as e:
                    print(f"[{self.name}] Failed to process category {category_url}: {e}")

            await page.close()
            await context.close()
            await browser.close()
