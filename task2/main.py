import multiprocessing
import time
from multiprocessing import Manager
from scraper_process import ScraperProcess
from data_models.book import Book


def main():
    manager = Manager()
    task_queue = manager.Queue()
    results_queue = manager.Queue()

    category_urls = [
        "https://books.toscrape.com/catalogue/category/books/poetry_23/index.html",
        "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
    ]

    for url in category_urls:
        task_queue.put(url)

    num_processes = 2
    processes = []

    for _ in range(num_processes):
        p = ScraperProcess(task_queue, results_queue)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("\nAll scraper processes finished. Results:\n")

    results = []
    while not results_queue.empty():
        book: Book = results_queue.get()
        results.append(book)

    print(f"Total books collected: {len(results)}\n")
    for b in results:
        print(f"{b.title} | {b.category} | {b.price}")


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn") 
    main()
