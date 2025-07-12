from bot_keydrop.system_safety.error_reporter import ErrorReporter, TEST_ENV_VAR


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
