import threading
import logging
from queue import Queue, Empty
from task1.scraper.models import Product
from task1.database.database import Database

class WriterThread(threading.Thread):
    def __init__(self, result_queue: Queue, db: Database):
        super().__init__()
        self.result_queue = result_queue
        self.db = db
        self.daemon = True

    def run(self):
        while True:
            try:
                product = self.result_queue.get(timeout=10)
            except Empty:
                logging.debug(f"[Writer {self.name}] Queue timeout, exiting")
                break

            if product is None:
                self.result_queue.task_done()
                logging.debug(f"[Writer {self.name}] Received stop signal")
                break
            
            logging.info(f"[Writer {self.name}] Inserting product: {product.name}")

            try:
                self.db.insert_product(product)
            except Exception as e:
                logging.error(f"[Writer {self.name}] Failed to insert product {product.name}: {e}")
            finally:
                self.result_queue.task_done()
