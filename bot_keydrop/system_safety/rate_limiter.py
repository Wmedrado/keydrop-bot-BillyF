"""Rate limiter utilities.

This module exposes :class:`RateLimiter`, a simple sliding-window limiter used
across the project. It keeps track of calls per arbitrary key (such as a user
or task name) and rejects new ones when the limit is exceeded.
"""

from __future__ import annotations

from collections import deque
from time import time
from typing import Deque, Dict


class RateLimiter:
    """Limit the number of actions per key within a period.

    Parameters
    ----------
    max_calls:
        Maximum number of allowed calls during ``period`` seconds.
    period:
        Size of the sliding time window in seconds.

    Examples
    --------
    >>> rl = RateLimiter(2, 5)
    >>> if rl.allow("user"):
    ...     print("allowed")
    """

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
