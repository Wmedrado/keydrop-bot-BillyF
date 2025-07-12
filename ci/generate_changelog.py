#!/usr/bin/env python3
"""Generate PR summary and changelog entry."""
from __future__ import annotations

import datetime
import subprocess
from pathlib import Path


def changed_files(base_ref: str = "origin/clean-main") -> list[str]:
    subprocess.run(["git", "fetch", "origin", base_ref], check=False)
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"], capture_output=True, text=True
    )
    return [f for f in result.stdout.splitlines() if f]


def write_summary(files: list[str]) -> Path:
    out = Path("ci/pr_summary.md")
    lines = ["### Resumo Técnico", "", "Arquivos modificados:"]
    lines.extend(f"- {f}" for f in files)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def update_changelog(files: list[str]) -> Path:
    changelog = Path("CHANGELOG.md")
    version = Path("VERSION").read_text().strip()
    entry_lines = [f"## {version} - {datetime.date.today()}", ""]
    entry_lines.extend(f"- {f}" for f in files)
    entry = "\n".join(entry_lines) + "\n"
    if changelog.exists():
        content = changelog.read_text(encoding="utf-8")
    else:
        content = ""
    changelog.write_text(entry + "\n" + content, encoding="utf-8")
    return changelog


def main() -> int:
    files = changed_files()
    write_summary(files)
    update_changelog(files)
    print("Changelog and summary updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

