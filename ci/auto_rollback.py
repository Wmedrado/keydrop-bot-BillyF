#!/usr/bin/env python3
"""Trigger rollback if the last two builds failed."""
from __future__ import annotations

import argparse
import sys
from bot_keydrop.utils.cli_sanitizer import sanitize_cli_args
import json
import subprocess
from pathlib import Path

STATE_FILE = Path(__file__).parent / "rollback_state.json"
LAST_SUCCESS = Path(__file__).parent / "last_success_commit.txt"


def record_success() -> None:
    STATE_FILE.write_text(json.dumps({"failures": 0}), encoding="utf-8")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    LAST_SUCCESS.write_text(commit, encoding="utf-8")


def record_failure() -> None:
    if STATE_FILE.exists():
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    else:
        data = {"failures": 0}
    data["failures"] = data.get("failures", 0) + 1
    STATE_FILE.write_text(json.dumps(data), encoding="utf-8")
    if data["failures"] >= 2 and LAST_SUCCESS.exists():
        commit = LAST_SUCCESS.read_text(encoding="utf-8").strip()
        Path("ci/rollback_triggered.txt").write_text(commit, encoding="utf-8")


def main() -> int:
    sanitize_cli_args(sys.argv[1:])
    parser = argparse.ArgumentParser()
    parser.add_argument("--success", action="store_true")
    parser.add_argument("--failure", action="store_true")
    args = parser.parse_args()

    if args.success == args.failure:
        print("Specify --success or --failure")
        return 1

    if args.success:
        record_success()
    else:
        record_failure()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
