import logging
import os
import psutil
import threading
import time


class ProcessWatchdog(threading.Thread):
    """Monitor the current process for abnormal resource usage."""

    def __init__(self, interval: float = 5.0, cpu_limit: float = 90.0, memory_limit_mb: float = 500.0):
        super().__init__(daemon=True)
        self.interval = interval
        self.cpu_limit = cpu_limit
        self.memory_limit_mb = memory_limit_mb
        self.logger = logging.getLogger("process_watchdog")
        self.running = True

    def run(self) -> None:
        proc = psutil.Process(os.getpid())
        while self.running:
            cpu = proc.cpu_percent(interval=None)
            mem = proc.memory_info().rss / (1024 * 1024)
            if cpu > self.cpu_limit or mem > self.memory_limit_mb:
                self.logger.warning("Uso excessivo - CPU %.1f%% MEM %.1fMB", cpu, mem)
            time.sleep(self.interval)

    def stop(self) -> None:
        self.running = False

