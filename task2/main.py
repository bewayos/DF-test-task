import multiprocessing
import logging
from multiprocessing import Queue
from storage.writer import WriterProcess
from process_manager import ProcessManager
from config import DEFAULT_CATEGORIES, NUM_PROCESSES


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    task_queue = Queue()
    results_queue = Queue()

    for url in DEFAULT_CATEGORIES:
        task_queue.put(url)

    writer = WriterProcess(results_queue)
    writer.start()

    pm = ProcessManager(NUM_PROCESSES, task_queue, results_queue)
    pm.start_processes()
    pm.monitor_processes()

    writer.join()
    logging.info("Writer process stopped.")

    logging.info("All scraper processes finished. Books are written directly to the database.")


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    main()
