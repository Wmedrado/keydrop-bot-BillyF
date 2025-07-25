import sys
import builtins
import errno
from pathlib import Path
from unittest import mock
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.system_safety import environment_checker
from bot_keydrop.system_safety.permissions_validator import validar_permissoes
from cloud import firebase_client


def test_internet_connection_failure(monkeypatch):
    def fail(*_args, **_kwargs):
        raise OSError
    monkeypatch.setattr(environment_checker.socket, "create_connection", fail)
    assert environment_checker.verificar_conexao_internet() is False


def test_firebase_offline(monkeypatch, tmp_path):
    monkeypatch.setattr(firebase_client.Path, "exists", lambda self: True)
    monkeypatch.setattr(firebase_client.credentials, "Certificate", lambda p: object())
    def fail_init(*_a, **_k):
        raise ConnectionError("offline")
    monkeypatch.setattr(firebase_client, "initialize_app", fail_init)
    with pytest.raises(ConnectionError):
        firebase_client.initialize_firebase()


def test_permission_denied(monkeypatch, tmp_path):
    def deny(*_a, **_kw):
        raise PermissionError
    monkeypatch.setattr(Path, "mkdir", deny)
    assert validar_permissoes([tmp_path / "data"]) is False




