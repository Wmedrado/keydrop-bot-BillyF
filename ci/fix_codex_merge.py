#!/usr/bin/env python3
"""Remove typical Codex merge conflict markers."""
from __future__ import annotations
from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parents[1]

def list_conflicted_files() -> list[Path]:
    result = subprocess.run([
        "git",
        "diff",
        "--name-only",
        "--diff-filter=U",
    ], capture_output=True, text=True, cwd=REPO_ROOT)
    return [REPO_ROOT / f for f in result.stdout.splitlines() if f.strip()]

def clean_file(path: Path) -> None:
    content = path.read_text(encoding="utf-8").splitlines()
    cleaned: list[str] = []
    skip = False
    for line in content:
        if line.startswith("<<<<<<<"):
            skip = True
            continue
        if line.startswith("=======") and skip:
            continue
        if line.startswith(">>>>>>>"):
            skip = False
            continue
        if not skip:
            cleaned.append(line)
    path.write_text("\n".join(cleaned) + "\n", encoding="utf-8")
    subprocess.run(["git", "add", str(path)], check=False, cwd=REPO_ROOT)

def main() -> int:
    files = list_conflicted_files()
    if not files:
        print("No conflicted files to fix")
        return 0
    for f in files:
        clean_file(f)
        print(f"Fixed conflicts in {f.relative_to(REPO_ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
