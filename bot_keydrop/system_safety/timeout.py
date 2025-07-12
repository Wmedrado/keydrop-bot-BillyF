import concurrent.futures
import functools
from typing import Callable, TypeVar


class TimeoutException(Exception):
    """Raised when a function execution exceeds the allotted time."""


F = TypeVar("F", bound=Callable)


def enforce_timeout(seconds: float) -> Callable[[F], F]:
    """Decorator to enforce a timeout on synchronous functions."""

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as exc:
                future = exc.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except concurrent.futures.TimeoutError as exc_info:
                    raise TimeoutException(
                        f"{func.__name__} exceeded {seconds}s"
                    ) from exc_info

        return wrapper  # type: ignore

    return decorator
