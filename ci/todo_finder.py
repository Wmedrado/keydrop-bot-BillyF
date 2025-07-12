#!/usr/bin/env python3
"""Fail if TODO or FIXME comments exist in the repository."""
from __future__ import annotations

import re
from pathlib import Path

PATTERN = re.compile(r"\b(TODO|FIXME):")


def check_todos(repo: Path) -> list[Path]:
    results: list[Path] = []
    for path in repo.rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if PATTERN.search(text):
            results.append(path)
    return results


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    found = check_todos(repo)
    if found:
        for f in found:
            print(f"TODO/FIXME found in {f}")
        return 1
    print("No TODO/FIXME found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

