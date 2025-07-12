#!/usr/bin/env python3
"""Automated rebase and test runner for AI-generated branches."""
from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent / "rebase_log.txt"


def log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(f"[{timestamp}] {message}\n")


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    """Run a command and log it."""
    log(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, text=True, capture_output=True)


def current_branch() -> str:
    result = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        text=True,
    )
    return result.strip()


def is_ai_branch(branch: str) -> bool:
    return re.match(r"^(codex|auto|gpt|bot)/", branch) is not None


def detect_main_branch() -> str:
    for name in ("main", "develop", "clean-main"):
        if subprocess.run(
            ["git", "rev-parse", "--verify", f"origin/{name}"],
            capture_output=True,
        ).returncode == 0:
            return name
    return "main"


def run_tests() -> bool:
    """Run test suite and log the result."""
    log("Running tests...")
    res = subprocess.run(["pytest", "-q"], text=True)
    log(f"Tests exited with code {res.returncode}")
    return res.returncode == 0


def main() -> int:
    start = datetime.now()
    LOG_FILE.write_text("")
    branch = current_branch()
    log(f"Current branch: {branch}")
    if not is_ai_branch(branch):
        log("Branch not marked as AI-generated. Skipping rebase.")
        return 0

    base = detect_main_branch()
    log(f"Rebasing onto origin/{base}")

    run(["git", "fetch", "origin"])
    proc = run(["git", "rebase", f"origin/{base}"])
    if proc.returncode != 0:
        log("Rebase reported conflicts. Attempting automatic fix.")
        log(proc.stdout)
        log(proc.stderr)
        run([
            sys.executable,
            str(Path(__file__).parent / "fix_codex_merge.py"),
        ])
        run(["git", "add", "-A"])
        cont = run(["git", "rebase", "--continue"])
        if cont.returncode != 0:
            log("Automatic conflict resolution failed.")
            return 1
        run(["git", "commit", "--no-edit"])

    changed = subprocess.check_output(
        ["git", "diff", "--name-only", f"origin/{base}"],
        text=True,
    ).splitlines()
    for f in changed:
        log(f"Changed: {f}")

    if not run_tests():
        log("Tests failed after rebase.")
        return 1

    elapsed = (datetime.now() - start).total_seconds()
    log(f"Rebase and tests successful. Elapsed {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
