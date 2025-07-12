import logging
import threading
import queue
from pathlib import Path
import requests


class AsyncRemoteHandler(logging.Handler):
    """Send logs asynchronously to a remote HTTP endpoint with offline fallback."""

    def __init__(self, url: str, fallback_file: Path | str = "logs/offline.log"):
        super().__init__()
        self.url = url
        self.fallback_file = Path(fallback_file)
        self.queue: "queue.Queue[str]" = queue.Queue()
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()
        self.session = requests.Session()

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.queue.put(msg)

    def _worker(self) -> None:
        while True:
            msg = self.queue.get()
            try:
                resp = self.session.post(self.url, json={"log": msg}, timeout=5)
                if resp.status_code not in (200, 204):
                    raise RuntimeError(f"bad status {resp.status_code}")
            except Exception:
                self._write_offline(msg)
            finally:
                self.queue.task_done()

    def _write_offline(self, msg: str) -> None:
        self.fallback_file.parent.mkdir(exist_ok=True)
        with self.fallback_file.open("a", encoding="utf-8") as fh:
            fh.write(msg + "\n")

    def flush_offline(self) -> None:
        if not self.fallback_file.exists():
            return
        for line in list(self.fallback_file.read_text(encoding="utf-8").splitlines()):
            try:
                resp = self.session.post(self.url, json={"log": line}, timeout=5)
                if resp.status_code not in (200, 204):
                    raise RuntimeError
            except Exception:
                return
        self.fallback_file.unlink()
