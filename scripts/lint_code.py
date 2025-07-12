"""Run Ruff linting on the project."""
from __future__ import annotations

import subprocess


def main() -> None:
    """Execute Ruff in check mode."""
    subprocess.run(["ruff", "check", "."], check=True)


if __name__ == "__main__":
    main()

