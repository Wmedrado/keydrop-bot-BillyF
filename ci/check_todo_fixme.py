#!/usr/bin/env python3
"""Fail if TODO or FIXME comments exist."""
from __future__ import annotations
import re
import sys
from pathlib import Path

EXCLUDE_DIRS = {'.git', 'build', 'venv'}
PATTERN = re.compile(r'\b(?:TODO|FIXME):')

def scan_file(path: Path) -> list[str]:
    matches: list[str] = []
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return matches
    for i, line in enumerate(text.splitlines(), 1):
        if PATTERN.search(line):
            matches.append(f"{path}:{i}:{line.strip()}")
    return matches


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    issues: list[str] = []
    for file in repo_root.rglob('*.py'):
        if any(part in EXCLUDE_DIRS for part in file.parts):
            continue
        issues.extend(scan_file(file))
    if issues:
        print('TODO/FIXME comments found:')
        for m in issues:
            print(m)
        return 1
    print('No TODO/FIXME comments found.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
