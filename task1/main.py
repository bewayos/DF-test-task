import logging
import sys
import os

# Add the current directory to Python path to handle imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task1.threads.queue import create_task_queue, create_result_queue
from task1.threads.worker import WorkerThread
from task1.threads.writer import WriterThread
from task1.scraper.http_client import HttpClient
from task1.scraper.scraper import Scraper
from task1.database.database import Database
import time

# Logging config
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# 🔧 Configuration
CATEGORIES = {
    "DevOps": "https://www.vendr.com/categories/devops",
    "IT Infrastructure": "https://www.vendr.com/categories/it-infrastructure",
    "Data Analytics and Management": "https://www.vendr.com/categories/data-analytics-and-management",
}
NUM_WORKERS = 5

def main():
    logging.info("🔄 Starting scraping process...")

    # Initialize components
    client = HttpClient()
    scraper = Scraper(client)
    parser = scraper.product_parser
    db = Database()

    task_queue = create_task_queue()
    result_queue = create_result_queue()

    # 🧵 Start writer
    writer = WriterThread(result_queue, db)
    writer.start()

    # 🧵 Start workers
    workers = []
    for i in range(NUM_WORKERS):
        worker = WorkerThread(task_queue, result_queue, parser)
        worker.start()
        workers.append(worker)

    # 📦 Generate tasks
    for category, url in CATEGORIES.items():
        logging.info(f"🔗 Getting products for category: {category}")
        products_meta = scraper.link_extractor.get_all_product_links(url, category)
        for product_info in products_meta:
            task_queue.put(product_info)
        logging.info(f"[Scraper] Got {len(products_meta)} product links for {category}")

    # ✅ Task generation completed
    logging.info("✅ All product links pushed to queue.")

    # 🛑 Send stop signals to workers
    for _ in range(NUM_WORKERS):
        task_queue.put(None)

    # Wait for all workers to finish
    task_queue.join()
    logging.info("✅ All workers finished.")

    # Wait for workers to actually complete
    for worker in workers:
        worker.join()
    logging.info("✅ All worker threads joined.")

    # 🛑 Stop writer
    result_queue.put(None)
    result_queue.join()
    logging.info("✅ Writer finished.")

    # Wait for writer to actually complete
    writer.join()
    logging.info("✅ Writer thread joined.")

    # Close database connection
    db.close()
    logging.info("🏁 Scraping completed successfully.")


if __name__ == "__main__":
    t0 = time.time()
    main()
    logging.info(f"🕒 Total time: {time.time() - t0:.2f} seconds")
