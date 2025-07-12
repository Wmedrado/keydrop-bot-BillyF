#!/usr/bin/env python3
"""Generate simple changelog from git log."""
from __future__ import annotations
import subprocess
from pathlib import Path

OUTPUT = Path('build_results/changelog.md')


def generate_changelog() -> str:
    try:
        log = subprocess.check_output(['git', 'log', '--format=%s', '-n', '10'])
        lines = [f'- {line.strip()}' for line in log.decode().splitlines()]
        return '# Changelog\n\n' + '\n'.join(lines)
    except Exception:
        return '# Changelog\n\nNo history available.'


def main() -> int:
    OUTPUT.write_text(generate_changelog(), encoding='utf-8')
    print('Changelog generated')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
