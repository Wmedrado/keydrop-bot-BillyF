import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ci import auto_rollback as ar  # noqa: E402


def test_auto_rollback_increment(tmp_path, monkeypatch):
    build = tmp_path / 'build_results'
    build.mkdir()
    status = build / 'build_status.log'
    counter = build / 'failure_count.txt'
    status.write_text('failed')
    monkeypatch.setattr(ar, 'STATUS_FILE', status)
    monkeypatch.setattr(ar, 'COUNTER_FILE', counter)
    monkeypatch.setattr(ar.subprocess, 'run', lambda *a, **k: None)
    monkeypatch.chdir(tmp_path)
    ar.main()
    assert counter.read_text() == '1'
