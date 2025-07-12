"""Time-based caching utilities."""

from __future__ import annotations

import time
from functools import wraps
from typing import Any, Callable, Dict, Tuple


def cache_result(ttl: float = 60.0) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Cache function results for *ttl* seconds."""

    storage: Dict[Tuple[Any, ...], Tuple[float, Any]] = {}

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = args + tuple(sorted(kwargs.items()))
            now = time.time()
            if key in storage:
                ts, val = storage[key]
                if now - ts < ttl:
                    return val
            result = func(*args, **kwargs)
            storage[key] = (now, result)
            return result

        return wrapper

    return decorator
