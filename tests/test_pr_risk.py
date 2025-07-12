import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ci.classify_pr_risk import classify_files, generate_report  # noqa: E402


def test_classify_high():
    files = ["bot_keydrop/backend/bot_logic/browser_manager.py"]
    assert classify_files(files) == "Alto Risco"


def test_classify_medium():
    files = ["bot_keydrop/frontend/index.html"]
    assert classify_files(files) == "Médio Risco"


def test_generate_report(tmp_path):
    (tmp_path / "ci").mkdir()
    report = generate_report(["docs/readme.md"], "Baixo Risco", tmp_path)
    assert report.exists()
    with report.open("r", encoding="utf-8") as f:
        text = f.read()
    assert "Baixo Risco" in text
    assert "docs/readme.md" in text
