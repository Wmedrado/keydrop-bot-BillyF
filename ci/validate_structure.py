from pathlib import Path
import sys

ALLOWED_ROOT_PY = {
    'launcher.py',
    'input_utils.py',
    'log_utils.py',
}

REQUIRED_DIRS = {'bot_keydrop', 'tests', 'ci'}


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing = [d for d in REQUIRED_DIRS if not (root / d).exists()]
    if missing:
        print(f"Missing required directories: {', '.join(missing)}")
        return 1
    bad_py = [p.name for p in root.glob('*.py') if p.name not in ALLOWED_ROOT_PY]
    if bad_py:
        print(f"Unexpected python files at project root: {', '.join(bad_py)}")
        return 1
    print("Structure validated")
    return 0


if __name__ == '__main__':
    sys.exit(main())
