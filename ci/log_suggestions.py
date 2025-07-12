#!/usr/bin/env python3
"""Analyze log files and generate improvement suggestions."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

# When executed directly the repository root may not be on the PYTHONPATH.
# Append the parent directory of this file to import the bot packages.
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from bot_keydrop.system_safety.error_analyzer import analyze_error

DEFAULT_LOG = Path("logs/bot_engine.log")
OUTPUT_FILE = Path("ci/log_suggestions.md")


def tail_lines(path: Path, count: int = 50) -> List[str]:
    """Return the last `count` lines from `path` if it exists."""
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    return lines[-count:]


def generate_suggestions(lines: List[str]) -> List[str]:
    """Return unique suggestions based on error lines."""
    suggestions: List[str] = []
    for line in lines:
        if "ERROR" in line or "Exception" in line:
            suggestion = analyze_error(line)
            if suggestion not in suggestions:
                suggestions.append(suggestion)
    return suggestions


def main(log_path: Path = DEFAULT_LOG) -> int:
    lines = tail_lines(log_path)
    suggestions = generate_suggestions(lines)
    if suggestions:
        out_lines = ["# Log Suggestions", ""]
        out_lines.extend(f"- {s}" for s in suggestions)
        OUTPUT_FILE.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        print(f"Suggestions written to {OUTPUT_FILE}")
    else:
        print("No suggestions generated")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "log", nargs="?", default=str(DEFAULT_LOG), help="Log file to analyze"
    )
    args = parser.parse_args()
    raise SystemExit(main(Path(args.log)))
