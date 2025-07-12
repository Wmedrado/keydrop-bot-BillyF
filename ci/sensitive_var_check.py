"""Check for plaintext sensitive variables in the code base."""

from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERN = re.compile(r"(password|secret|token|apikey|api_key)", re.IGNORECASE)


def main() -> int:
    for path in Path('.').rglob('*.py'):
        if path.parts[0] in {'.git', 'venv', '__pycache__'}:
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        for idx, line in enumerate(text.splitlines(), 1):
            if PATTERN.search(line) and '=' in line and not line.strip().startswith('#'):
                print(f"Sensitive variable detected: {path}:{idx}")
                return 1
    print("No sensitive variables found.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
