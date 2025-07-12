from pathlib import Path
from bot_keydrop.system_safety.environment_checker import executando_no_diretorio_correto


def test_executando_no_diretorio_correto(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "launcher.py").write_text("print('hi')")
    (tmp_path / "bot_keydrop").mkdir()
    (tmp_path / "config.json").write_text("{}")
    assert executando_no_diretorio_correto()
