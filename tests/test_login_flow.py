import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import user_interface  # noqa: E402


class DummyVar:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def set(self, v):
        self.value = v


def test_login_handle_empty(monkeypatch):
    msgs = []
    monkeypatch.setattr(
        "tkinter.messagebox.showerror",
        lambda t, m: msgs.append(m),
    )
    frame = object.__new__(user_interface.LoginFrame)
    frame.email_var = DummyVar("")
    frame.senha_var = DummyVar("")
    frame.on_login = lambda u: None
    user_interface.LoginFrame._handle_login(frame)
    assert msgs


def test_login_via_discord(monkeypatch):
    info = {
        "id": "d1",
        "username": "foo",
        "email": "bar@example.com",
        "token": "t",
    }
    monkeypatch.setattr(user_interface, "oauth_login", lambda: info)

    class Auth:
        def sign_in_with_custom_token(self, tok):
            return {"idToken": "i", "refreshToken": "r", "localId": "uid"}

    monkeypatch.setattr(
        user_interface,
        "_load_pyrebase",
        lambda: types.SimpleNamespace(auth=lambda: Auth()),
    )
    monkeypatch.setattr(user_interface, "_save_session", lambda u: None)
    fake_auth = types.SimpleNamespace(
        get_user_by_email=lambda e: types.SimpleNamespace(uid="uid"),
        create_user=lambda **kw: types.SimpleNamespace(uid="uid"),
        create_custom_token=lambda uid: b"tok",
    )
    monkeypatch.setitem(
        sys.modules, "firebase_admin", types.SimpleNamespace(auth=fake_auth)
    )
    monkeypatch.setattr(user_interface, "initialize_firebase", lambda: None)
    calls = {}
    monkeypatch.setattr(
        user_interface,
        "salvar_discord_info",
        lambda uid, d: calls.setdefault("discord", d),
    )

    user = user_interface.login_via_discord()
    assert user["discord"]["id"] == "d1"
    assert "discord" in calls
