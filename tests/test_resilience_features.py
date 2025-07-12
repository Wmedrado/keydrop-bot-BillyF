from pathlib import Path
import sys
import time
import pytest

PYTHONPATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PYTHONPATH))

from ci.todo_finder import check_todos  # noqa: E402
from ci.enforce_str_repr import validate_file  # noqa: E402
from bot_keydrop.system_safety.crash_tracker import (
    start_crash_tracker,
    log_exception,
    LAST_LINE,
)  # noqa: E402
from bot_keydrop.utils.circuit_breaker import CircuitBreaker, CircuitBreakerOpen  # noqa: E402
from bot_keydrop.utils.loop_detector import LoopDetector, LiveLoopError  # noqa: E402
from bot_keydrop.utils.time_monitor import monitor_time  # noqa: E402
from bot_keydrop.utils.retry import retry_with_backoff  # noqa: E402


def test_todo_finder(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("# TODO: fix\nprint('x')")
    found = check_todos(tmp_path)
    assert f in found


def test_enforce_str_repr(tmp_path):
    code = """class Sample:\n    pass\n"""
    file = tmp_path / "m.py"
    file.write_text(code)
    errors = validate_file(file)
    assert errors


def test_crash_tracker(tmp_path):
    log = tmp_path / "log.txt"
    start_crash_tracker(log)

    def boom():
        raise ValueError("fail")

    try:
        boom()
    except Exception as exc:
        log_exception(exc)

    text = log.read_text()
    assert "boom" in text


def test_circuit_breaker():
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)

    calls = {"n": 0}

    @breaker
    def flaky():
        calls["n"] += 1
        raise RuntimeError

    for _ in range(2):
        try:
            flaky()
        except RuntimeError:
            pass

    with pytest.raises(CircuitBreakerOpen):
        flaky()


def test_loop_detector():
    det = LoopDetector(max_iterations=5, time_window=0.5)
    with pytest.raises(LiveLoopError):
        for _ in range(6):
            det.tick()


def test_time_monitor(caplog):
    @monitor_time(0.0)
    def work():
        time.sleep(0.01)

    with caplog.at_level("WARNING"):
        work()
        work()
    assert any("exceeds" in r.message for r in caplog.records)


def test_retry_with_backoff(monkeypatch):
    attempts = {"n": 0}

    @retry_with_backoff(retries=3, base_delay=0)
    def func():
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise ValueError
        return 5

    assert func() == 5
    assert attempts["n"] == 3
