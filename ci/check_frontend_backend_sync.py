import re
import sys
from pathlib import Path

FRONTEND_JS = Path('bot_keydrop/frontend/src/js/api.js')
BACKEND_PY = Path('bot_keydrop/backend/main.py')


def get_frontend_endpoints() -> set[str]:
    text = FRONTEND_JS.read_text(encoding='utf-8') if FRONTEND_JS.exists() else ''
    return set(re.findall(r"request\(['\"](/[^'\"]+)", text))


def get_backend_endpoints() -> set[str]:
    text = BACKEND_PY.read_text(encoding='utf-8') if BACKEND_PY.exists() else ''
    return set(re.findall(r"@app\.(?:get|post|put|delete|patch)\(['\"](/[^'\"]*)", text))


def main() -> int:
    front = get_frontend_endpoints()
    back = get_backend_endpoints()
    missing_back = sorted(front - back)
    if missing_back:
        print('Frontend/Backend mismatch detected')
        print('Endpoints used in frontend but missing in backend:', ', '.join(missing_back))
        return 1
    print('Frontend and backend endpoints are synchronized')
    return 0


if __name__ == '__main__':
    sys.exit(main())
