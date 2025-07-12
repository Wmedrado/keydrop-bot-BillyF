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


def _check_depth(node: ast.AST, depth: int, path: Path, issues: list[str]) -> None:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and depth > 2:
        issues.append(f"{path}:{node.lineno} nesting deeper than 2 levels")
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            _check_depth(child, depth + 1, path, issues)
        else:
            _check_depth(child, depth, path, issues)


def check_file(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    issues: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            _check_depth(node, 0, path, issues)
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
