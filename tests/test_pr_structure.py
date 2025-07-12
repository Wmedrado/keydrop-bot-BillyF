import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ci import check_pr_structure as cps  # noqa: E402


def test_validate_success(tmp_path):
    body = (
        "### 🌐 Objetivo da alteração\ntexto\n"
        "### 📂 Arquivos principais alterados\nfile1.py\n"
        "### 🔍 Impacto em outros módulos\nnenhum\n"
        "### 🧪 Testes existentes cobrem essa lógica?\nSim\n"
        "### 🔒 Algum risco de segurança?\nNão\n"
        "### ✅ Justificativa no history_of_decisions.md\nSim\n"
    )
    report = tmp_path / "report.md"
    assert cps.validate_body(body, report)
    assert report.exists()


def test_validate_missing(tmp_path):
    body = (
        "### 🌐 Objetivo da alteração\ntexto\n"
        "### 📂 Arquivos principais alterados\n\n"  # empty section
        "### 🔍 Impacto em outros módulos\nnenhum\n"
        "### 🧪 Testes existentes cobrem essa lógica?\n\n"  # empty
        "### 🔒 Algum risco de segurança?\nNão\n"
    )
    report = tmp_path / "report.md"
    assert not cps.validate_body(body, report)
    assert report.exists()
