"""Utilities for resilient function execution."""
from __future__ import annotations
import logging
import time
from collections import deque
from functools import wraps

logger = logging.getLogger(__name__)


class CircuitOpen(Exception):
    """Raised when circuit breaker is open."""


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.opened_at = 0.0

    def is_open(self) -> bool:
        return self.failures >= self.failure_threshold and (time.time() - self.opened_at) < self.recovery_timeout

    def call(self, func, *args, **kwargs):
        if self.is_open():
            raise CircuitOpen('Circuit breaker open')
        try:
            result = func(*args, **kwargs)
            self.failures = 0
            return result
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.opened_at = time.time()
            raise

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        return wrapper


class LoopDetector:
    """Detect excessive loop iterations."""

    def __init__(self, max_iterations: int = 1_000_000):
        self.max_iterations = max_iterations
        self.count = 0

    def check(self) -> None:
        self.count += 1
        if self.count > self.max_iterations:
            raise RuntimeError('Possible infinite loop detected')


def average_time_monitor(threshold: float, window: int = 5):
    """Decorator to warn if average execution time exceeds threshold."""
    durations: deque[float] = deque(maxlen=window)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            durations.append(time.perf_counter() - start)
            avg = sum(durations) / len(durations)
            if avg > threshold:
                logger.warning('Average execution time %.3fs exceeded threshold %.3fs for %s', avg, threshold, func.__name__)
            return result
        return wrapper

    return decorator


def retry_with_backoff(max_attempts: int = 3, base_delay: float = 0.1, exceptions: tuple[type[Exception], ...] = (Exception,)):
    """Retry function on failure with exponential backoff."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
                    delay *= 2
        return wrapper

    return decorator
