import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ci import check_todo_fixme as ctf  # noqa: E402


def test_scan_file(tmp_path):
    p = tmp_path / 'a.py'
    p.write_text('# TODO: fix')
    assert ctf.scan_file(p)
    p.write_text('x = 1')
    assert not ctf.scan_file(p)
