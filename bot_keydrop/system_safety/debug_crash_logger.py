"""Crash logger for debug mode."""

from __future__ import annotations

import sys
import threading
import time
from pathlib import Path
import traceback
import psutil

_start = time.perf_counter()


def install(log_file: Path = Path("logs/last_crash_debug.log")) -> None:
    """Install a global exception hook writing detailed crash info."""
    log_file.parent.mkdir(exist_ok=True)
    prev = sys.excepthook

    def handler(exc_type, exc, tb):
        elapsed = time.perf_counter() - _start
        mem = psutil.Process().memory_info().rss / (1024 * 1024)
        thread = threading.current_thread().name
        text = "".join(traceback.format_exception(exc_type, exc, tb))
        with log_file.open("w", encoding="utf-8") as fh:
            fh.write(
                f"Thread: {thread}\nMemoryMB: {mem:.1f}\nElapsed: {elapsed:.2f}s\n{text}"
            )
        if prev:
            prev(exc_type, exc, tb)

    sys.excepthook = handler
