from bot_keydrop.system_safety.error_reporter import ErrorReporter


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
