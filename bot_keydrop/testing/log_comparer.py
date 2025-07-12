from __future__ import annotations

from itertools import zip_longest
from pathlib import Path
from typing import List


def compare_logs(log_a: Path, log_b: Path) -> List[str]:
    """Return list of human readable differences between two log files."""
    a_lines = log_a.read_text(encoding="utf-8").splitlines()
    b_lines = log_b.read_text(encoding="utf-8").splitlines()
    diffs: List[str] = []
    for idx, (a, b) in enumerate(zip_longest(a_lines, b_lines), start=1):
        if a != b:
            diffs.append(f"Line {idx}: {a!r} != {b!r}")
    return diffs
