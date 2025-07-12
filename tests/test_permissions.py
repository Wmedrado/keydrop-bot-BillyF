import sys
from pathlib import Path
import types

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cloud import permissions


def test_subscription_active():
    data = {"expiration_date": "2999-01-01T00:00:00Z"}
    assert permissions.subscription_active(data)
    data = {"expiration_date": "2000-01-01T00:00:00Z"}
    assert not permissions.subscription_active(data)


def test_fetch_permissions(monkeypatch):
    perm = {"premium_access": True}

    class Ref:
        def get(self):
            return perm

    monkeypatch.setattr(permissions, "initialize_firebase", lambda: None)
    monkeypatch.setattr(permissions, "db", types.SimpleNamespace(reference=lambda p: Ref()))
    assert permissions.fetch_permissions("uid") == perm


def test_update_permissions(monkeypatch):
    updates = {"premium_access": False}
    captured = {}

    class Ref:
        def update(self, data):
            captured.update(data)

    monkeypatch.setattr(permissions, "initialize_firebase", lambda: None)
    monkeypatch.setattr(permissions, "db", types.SimpleNamespace(reference=lambda p: Ref()))
    permissions.update_permissions("u", updates)
    assert captured == updates
