#!/usr/bin/env python3
"""Ensure all classes implement __str__ and __repr__."""
from __future__ import annotations
import ast
import sys
from pathlib import Path

EXCLUDE_DIRS = {'.git', 'build', 'venv', 'tests'}

def class_methods(node: ast.ClassDef) -> set[str]:
    return {n.name for n in node.body if isinstance(n, ast.FunctionDef)}


def analyze_file(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'))
    except Exception:
        return issues
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = class_methods(node)
            missing = [m for m in ('__str__', '__repr__') if m not in methods]
            if missing:
                issues.append(f"{path}:{node.lineno} missing {', '.join(missing)}")
    return issues


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    problems: list[str] = []
    for file in repo_root.rglob('*.py'):
        if any(part in EXCLUDE_DIRS for part in file.parts):
            continue
        problems.extend(analyze_file(file))
    if problems:
        print('Missing __str__/__repr__ methods:')
        for p in problems:
            print(p)
        return 1
    print('All classes define __str__ and __repr__.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
