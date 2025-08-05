import asyncio
import sys
import queue
from multiprocessing import Process, Queue
from playwright.async_api import async_playwright
from browser.book_parser import BookParser
from browser.category_parser import CategoryParser
from data_models.book import Book


class ScraperProcess(Process):
    """
    ScraperProcess is a separate process for processing one or more categories.
    It initializes its own Playwright browser, takes tasks from task_queue,
    and puts the result into results_queue.
    """

    crashed_once = False  # class-level flag to ensure crash happens only once

    def __init__(self, task_queue: Queue, results_queue: Queue, simulate_crash: bool = False):
        super().__init__()
        self.task_queue = task_queue
        self.results_queue = results_queue
        self.simulate_crash = simulate_crash

    def run(self) -> None:
        asyncio.run(self.scrape_loop())

    async def scrape_loop(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            while True:
                try:
                    category_url = self.task_queue.get(timeout=1)
                except queue.Empty:
                    break 

                print(f"[{self.name}] Processing: {category_url}")

                try:
                    category_parser = CategoryParser(page)
                    book_links = await category_parser.get_all_book_links(category_url)

                    for idx, link in enumerate(book_links):
                        if not link.endswith("/index.html"):
                            continue

                        book_page = await context.new_page()
                        try:
                            await book_page.goto(link)
                            parser = BookParser(book_page)
                            book: Book = await parser.parse()
                            self.results_queue.put(book)
                            print(f"[{self.name}] Pushed to results_queue: {book.title}")

                            if (
                                self.simulate_crash
                                and idx == 0
                                and not ScraperProcess.crashed_once
                            ):
                                ScraperProcess.crashed_once = True
                                print(f"[{self.name}] Simulating controlled crash now...")
                                sys.exit(1)

                        except Exception as e:
                            print(f"[{self.name}] Error parsing {link}: {e}")
                        finally:
                            await book_page.close()

                except Exception as e:
                    print(f"[{self.name}] Failed to process category {category_url}: {e}")

            await page.close()
            await context.close()
            await browser.close()
