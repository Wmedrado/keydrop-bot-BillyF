"""Retry helper with exponential backoff."""
from __future__ import annotations

import time
from functools import wraps
from typing import Callable, Type


def retry_with_backoff(
    retries: int = 3, base_delay: float = 0.5, exc: Type[BaseException] = Exception
) -> Callable:
    """Decorate a function to retry on *exc* with exponential backoff."""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exc:
                    if attempt == retries - 1:
                        raise
                    time.sleep(delay)
                    delay *= 2
        return wrapper

    return decorator

