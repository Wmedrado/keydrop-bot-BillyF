import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ci import pr_structure_validator as psv  # noqa: E402


def test_validator_success(tmp_path):
    body = (
        "## 📌 Objetivo do PR\ntexto\n"
        "## ✅ Alterações principais\n- [x] ajuste\n"
        "## 🧪 Testes executados\n- [x] Teste A\n- [x] Teste B\n"
        "## 🧠 Contexto técnico\nimpl\n"
        "## 📎 Arquivos afetados\nlista\n"
        "## 🧼 Checklist automático\n"
        "- [x] PR validado localmente\n"
        "- [x] Build est\u00e1 passando\n"
        "- [x] Nenhum arquivo de conflito inclu\u00eddo\n"
    )
    report = tmp_path / "report.md"
    assert psv.validate_body(body, report)
    assert report.exists()


def test_validator_failure(tmp_path):
    body = (
        "## 📌 Objetivo do PR\n\n"  # empty objective
        "## ✅ Alterações principais\n- [ ] ajuste\n"
        "## 🧪 Testes executados\n- [ ] Teste A\n- [x] Teste B\n"
        "## 🧠 Contexto técnico\nimpl\n"
        "## 📎 Arquivos afetados\nlista\n"
        "## 🧼 Checklist automático\n"
        "- [ ] PR validado localmente\n"
        "- [x] Build est\u00e1 passando\n"
        "- [ ] Nenhum arquivo de conflito inclu\u00eddo\n"
    )
    report = tmp_path / "report.md"
    assert not psv.validate_body(body, report)
    assert report.exists()
