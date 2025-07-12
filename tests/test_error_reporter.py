from bot_keydrop.system_safety.error_reporter import ErrorReporter
from bot_keydrop.system_safety.error_reporter import TEST_ENV_VAR

# Updated to trigger auto review tests

import json


def test_capture_exception(tmp_path):
    log = tmp_path / "err.log"
    reporter = ErrorReporter(log_file=log)
    try:
        raise RuntimeError("boom")
    except Exception as exc:
        h = reporter.capture_exception(exc)
    assert log.exists()
    content = log.read_text()
    assert "boom" in content
    assert h in content


def test_capture_exception_no_send_in_tests(monkeypatch, tmp_path):
    """send_callback should not run when under pytest."""
    log = tmp_path / "err.log"
    called = []

    def fake_send(hash_, tb):
        called.append(hash_)

    reporter = ErrorReporter(log_file=log, send_callback=fake_send)
    monkeypatch.setenv(TEST_ENV_VAR, "x")
    try:
        raise ValueError("test")
    except Exception as exc:
        reporter.capture_exception(exc)
    assert not called


def test_pending_file_on_send_fail(tmp_path, monkeypatch):
    log = tmp_path / "err.log"
    pend = tmp_path / "pend.json"
    reporter = ErrorReporter(log_file=log, pending_file=pend)

    monkeypatch.setattr(reporter, "_send_discord", lambda info: False)

    try:
        raise ValueError("fail")
    except Exception as exc:
        reporter.capture_exception(exc)

    assert pend.exists()
    data = json.loads(pend.read_text())
    assert data[0]["message"].endswith("fail")
