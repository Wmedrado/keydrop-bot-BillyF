#!/usr/bin/env python3
"""CI helper to enforce justification for changes to critical files."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List

PROTECTED_FILES = [
    "core/contingency_engine.py",
    "bot_engine/participation.py",
    "config/macro_templates.json",
    "monitoring/metrics_collector.py",
]


def run_git_diff(base_ref: str, repo_root: Path) -> List[str]:
    """Return list of files changed between base_ref and HEAD."""
    subprocess.run(
        ["git", "fetch", "origin", base_ref],
        cwd=repo_root,
        check=False,
    )
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    # fmt: off
    return [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]
    # fmt: on


def check_history(changes: List[str], history_file: Path) -> bool:
    """Verify history_file lists all changed files."""
    if not history_file.exists():
        print(f"History file missing: {history_file}")
        return False
    content = history_file.read_text(encoding="utf-8")
    missing = [f for f in changes if f not in content]
    if missing:
        print("Justification missing for: " + ", ".join(missing))
        return False
    return True


def main(base_ref: str = "origin/clean-main") -> int:
    repo_root = Path(__file__).resolve().parents[1]
    history_path = repo_root / "context" / "history_of_decisions.md"
    changed_files = run_git_diff(base_ref, repo_root)
    protected_changes = [f for f in changed_files if f in PROTECTED_FILES]

    if not protected_changes:
        print("No protected files changed.")
        return 0

    print("Protected files changed: " + ", ".join(protected_changes))

    if not check_history(protected_changes, history_path):
        print("Add explanations to", history_path)
        return 1

    print("All protected changes justified.")
    return 0


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/clean-main"
    sys.exit(main(base))
