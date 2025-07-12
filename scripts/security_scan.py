"""Run Bandit security audit on the project."""
from __future__ import annotations

import subprocess


def main() -> None:
    """Execute Bandit recursively on the code base."""
    subprocess.run(["bandit", "-r", "."], check=False)


if __name__ == "__main__":
    main()

