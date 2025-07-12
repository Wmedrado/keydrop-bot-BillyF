import threading
import time
import psutil
import logging


class ProcessWatchdog(threading.Thread):
    """Monitor the current process for CPU and memory usage."""

    def __init__(self, interval=5, cpu_limit=90, mem_limit_mb=1024):
        super().__init__(daemon=True)
        self.interval = interval
        self.cpu_limit = cpu_limit
        self.mem_limit_mb = mem_limit_mb
        self._running = True

    def run(self):
        proc = psutil.Process()
        while self._running:
            try:
                cpu = proc.cpu_percent(interval=None)
                mem = proc.memory_info().rss / (1024 * 1024)
                if cpu > self.cpu_limit or mem > self.mem_limit_mb:
                    logging.warning(
                        "Consumo alto detectado: CPU %.1f%% MEM %.1fMB", cpu, mem
                    )
            except Exception as e:
                logging.error("Watchdog error: %s", e)
            time.sleep(self.interval)

    def stop(self):
        self._running = False
