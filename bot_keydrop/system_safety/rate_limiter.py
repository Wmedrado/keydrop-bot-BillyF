"""Rate limiter utilities."""

from __future__ import annotations

from collections import deque
from time import time
from typing import Deque, Dict


class RateLimiter:
    """Limit the number of actions per period for multiple keys."""

    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls: Dict[str, Deque[float]] = {}

    def allow(self, key: str) -> bool:
        q = self.calls.setdefault(key, deque())
        now = time()
        while q and now - q[0] > self.period:
            q.popleft()
        if len(q) >= self.max_calls:
            return False
        q.append(now)
        return True
