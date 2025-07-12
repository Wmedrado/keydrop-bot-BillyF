#!/usr/bin/env python3
"""Rollback to previous commit if build fails twice."""
from __future__ import annotations
import subprocess
from pathlib import Path

STATUS_FILE = Path('build_results/build_status.log')
COUNTER_FILE = Path('build_results/failure_count.txt')


def main() -> int:
    status = STATUS_FILE.read_text().strip() if STATUS_FILE.exists() else ''
    count = int(COUNTER_FILE.read_text().strip()) if COUNTER_FILE.exists() else 0
    if status == 'Build succeeded':
        COUNTER_FILE.write_text('0')
        return 0
    count += 1
    COUNTER_FILE.write_text(str(count))
    if count >= 2:
        print('Rolling back to previous commit')
        subprocess.run(['git', 'reset', '--hard', 'HEAD~1'], check=False)
    return 1

if __name__ == '__main__':
    raise SystemExit(main())
