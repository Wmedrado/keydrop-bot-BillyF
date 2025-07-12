import logging
import time
import pytest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.resilience_utils import (
    CircuitBreaker,
    CircuitOpen,
    LoopDetector,
    average_time_monitor,
    retry_with_backoff,
)


def test_circuit_breaker():
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)

    def fail():
        raise ValueError('x')

    for _ in range(2):
        with pytest.raises(ValueError):
            cb.call(fail)
    with pytest.raises(CircuitOpen):
        cb.call(fail)


def test_loop_detector():
    ld = LoopDetector(max_iterations=2)
    ld.check()
    ld.check()
    with pytest.raises(RuntimeError):
        ld.check()


def test_average_time_monitor(caplog):
    @average_time_monitor(0.01, window=2)
    def slow():
        time.sleep(0.02)

    with caplog.at_level(logging.WARNING):
        slow()
        slow()
    assert 'exceeded' in caplog.text


def test_retry_with_backoff():
    calls = []

    @retry_with_backoff(max_attempts=3, base_delay=0)
    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise ValueError('fail')
        return 'ok'

    assert flaky() == 'ok'
    assert len(calls) == 3
