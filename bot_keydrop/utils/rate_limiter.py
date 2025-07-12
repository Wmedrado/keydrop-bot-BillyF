from __future__ import annotations

import time
from typing import Dict


class RateLimiter:
    """Simple time-based rate limiter per key (e.g., IP)."""

    def __init__(self, interval: float, limit: int):
        self.interval = interval
        self.limit = limit
        self.calls: Dict[str, list[float]] = {}

    def allow(self, key: str) -> bool:
        now = time.time()
        window = self.calls.setdefault(key, [])
        window[:] = [t for t in window if now - t < self.interval]
        if len(window) >= self.limit:
            return False
        window.append(now)
        return True
