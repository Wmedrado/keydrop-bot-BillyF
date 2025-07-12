import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ci import check_protected_files as cpf  # noqa: E402


def test_check_history_success(tmp_path):
    hist = tmp_path / "history_of_decisions.md"
    hist.write_text("bot_engine/participation.py: refatorado")
    assert cpf.check_history(["bot_engine/participation.py"], hist)


def test_check_history_failure(tmp_path):
    hist = tmp_path / "history_of_decisions.md"
    hist.write_text("nenhuma justificativa")
    assert not cpf.check_history(["bot_engine/participation.py"], hist)


def test_main_no_changes(monkeypatch, tmp_path):
    (tmp_path / "context").mkdir()
    hist = tmp_path / "context" / "history_of_decisions.md"
    hist.write_text("")

    def fake_diff(base_ref, repo_root):
        return []

    monkeypatch.setattr(cpf, "run_git_diff", fake_diff)
    monkeypatch.setattr(cpf, "Path", Path)
    monkeypatch.setattr(
        cpf, "__file__", str(tmp_path / "ci" / "check_protected_files.py")
    )
    assert cpf.main("HEAD") == 0


def test_main_missing_justification(monkeypatch, tmp_path):
    (tmp_path / "context").mkdir()
    hist = tmp_path / "context" / "history_of_decisions.md"
    hist.write_text("")

    def fake_diff(base_ref, repo_root):
        return ["core/contingency_engine.py"]

    monkeypatch.setattr(cpf, "run_git_diff", fake_diff)
    monkeypatch.setattr(cpf, "Path", Path)
    monkeypatch.setattr(
        cpf, "__file__", str(tmp_path / "ci" / "check_protected_files.py")
    )
    assert cpf.main("HEAD") == 1
