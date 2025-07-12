"""Simple circuit breaker implementation."""
from __future__ import annotations

import time
from functools import wraps
from typing import Callable


class CircuitBreakerOpen(Exception):
    """Raised when the circuit is open."""


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.open_until = 0.0

    def __call__(self, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if time.time() < self.open_until:
                raise CircuitBreakerOpen()
            try:
                result = func(*args, **kwargs)
            except Exception:
                self.failures += 1
                if self.failures >= self.failure_threshold:
                    self.open_until = time.time() + self.recovery_timeout
                    self.failures = 0
                raise
            else:
                self.failures = 0
                return result

        return wrapper

