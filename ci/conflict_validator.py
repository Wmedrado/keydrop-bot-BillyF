import subprocess
import sys


def has_conflicts(base: str = "origin/main") -> bool:
    base_commit = subprocess.check_output(
        [
            "git",
            "merge-base",
            "HEAD",
            base,
        ],
        text=True,
    ).strip()
    result = subprocess.run(
        ["git", "merge-tree", base_commit, "HEAD", base],
        capture_output=True,
        text=True,
    )
    return "<<<<<<<" in result.stdout


def main() -> int:
    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
    ).strip()
    if has_conflicts():
        print(f"Potential merge conflicts detected on branch {branch}")
        return 1
    print("No merge conflicts detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
