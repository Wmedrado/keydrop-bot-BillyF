import sys
from pathlib import Path
import types
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.backend.discord_integration import notifier

class DummyWebhook:
    def __init__(self, *a, **k):
        pass
    def add_embed(self, embed):
        self.embed = embed
    def execute(self):
        class Resp:
            status_code = 200
        return Resp()

@pytest.mark.asyncio
async def test_send_discord_notification_now(monkeypatch):
    monkeypatch.setattr(notifier, "DiscordWebhook", DummyWebhook)
    async def fake_send_custom_notification(title, description, notification_type='info', **kw):
        return True
    monkeypatch.setattr(notifier.discord_notifier, "send_custom_notification", fake_send_custom_notification)
    ok = await notifier.send_discord_notification_now(title="t", description="d")
    assert ok
