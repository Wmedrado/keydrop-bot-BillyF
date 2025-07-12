"""Decorator providing timeout with automatic retries."""

from __future__ import annotations
import asyncio
from functools import wraps
from typing import Callable, Awaitable, Type


def smart_timeout(
    seconds: float, retries: int = 3, exc: Type[BaseException] = Exception
) -> Callable:
    """Decorate an async function to retry if it exceeds *seconds* timeout."""

    def decorator(func: Callable[..., Awaitable]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return await asyncio.wait_for(
                        func(*args, **kwargs), timeout=seconds
                    )
                except exc:
                    if attempt == retries - 1:
                        raise

        return wrapper

    return decorator
