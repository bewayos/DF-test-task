import logging
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task1.threads.queue import create_task_queue, create_result_queue
from task1.threads.worker import WorkerThread
from task1.threads.writer import WriterThread
from task1.scraper.http_client import HttpClient
from task1.scraper.scraper import Scraper
from task1.database.database import Database

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Configuration
CATEGORIES = {
    "DevOps": "https://www.vendr.com/categories/devops",
    "IT Infrastructure": "https://www.vendr.com/categories/it-infrastructure",
    "Data Analytics and Management": "https://www.vendr.com/categories/data-analytics-and-management",
}
# You can change the number of workers to fit your needs
NUM_WORKERS = 15


def main():
    logging.info(" Starting scraping process...")

    # Init components
    client = HttpClient()
    scraper = Scraper(client)
    parser = scraper.product_parser
    db = Database()

    task_queue = create_task_queue()
    result_queue = create_result_queue()

    for category, url in CATEGORIES.items():
        logging.info(f" Getting products for category: {category}")
        subcats = scraper.link_extractor.get_subcategories(url)

        for subcat in subcats:
            product_links = scraper.link_extractor.get_all_product_links(subcat, category)
            for info in product_links:
                task_queue.put(info)


    logging.info(" All product links pushed to queue.")

    writer = WriterThread(result_queue, db)
    writer.start()

    workers = []
    for i in range(NUM_WORKERS):
        worker = WorkerThread(task_queue, result_queue, parser)
        worker.start()
        workers.append(worker)

    for _ in range(NUM_WORKERS):
        task_queue.put(None)

    task_queue.join()
    logging.info(" All workers finished.")

    for worker in workers:
        worker.join()
    logging.info(" All worker threads joined.")

    result_queue.put(None)
    result_queue.join()
    logging.info(" Writer finished.")

    writer.join()
    logging.info(" Writer thread joined.")

    db.close()
    logging.info(" Scraping completed successfully.")

if __name__ == "__main__":
    t0 = time.time()
    main()
    logging.info(f" Total time: {time.time() - t0:.2f} seconds")
