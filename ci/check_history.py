import subprocess
import sys
from pathlib import Path

HISTORY_FILE = Path("context/history_of_decisions.md")


def get_changed_files() -> list[str]:
    """Return list of files changed in the last commit."""
    try:
        output = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD~1"], text=True
        )
    except subprocess.CalledProcessError:
        return []
    return [line.strip() for line in output.splitlines() if line.strip()]


def main() -> int:
    changed = get_changed_files()
    if not changed:
        print("No changes detected.")
        return 0

    # fmt: off
    code_changes = [
        f
        for f in changed
        if not f.startswith("docs/") and f != str(HISTORY_FILE)
    ]
    # fmt: on

    if code_changes and str(HISTORY_FILE) not in changed:
        msg = (
            "Error: context/history_of_decisions.md must be updated "
            "with decision rationale."
        )
        print(msg)
        print("Changed files:", ", ".join(code_changes))
        return 1

    print("History of decisions check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
