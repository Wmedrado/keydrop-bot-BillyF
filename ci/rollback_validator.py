#!/usr/bin/env python3
"""Check for critical file changes and generate rollback instructions."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List

CRITICAL_PATTERNS = ["login", "transaction", "sorteio", "lottery"]


def run_git_diff(base_ref: str, repo_root: Path) -> List[str]:
    subprocess.run(["git", "fetch", "origin", base_ref], cwd=repo_root, check=False)
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def should_trigger_rollback(files: List[str]) -> bool:
    return any(any(p in f for p in CRITICAL_PATTERNS) for f in files)


def main(base_ref: str = "origin/clean-main") -> int:
    repo_root = Path(__file__).resolve().parents[1]
    build_dir = repo_root / "build_results"
    build_dir.mkdir(exist_ok=True)
    files = run_git_diff(base_ref, repo_root)
    if should_trigger_rollback(files):
        (build_dir / "rollback_required.txt").write_text(
            "Critical changes detected. Prepare rollback.",
            encoding="utf-8",
        )
        print("Rollback file created")
    else:
        print("No critical changes detected")
    return 0


if __name__ == "__main__":
    ref = sys.argv[1] if len(sys.argv) > 1 else "origin/clean-main"
    sys.exit(main(ref))
