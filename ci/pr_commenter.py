#!/usr/bin/env python3
"""Generate PR comment summarizing changed files."""
from __future__ import annotations
import subprocess
from pathlib import Path

OUTPUT = Path('build_results/pr_comment.md')


def get_changed_files() -> list[str]:
    try:
        diff = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD~1'])
        return [line.strip() for line in diff.decode().splitlines() if line.strip()]
    except Exception:
        return []


def main() -> int:
    files = get_changed_files()
    if not files:
        OUTPUT.write_text('No changes detected.\n', encoding='utf-8')
        return 0
    msg = '# Arquivos modificados\n\n'
    for f in files:
        msg += f'- {f}\n'
    OUTPUT.write_text(msg, encoding='utf-8')
    print('PR comment generated')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
