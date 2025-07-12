from pathlib import Path

from bot_keydrop.system_safety.stability import (
    auto_retry,
    backup_config,
    detect_memory_leak,
    check_crash_and_mark,
)


def test_auto_retry_succeeds(tmp_path):
    calls = []

    @auto_retry(max_attempts=3, delay=0)
    def flaky():
        calls.append(1)
        if len(calls) < 2:
            raise ValueError("fail")
        return 42

    assert flaky() == 42
    assert len(calls) == 2


def test_backup_config(tmp_path, monkeypatch):
    cfg = tmp_path / "config.json"
    cfg.write_text("{}")
    monkeypatch.chdir(tmp_path)
    backup = backup_config(config_path=cfg)
    assert backup.exists()


def test_detect_memory_leak():
    assert not detect_memory_leak([10, 11])
    assert detect_memory_leak([1, 2, 3, 4])


def test_check_crash_and_mark(tmp_path):
    state = tmp_path / "state.json"
    version = "v1"
    assert not check_crash_and_mark(version, state)
    assert check_crash_and_mark(version, state)
    flag = Path("rollback.flag")
    assert flag.exists()
    flag.unlink()
