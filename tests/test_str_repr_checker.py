import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ci import check_str_repr as csr  # noqa: E402


def test_analyze_file(tmp_path):
    f = tmp_path / 'a.py'
    f.write_text('class A:\n    pass\n')
    assert csr.analyze_file(f)
    f.write_text('class A:\n    def __str__(self):\n        return "a"\n    def __repr__(self):\n        return "A()"\n')
    assert not csr.analyze_file(f)
