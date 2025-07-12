"""Utility to detect potential live loops."""
from __future__ import annotations

import time


class LiveLoopError(RuntimeError):
    """Raised when a loop appears to run indefinitely."""


class LoopDetector:
    def __init__(self, max_iterations: int = 1_000_000, time_window: float = 1.0):
        self.max_iterations = max_iterations
        self.time_window = time_window
        self.count = 0
        self.start = time.perf_counter()

    def tick(self) -> None:
        self.count += 1
        now = time.perf_counter()
        if self.count >= self.max_iterations and (now - self.start) < self.time_window:
            raise LiveLoopError("Possible live loop detected")
        if (now - self.start) >= self.time_window:
            self.count = 0
            self.start = now

