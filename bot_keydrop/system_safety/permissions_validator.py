from pathlib import Path


def check_permissions(dirs=None):
    """Ensure given directories are writable. Return list of issues."""
    if dirs is None:
        dirs = ["logs", "data", "profiles"]
    issues = []
    for d in dirs:
        path = Path(d)
        try:
            path.mkdir(parents=True, exist_ok=True)
            test_file = path / "perm_test.tmp"
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("test")
            test_file.unlink()
        except Exception as e:
            issues.append(f"{d}: {e}")
    return issues
