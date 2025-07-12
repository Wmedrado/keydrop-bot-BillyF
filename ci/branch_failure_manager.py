#!/usr/bin/env python3
"""Track CI failures per branch and mark for revert after 3 failures."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

STATE_FILE = Path(os.environ.get("FAILURE_STATE_FILE", Path(__file__).parent / "branch_failure_state.json"))


def current_branch() -> str:
    result = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True)
    return result.strip()


def update_failure(success: bool, branch: str | None = None) -> int:
    branch = branch or current_branch()
    if STATE_FILE.exists():
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    else:
        data = {}
    count = data.get(branch, 0)
    if success:
        data[branch] = 0
    else:
        count += 1
        data[branch] = count
    STATE_FILE.write_text(json.dumps(data), encoding="utf-8")
    return data[branch]


def check_and_mark(branch: str | None = None) -> bool:
    branch = branch or current_branch()
    if STATE_FILE.exists():
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    else:
        return False
    count = data.get(branch, 0)
    if count >= 3:
        build_dir = Path(__file__).parent / ".." / "build_results"
        build_dir.mkdir(exist_ok=True)
        (build_dir / "branch_reverted.txt").write_text(branch, encoding="utf-8")
        print(f"Branch {branch} marked for revert")
        return True
    return False


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Manage branch failure counts")
    parser.add_argument("--success", action="store_true", help="Record successful build")
    parser.add_argument("--failure", action="store_true", help="Record failed build")
    args = parser.parse_args()

    if args.success == args.failure:
        print("Specify either --success or --failure")
        return 1

    update_failure(success=args.success)
    if args.failure:
        check_and_mark()
    return 0


if __name__ == "__main__":
    sys.exit(main())
