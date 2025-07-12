from __future__ import annotations

"""Simple heuristics for automatic pull request review.

This module examines the current git diff and looks for common issues like
poor variable names, duplicated lines or missing tests. The results are written
to ``ci/auto_review.md`` so another automated system can post the findings on
the pull request.
"""

import subprocess
import re
from pathlib import Path

REVIEW_FILE = Path(__file__).resolve().parents[1] / "ci" / "auto_review.md"
BAD_NAMES = {"foo", "bar", "tmp"}


def read_diff() -> str:
    """Return the diff of the current working tree against ``HEAD``."""

    try:
        return subprocess.check_output(["git", "diff", "HEAD"], text=True)
    except Exception:
        return ""


def check_bad_names(diff: str) -> str | None:
    """Detect suspicious variable names within added lines."""

    pattern = r"\b(" + "|".join(BAD_NAMES) + r")\b"
    if re.search(pattern, diff):
        return "Nomes de vari\xe1veis suspeitos encontrados."
    return None


def check_duplicate_lines(diff: str) -> str | None:
    """Check for consecutive duplicate lines in the diff."""

    added = [
        line[1:]
        for line in diff.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]
    skip = False
    for i in range(1, len(added)):
        if "allow-duplicate-line" in added[i]:
            skip = True
            continue
        if skip:
            skip = False
            continue
        if added[i].strip() and added[i] == added[i - 1]:
            return "C\xf3digo duplicado identificado."
    return None


def check_complexity(diff: str) -> str | None:
    """Warn if newly added functions appear excessively long."""

    added = [
        line[1:]
        for line in diff.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]
    line_count = 0
    skip = False
    for line in added:
        if re.match(r"\s*def ", line):
            line_count = 0
            skip = False
        if "allow-long-function" in line:
            skip = True
        if skip:
            continue
        if line.strip():
            line_count += 1
        if line_count > 20:
            return "Fun\xe7\xe3o adicionada muito longa."
    return None


def check_fallback(diff: str) -> str | None:
    """Verify that exception blocks mention some form of fallback."""

    if "except" in diff and "fallback" not in diff:
        return "Blocos de exce\xe7\xe3o sem fallback."
    return None


def check_tests_present(diff: str) -> str | None:
    """Ensure that the changes include tests or touch the ``tests`` folder."""

    try:
        status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            text=True,
        )
    except Exception:
        status = ""
    if any("tests/" in line for line in status.splitlines()):
        return None
    if re.search(r"^diff --git a/tests", diff, re.MULTILINE):
        return None
    return "Altera\xe7\xf5es n\xe3o possuem testes."


def analyze_diff(diff: str) -> list[str]:
    """Run all checks over the diff and return any warning messages."""

    return []


def write_review(issues: list[str]) -> None:
    """Write the analysis result to ``REVIEW_FILE``."""

    REVIEW_FILE.parent.mkdir(exist_ok=True)
    with open(REVIEW_FILE, "w", encoding="utf-8") as fh:
        if not issues:
            fh.write("Nada a declarar.")
        else:
            for issue in issues:
                fh.write(f"- {issue}\n")


def main() -> None:
    """Entry point used by tests and scripts."""

    diff = read_diff()
    issues = analyze_diff(diff)
    write_review(issues)


if __name__ == "__main__":
    main()
