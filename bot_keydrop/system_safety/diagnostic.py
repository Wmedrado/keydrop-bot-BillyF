import asyncio
import functools
import logging
import time
import traceback

from .error_reporter import error_reporter


def diagnostic(func):
    """Decorator to log entry/exit and capture exceptions with timing."""
    logger = logging.getLogger(func.__module__)
    qualname = func.__qualname__
    line = func.__code__.co_firstlineno

    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger.debug("Entering %s (line %d)", qualname, line)
            start = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as exc:  # pragma: no cover - re-raise after logging
                tb = traceback.format_exc()
                logger.error("Exception in %s (line %d): %s", qualname, line, tb)
                try:
                    error_reporter.capture_exception(exc)
                except Exception:
                    logger.exception("Failed to report error")
                raise
            finally:
                elapsed = (time.perf_counter() - start) * 1000
                logger.debug("Exiting %s (line %d) after %.2fms", qualname, line, elapsed)
        return wrapper
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug("Entering %s (line %d)", qualname, line)
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as exc:  # pragma: no cover - re-raise after logging
                tb = traceback.format_exc()
                logger.error("Exception in %s (line %d): %s", qualname, line, tb)
                try:
                    error_reporter.capture_exception(exc)
                except Exception:
                    logger.exception("Failed to report error")
                raise
            finally:
                elapsed = (time.perf_counter() - start) * 1000
                logger.debug("Exiting %s (line %d) after %.2fms", qualname, line, elapsed)
        return wrapper

