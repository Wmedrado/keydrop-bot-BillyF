"""Monitor average execution time of functions."""
from __future__ import annotations

import logging
import time
from functools import wraps
from typing import Callable


def monitor_time(expected: float) -> Callable:
    """Decorate a function and warn if average runtime exceeds *expected* seconds."""

    def decorator(func: Callable):
        stats = {"count": 0, "total": 0.0}
        logger = logging.getLogger(func.__name__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            stats["count"] += 1
            stats["total"] += elapsed
            mean = stats["total"] / stats["count"]
            if mean > expected:
                logger.warning(
                    "Average execution time %.4fs exceeds expected %.4fs", mean, expected
                )
            return result

        return wrapper

    return decorator

