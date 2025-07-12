import sys
from pathlib import Path
import types

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.system_safety import environment_checker as ec
from bot_keydrop.system_safety.permissions_validator import validar_permissoes
from bot_keydrop.system_safety.backups import backup_arquivo, restaurar_arquivo


def test_verificar_conexao_internet_mock(monkeypatch):
    def fake_create_connection(*args, **kwargs):
        return types.SimpleNamespace()
    monkeypatch.setattr(ec.socket, "create_connection", fake_create_connection)
    assert ec.verificar_conexao_internet()


def test_validar_permissoes(tmp_path):
    assert validar_permissoes([tmp_path])


def test_backup_and_restore(tmp_path):
    p = tmp_path / "test.json"
    p.write_text("data")
    backup = backup_arquivo(p)
    p.unlink()
    restored = restaurar_arquivo(p)
    assert restored is not None
    assert p.exists()
