import ast
import re
import sys
from pathlib import Path


GENERIC_NAMES = {
    'data',
    'info',
    'helper2',
    'result',
    'main2',
    'doStuff',
    'test_test',
}

GENERIC_FILE_NAMES = {
    'data.py',
    'info.py',
    'helper.py',
    'script.py',
    'temp.py',
}


def is_generic(name: str) -> bool:
    lower = name.lower()
    if name in GENERIC_NAMES:
        return True
    if re.fullmatch(r'(data|info|helper|temp|result)\d*', lower):
        return True
    if lower.startswith('do') and 'stuff' in lower:
        return True
    if lower == 'main2':
        return True
    if re.fullmatch(r'test_?test.*', lower):
        return True
    return False


def analyze_file(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'))
    except Exception as exc:  # SyntaxError or others
        issues.append(f"🚫 {path}: erro ao analisar - {exc}")
        return issues

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if is_generic(node.name):
                issues.append(
                    f"🚫 {path}:{node.lineno} -> nome '{node.name}' parece genérico ou pouco descritivo."
                )
            elif len(node.name) < 3:
                issues.append(
                    f"🚫 {path}:{node.lineno} -> nome '{node.name}' muito curto para ser descritivo."
                )
    if path.name in GENERIC_FILE_NAMES or is_generic(path.stem):
        issues.append(
            f"🚫 Nome do arquivo '{path.name}' é genérico e não descreve seu conteúdo."
        )
    return issues


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    python_files = [p for p in repo_root.rglob('*.py') if 'venv' not in p.parts and 'build' not in p.parts]
    all_issues: list[str] = []
    for py in python_files:
        all_issues.extend(analyze_file(py))

    violations = repo_root / 'naming_violations.md'
    if all_issues:
        with open(violations, 'w', encoding='utf-8') as f:
            f.write('# Violações de Nomeação\n\n')
            for iss in all_issues:
                f.write(f'- {iss}\n')
        for iss in all_issues:
            print(iss)
        print('Erros de nomenclatura encontrados. Consulte naming_violations.md.')
        return 1
    else:
        if violations.exists():
            violations.unlink()
        print('Nenhuma violação de nomeação encontrada.')
        return 0


if __name__ == '__main__':
    sys.exit(main())
