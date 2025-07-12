import subprocess
from pathlib import Path
import ast

DOCS_DIR = Path("docs/functions")


def changed_files() -> list[Path]:
    out = subprocess.check_output(["git", "diff", "--name-only", "HEAD~1"], text=True)
    return [Path(p) for p in out.splitlines() if p.endswith(".py")]


def generate_doc(py_file: Path) -> str:
    doc = f"# {py_file.name}\n\n"
    try:
        tree = ast.parse(py_file.read_text())
    except Exception:
        return doc
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if ast.get_docstring(node):
                doc += f"## {node.name}\n" + ast.get_docstring(node) + "\n\n"
    return doc


def main() -> int:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    for py in changed_files():
        doc_path = DOCS_DIR / (py.stem + ".md")
        if not doc_path.exists():
            doc_path.write_text(generate_doc(py), encoding="utf-8")
            print("Doc created for", py)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
