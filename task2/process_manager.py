import time
import logging
from scraper_process import ScraperProcess
from multiprocessing import Queue
from config import SIMULATE_CRASH, STOP_SIGNAL


class ProcessManager:
    """
    ProcessManager controls ScraperProcess instances:
    - starts initial processes
    - monitors their status
    - restarts a process if it dies unexpectedly
    - exits when no tasks remain and all processes are done
    """

    def __init__(self, num_scrapers: int, task_queue: Queue, results_queue: Queue):
        self.num_scrapers = num_scrapers
        self.task_queue = task_queue
        self.results_queue = results_queue
        self.scrapers = []
        

    def start_processes(self):
        logging.info(f"Starting {self.num_scrapers} scraper processes")
        for i in range(self.num_scrapers):
            simulate_crash = SIMULATE_CRASH and (i == 0)
            p = ScraperProcess(self.task_queue, self.results_queue, simulate_crash=simulate_crash)
            p.start()
            self.scrapers.append(p)
            logging.info(f"Started process PID={p.pid}")


    def monitor_processes(self):
        """
        Monitor and restart processes if they stop unexpectedly.
        Uses multiprocessing.Queue to avoid BrokenPipeError when restarting.
        """
        logging.info("Monitoring scraper processes...")

        while True:
            alive_count = 0
            for i, p in enumerate(self.scrapers):
                if p is not None and p.is_alive():
                    alive_count += 1
                elif p is not None and not p.is_alive():
                    if not self.task_queue.empty():
                        logging.warning(f"Process PID={p.pid} died. Restarting...")
                        new_p = ScraperProcess(self.task_queue, self.results_queue)
                        new_p.start()
                        self.scrapers[i] = new_p
                        logging.info(f"Restarted process PID={new_p.pid}")
                    else:
                        self.scrapers[i] = p

            if self.task_queue.empty() and all(not (proc and proc.is_alive()) for proc in self.scrapers):
                logging.info("No tasks remaining. All scraper processes finished.")
                self.results_queue.put(STOP_SIGNAL)
                break

            time.sleep(2)


    def stop_all(self):
        """Terminate all scraper processes."""
        logging.info("Stopping all scraper processes...")
        for p in self.scrapers:
            if p and p.is_alive():
                p.terminate()
                p.join()
        logging.info("All scraper processes stopped.")
