import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ci import pr_structure_validator as psv  # noqa: E402


def test_validator_success(tmp_path):
    body = (
        "### 🌐 Objetivo da alteração\ntexto\n"
        "### 📂 Arquivos principais alterados\nfile.py\n"
        "### 🔍 Impacto em outros módulos\nnenhum\n"
        "### 🧪 Testes existentes cobrem essa lógica?\nSim\n"
        "### 🔒 Algum risco de segurança?\nNão\n"
        "### ✅ Justificativa no history_of_decisions.md\nSim\n"
    )
    report = tmp_path / "report.md"
    assert psv.validate_body(body, report)
    assert report.exists()


def test_validator_failure(tmp_path):
    body = (
        "### 🌐 Objetivo da alteração\n\n"  # empty objective
        "### 📂 Arquivos principais alterados\nfile.py\n"
        "### 🔍 Impacto em outros módulos\nnenhum\n"
        "### 🧪 Testes existentes cobrem essa lógica?\n\n"  # empty
        "### 🔒 Algum risco de segurança?\n\n"  # empty
        "### ✅ Justificativa no history_of_decisions.md\nSim\n"
    )
    report = tmp_path / "report.md"
    assert not psv.validate_body(body, report)
    assert report.exists()
