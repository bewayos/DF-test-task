import multiprocessing
import time
from multiprocessing import Manager
from scraper_process import ScraperProcess
from data_models.book import Book
from storage.writer import WriterProcess
from config import DEFAULT_CATEGORIES, NUM_PROCESSES, HEADLESS, TIMEOUT

def main():
    manager = Manager()
    task_queue = manager.Queue()
    results_queue = manager.Queue()

    category_urls = DEFAULT_CATEGORIES
    num_processes = NUM_PROCESSES

    for url in category_urls:
        task_queue.put(url)

    processes = []

    for _ in range(num_processes):
        p = ScraperProcess(task_queue, results_queue)
        p.start()
        processes.append(p)

    writer = WriterProcess(results_queue)
    writer.start()

    for p in processes:
        p.join()

    time.sleep(3)

    writer.terminate()
    writer.join()

    print("All scraper processes finished. Books are written directly to the database.")



if __name__ == "__main__":
    multiprocessing.set_start_method("spawn") 
    main()
