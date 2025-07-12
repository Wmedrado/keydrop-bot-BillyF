import re
import subprocess
from pathlib import Path

VERSION_FILE = Path("VERSION")


def read_version() -> tuple[int, int, int]:
    if VERSION_FILE.exists():
        text = VERSION_FILE.read_text().strip()
        try:
            major, minor, patch = map(int, text.split("."))
            return major, minor, patch
        except Exception:
            pass
    return 0, 0, 0


def write_version(v: tuple[int, int, int]) -> None:
    VERSION_FILE.write_text(f"{v[0]}.{v[1]}.{v[2]}\n")


def get_last_commit_message() -> str:
    msg = subprocess.check_output(["git", "log", "-1", "--pretty=%B"], text=True)
    return msg.strip()


def bump_version(msg: str) -> tuple[int, int, int]:
    major, minor, patch = read_version()
    if "BREAKING" in msg or "!" in msg.split("\n")[0]:
        major += 1
        minor = 0
        patch = 0
    elif msg.startswith("feat"):
        minor += 1
        patch = 0
    elif msg.startswith("fix"):
        patch += 1
    else:
        patch += 1
    return major, minor, patch


def main() -> int:
    msg = get_last_commit_message()
    new_version = bump_version(msg)
    write_version(new_version)
    print("Version updated to", ".".join(map(str, new_version)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
