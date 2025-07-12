import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gerador_exe import builder


def test_required_files():
    assert builder.check_required_files()
