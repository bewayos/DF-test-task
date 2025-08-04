import threading
import logging
from queue import Queue, Empty
from task1.scraper.product_parser import ProductParser

class WorkerThread(threading.Thread):
    def __init__(self, task_queue: Queue, result_queue: Queue, parser: ProductParser):
        super().__init__(daemon=True)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.parser = parser

    def run(self):
        while True:
            try:
                task = self.task_queue.get(timeout=5)
            except Empty:
                logging.debug(f"[Worker {self.name}] Timeout — exiting")
                break

            if task is None:
                self.task_queue.task_done()
                logging.debug(f"[Worker {self.name}] Received stop signal")
                break

            try:
                product = self.parser.parse_product_page(task["url"], task["category"], task)
                if product:
                    self.result_queue.put(product)
                    logging.info(f"[Worker {self.name}] Parsed: {product.name}")
            except Exception as e:
                logging.error(f"[Worker {self.name}] Error on {task.get('url')}: {e}")
            finally:
                self.task_queue.task_done()
