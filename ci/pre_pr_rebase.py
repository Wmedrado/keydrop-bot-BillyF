#!/usr/bin/env python3
"""Automatically rebase AI branches and run tests."""
from __future__ import annotations
import subprocess
import sys
import time
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent / "rebase_log.txt"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True)


def _install_req_file(path: str) -> None:
    """Install packages from a requirements file with basic filtering."""
    for line in Path(path).read_text().splitlines():
        pkg = line.strip()
        if not pkg or pkg.startswith("#"):
            continue
        args = [sys.executable, "-m", "pip", "install", pkg]
        if pkg.startswith("win10toast"):
            args.append("--no-deps")
        run(args)


def install_deps() -> None:
    """Install minimal dependencies needed for running tests."""
    reqs = [
        "bot_keydrop/requirements.txt",
        "bot_keydrop/backend/requirements.txt",
    ]
    for req in reqs:
        _install_req_file(req)
    run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "pytest",
            "pytest-asyncio",
            "pytest-mock",
            "beautifulsoup4",
            "tkhtmlview",
        ]
    )


def current_branch() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
    ).strip()


def is_ai_branch(name: str) -> bool:
    prefixes = ("codex/", "auto/", "gpt/", "bot/")
    return any(name.startswith(p) for p in prefixes)


def detect_base_branch() -> str | None:
    for b in ("main", "develop", "clean-main"):
        try:
            subprocess.run(
                ["git", "rev-parse", "--verify", f"origin/{b}"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return b
        except subprocess.CalledProcessError:
            continue
    return None


def tests_pass() -> bool:
    install_deps()
    proc = subprocess.run(["pytest", "-q"], text=True)
    return proc.returncode == 0


def has_changes() -> bool:
    out = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    return bool(out.stdout.strip())


def main() -> int:
    start = time.time()
    lines: list[str] = []
    branch = current_branch()
    lines.append(f"Branch: {branch}")

    if not is_ai_branch(branch):
        lines.append("Not an AI branch. Skipping rebase.")
        LOG_FILE.write_text("\n".join(lines) + "\n")
        return 0

    base = detect_base_branch()
    if not base:
        lines.append("Base branch not found.")
        LOG_FILE.write_text("\n".join(lines) + "\n")
        return 1

    run(["git", "fetch", "origin", base])
    result = run(["git", "rebase", f"origin/{base}"])
    if result.returncode != 0:
        lines.append("Rebase conflicts detected. Running fixer.")
        fixer = Path(__file__).parent / "fix_codex_merge.py"
        if fixer.exists():
            subprocess.run([sys.executable, str(fixer)])
        run(["git", "add", "-A"])
        run(["git", "rebase", "--continue"])

    changed = subprocess.check_output(
        ["git", "diff", "--name-only", f"origin/{base}"], text=True
    ).splitlines()
    if changed:
        lines.append("Files changed after rebase:")
        lines.extend(changed)

    if has_changes():
        run(["git", "add", "-A"])
        run(["git", "commit", "-m", "chore: auto-resolve rebase"])

    success = tests_pass()
    lines.append(f"Tests {'passed' if success else 'failed'}")
    duration = time.time() - start
    lines.append(f"Duration: {duration:.2f}s")
    LOG_FILE.write_text("\n".join(lines) + "\n")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
