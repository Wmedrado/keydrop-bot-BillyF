import sys
from pathlib import Path
import types

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import importlib
import pytest

sys.modules.setdefault(
    "discord_webhook",
    types.SimpleNamespace(DiscordWebhook=object, DiscordEmbed=object),
)

sys.modules.setdefault(
    "discord_integration",
    importlib.import_module("bot_keydrop.backend.discord_integration"),
)

from bot_keydrop.backend.tools import release_news

class FakeResponse:
    def __init__(self, data=None, raise_json=False):
        self._data = data or {}
        self._raise_json = raise_json

    def raise_for_status(self):
        pass

    def json(self):
        if self._raise_json:
            raise ValueError("bad json")
        return self._data

def test_get_latest_release_connection_error(monkeypatch):
    def fake_get(*args, **kwargs):
        import requests
        raise requests.ConnectionError("offline")
    monkeypatch.setattr(release_news.requests, "get", fake_get)
    result = release_news.get_latest_release("foo/bar")
    assert result.get("error") == "Erro ao buscar atualização"

def test_get_latest_release_malformed_json(monkeypatch):
    monkeypatch.setattr(release_news.requests, "get", lambda *a, **k: FakeResponse(raise_json=True))
    result = release_news.get_latest_release("foo/bar")
    assert result.get("error") == "Resposta malformada"

@pytest.mark.asyncio
async def test_main_handles_failure(monkeypatch):
    monkeypatch.setattr(release_news.requests, "get", lambda *a, **k: FakeResponse())

    async def dummy_notify(*args, **kwargs):
        return None

    monkeypatch.setattr(release_news, "notify_discord", dummy_notify)
    await release_news.main()
