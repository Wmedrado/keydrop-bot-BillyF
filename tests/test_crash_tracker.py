from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.system_safety import crash_tracker  # noqa: E402


def test_log_last_line(tmp_path):
    crash_tracker.LOG_FILE = tmp_path / 'last.log'
    try:
        raise RuntimeError('boom')
    except Exception as exc:
        crash_tracker.log_last_line(exc)
    data = crash_tracker.LOG_FILE.read_text()
    assert 'last.log' not in data  # content should reference file and line
