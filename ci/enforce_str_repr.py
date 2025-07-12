#!/usr/bin/env python3
"""Ensure new public classes define __str__ and __repr__."""
from __future__ import annotations

import ast
import subprocess
from pathlib import Path


def changed_files(base_ref: str = "origin/clean-main") -> list[Path]:
    subprocess.run(["git", "fetch", "origin", base_ref], check=False)
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"], capture_output=True, text=True
    )
    return [Path(p) for p in result.stdout.splitlines() if p.endswith(".py")]


def validate_file(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            methods = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}
            if "__str__" not in methods or "__repr__" not in methods:
                errors.append(f"Class {node.name} missing __str__/__repr__ in {path}")
    return errors


def main() -> int:
    errors: list[str] = []
    for file in changed_files():
        errors.extend(validate_file(file))
    for e in errors:
        print(e)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

