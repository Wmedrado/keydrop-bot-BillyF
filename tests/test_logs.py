import importlib

log_utils = importlib.import_module("log_utils")


def test_log_file_creation(tmp_path):
    logger = log_utils.setup_logger("test_logger", logs_dir=tmp_path)
    logger.info("hello")
    log_file = tmp_path / "test_logger.log"
    assert log_file.exists()
    try:
        content = log_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = log_file.read_text(encoding="latin-1")
    assert "hello" in content
