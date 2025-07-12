import types
import sys
import hashlib
from datetime import datetime
import importlib
from pathlib import Path

import pytest

# Ensure repository root is importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

updates = []


@pytest.fixture(autouse=True)
def stub_firebase(monkeypatch):
    """Provide minimal firebase modules for the tests."""
    fake_fb_client = types.ModuleType("cloud.firebase_client")
    fake_fb_client.initialize_firebase = lambda: None
    monkeypatch.setitem(sys.modules, "cloud.firebase_client", fake_fb_client)

    fake_admin = types.ModuleType("firebase_admin")
    fake_admin.db = None
    fake_admin.auth = types.SimpleNamespace(
        get_user_by_email=lambda e: types.SimpleNamespace(uid="u1"),
        update_user=lambda uid, password: updates.append((uid, password)),
    )
    monkeypatch.setitem(sys.modules, "firebase_admin", fake_admin)

    global password_reset
    if "password_reset" in sys.modules:
        password_reset = importlib.reload(sys.modules["password_reset"])
    else:
        password_reset = importlib.import_module("password_reset")
    password_reset.db = types.SimpleNamespace(
        reference=lambda p: types.SimpleNamespace(delete=lambda: None)
    )
    yield
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    for mod in ["firebase_admin", "cloud.firebase_client", "password_reset"]:
        sys.modules.pop(mod, None)


def setup_module(module):
    updates.clear()


def teardown_module(module):
    sys.modules.pop('firebase_admin', None)
    sys.modules.pop('cloud.firebase_client', None)


def test_request_reset_flow(monkeypatch):
    sent = {}
    store = {}

    def fake_save(uid, token, exp):
        store[uid] = {'token': token, 'exp': exp}

    def fake_send(email, token):
        sent['email'] = email
        sent['token'] = token

    monkeypatch.setattr(password_reset, '_save_token', fake_save)
    monkeypatch.setattr(password_reset, '_send_email', fake_send)

    token = password_reset.request_reset('user@example.com')
    assert sent['email'] == 'user@example.com'
    assert token == sent['token']
    assert store['u1']['token'] == hashlib.sha256(token.encode()).hexdigest()

    def verify(tok):
        hashed = hashlib.sha256(tok.encode()).hexdigest()
        if hashed == store['u1']['token'] and datetime.utcnow() < store['u1']['exp']:
            return 'u1'
        return None

    monkeypatch.setattr(password_reset, 'verify_token', verify)
    password_reset.reset_password(token, 'newpass')
    assert updates == [('u1', 'newpass')]


def test_invalid_token(monkeypatch):
    monkeypatch.setattr(password_reset, 'verify_token', lambda t: None)
    with pytest.raises(ValueError):
        password_reset.reset_password('bad', 'x')
