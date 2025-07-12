import ast
import subprocess
from pathlib import Path


def changed_files(base: str = "origin/clean-main") -> list[Path]:
    subprocess.run(["git", "fetch", "origin", base], check=False)
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return [Path(p) for p in result.stdout.splitlines() if p.endswith(".py")]


def check_file(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    issues: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name.startswith("_"):
                continue
            if not ast.get_docstring(node):
                issues.append(f"{path}:{node.lineno} missing docstring for {node.name}")
    return issues


def main() -> int:
    errors: list[str] = []
    for file in changed_files():
        errors.extend(check_file(file))
    for e in errors:
        print(e)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
