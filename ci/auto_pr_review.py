import os
import subprocess
import sys
from pathlib import Path


def _get_changed_files() -> set[str]:
    """Return the set of files changed in this PR."""
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        try:
            subprocess.run(["git", "fetch", "origin", base_ref], check=False)
            diff = subprocess.check_output(["git", "diff", "--name-only", f"origin/{base_ref}"])
            return set(diff.decode().split())
        except Exception:
            pass
    try:
        base = subprocess.check_output(["git", "rev-parse", "HEAD~1"]).decode().strip()
        diff = subprocess.check_output(["git", "diff", "--name-only", base])
        return set(diff.decode().split())
    except Exception:
        return set()


def _parse_flake_errors(path: Path, changed: set[str]) -> bool:
    if not path.exists():
        return False
    for line in path.read_text().splitlines():
        if ':' in line:
            file_path = line.split(':', 1)[0]
            if file_path in changed:
                return True
    return False


def _parse_black_errors(path: Path, changed: set[str]) -> bool:
    if not path.exists():
        return False
    for line in path.read_text().splitlines():
        if line.startswith('would reformat'):
            file_path = line.split('would reformat', 1)[1].strip()
            if file_path in changed:
                return True
    return False


def has_lint_errors(flake_log: Path, black_log: Path) -> bool:
    changed = _get_changed_files()
    return _parse_flake_errors(flake_log, changed) or _parse_black_errors(black_log, changed)


def tests_passed(coverage_log: Path) -> bool:
    if not coverage_log.exists():
        return True
    text = coverage_log.read_text()
    return 'FAILED' not in text and 'ERROR' not in text


def has_regression(regression_log: Path) -> bool:
    if not regression_log.exists():
        return False
    text = regression_log.read_text()
    return 'Regressao Critica' in text


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    results = repo_root / 'build_results'
    tests_dir = repo_root / 'tests'

    flake_log = results / 'flake8.log'
    black_log = results / 'black.log'
    coverage_log = tests_dir / 'coverage.txt'
    regression_log = results / 'regression_check.log'

    issues = []
    if has_lint_errors(flake_log, black_log):
        issues.append('Lint errors detected')
    if not tests_passed(coverage_log):
        issues.append('Test failures detected')
    if has_regression(regression_log):
        issues.append('Critical regression detected')

    review_file = results / 'auto_review.txt'
    if issues:
        review_file.write_text('Automatic review failed: ' + '; '.join(issues) + '\n', encoding='utf-8')
        print('Automatic review failed:', '; '.join(issues))
        return 1
    review_file.write_text('Automatic review passed: code approved automatically\n', encoding='utf-8')
    print('Automatic review passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
