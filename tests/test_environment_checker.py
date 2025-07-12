
from pathlib import Path
from bot_keydrop.system_safety.environment_checker import (
    executando_no_diretorio_correto,
    verificar_arquivos_obrigatorios,
)
from tkinter import messagebox
from bot_keydrop.system_safety.environment_checker import executando_no_diretorio_correto


def test_executando_no_diretorio_correto(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "launcher.py").write_text("print('hi')")
    (tmp_path / "bot_keydrop").mkdir()
    (tmp_path / "config.json").write_text("{}")
    assert executando_no_diretorio_correto()


def test_verificar_arquivos_obrigatorios_ok(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for name in ("firebase_credentials.json", "config.json", "release_info.json"):
        (tmp_path / name).write_text("{}")
    assert verificar_arquivos_obrigatorios()


def test_verificar_arquivos_obrigatorios_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    popups = []
    monkeypatch.setattr(messagebox, "showerror", lambda t, m: popups.append((t, m)))
    assert not verificar_arquivos_obrigatorios()
    assert popups
