"""Simple Prometheus metrics exporter."""

from prometheus_client import start_http_server, Gauge
import psutil
import time

CPU = Gauge("bot_cpu_percent", "CPU usage percent")
MEM = Gauge("bot_memory_percent", "Memory usage percent")


def run(port: int = 8001) -> None:
    start_http_server(port)
    while True:
        CPU.set(psutil.cpu_percent())
        MEM.set(psutil.virtual_memory().percent)
        time.sleep(5)


if __name__ == "__main__":
    run()
