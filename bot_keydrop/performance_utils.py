import asyncio
import time
from functools import wraps

from log_utils import setup_logger

perf_logger = setup_logger("performance")


def measure_time(label: str):
    """Decorator to log execution time for sync and async functions."""

    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    return await func(*args, **kwargs)
                finally:
                    duration = time.perf_counter() - start
                    perf_logger.info("%s took %.3fs", label, duration)
            return wrapper
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                try:
                    return func(*args, **kwargs)
                finally:
                    duration = time.perf_counter() - start
                    perf_logger.info("%s took %.3fs", label, duration)
            return wrapper

    return decorator
