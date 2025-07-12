from bot_keydrop.system_safety.error_reporter import (
    ErrorReporter,
    TEST_ENV_VAR,
    IS_TEST_ENV_VAR,
)

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import json
from datetime import datetime
from zoneinfo import ZoneInfo


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


def test_capture_exception_respects_is_test_env(monkeypatch, tmp_path):
    """Errors should not be sent when IS_TEST_ENV is true."""
    log = tmp_path / "err.log"
    reporter = ErrorReporter(log_file=log)
    called = []

    def fake_send(_info):
        called.append(True)
        return True

    monkeypatch.setenv(IS_TEST_ENV_VAR, "true")
    monkeypatch.setattr(reporter, "_send_discord", fake_send)
    try:
        raise ValueError("boom")
    except Exception as exc:
        reporter.capture_exception(exc)
    assert not called
    monkeypatch.delenv(IS_TEST_ENV_VAR, raising=False)


def test_pending_file_on_send_fail(tmp_path, monkeypatch):
    log = tmp_path / "err.log"
    pend = tmp_path / "pend.json"
    reporter = ErrorReporter(log_file=log, pending_file=pend)

    monkeypatch.delenv(TEST_ENV_VAR, raising=False)
    monkeypatch.setenv(IS_TEST_ENV_VAR, "false")
    monkeypatch.setattr(reporter, "_send_discord", lambda info: False)
    monkeypatch.delenv(TEST_ENV_VAR, raising=False)

    try:
        raise ValueError("fail")
    except Exception as exc:
        reporter.capture_exception(exc)

    assert reporter.counters
    assert pend.exists()
    data = json.loads(pend.read_text())
    assert data[0]["message"].endswith("fail")
    monkeypatch.delenv(IS_TEST_ENV_VAR, raising=False)


def test_timestamp_in_brasilia_timezone(tmp_path):
    log = tmp_path / "err.log"
    reporter = ErrorReporter(log_file=log)
    try:
        raise RuntimeError("boom")
    except Exception as exc:
        info = reporter._build_error_data(exc, "dummy")

    ts = datetime.strptime(info["timestamp"], "%Y-%m-%d %H:%M:%S").replace(
        tzinfo=ZoneInfo("America/Sao_Paulo")
    )
    now_brt = datetime.now(ZoneInfo("America/Sao_Paulo"))
    assert abs((now_brt - ts).total_seconds()) < 5
