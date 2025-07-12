import psutil
import time
from pathlib import Path


def watch(interval: int = 5) -> None:
    """Write simple live metrics to logs/live_monitor.html"""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    html_path = log_dir / 'live_monitor.html'
    start = time.time()
    while True:
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        uptime = int(time.time() - start)
        html = f"<html><body><h1>Live Monitor</h1><p>Uptime: {uptime}s</p>" \
               f"<p>CPU: {cpu}%</p><p>RAM: {mem}%</p></body></html>"
        html_path.write_text(html)
        time.sleep(interval)


if __name__ == '__main__':
    watch()
