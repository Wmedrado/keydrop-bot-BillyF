import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import user_interface

class DummyVar:
    def __init__(self, value=""):
        self.value = value
    def get(self):
        return self.value
    def set(self, v):
        self.value = v


def test_login_handle_empty(monkeypatch):
    msgs = []
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda t, m: msgs.append(m))
    frame = object.__new__(user_interface.LoginFrame)
    frame.email_var = DummyVar("")
    frame.senha_var = DummyVar("")
    frame.on_login = lambda u: None
    user_interface.LoginFrame._handle_login(frame)
    assert msgs
