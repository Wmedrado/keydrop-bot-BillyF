import sys
import asyncio
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.backend.discord_integration import notifier as discord_notifier
from bot_keydrop.backend.notifications import telegram_notifier


class DummyResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._data = json_data or {}

    def json(self):
        return self._data


def test_send_telegram_message_now_success(monkeypatch):
    def fake_post(url, data=None, timeout=10):
        assert 'bottoken' in url
        return DummyResponse(200, {'ok': True})

    monkeypatch.setattr(telegram_notifier.requests, 'post', fake_post)
    assert telegram_notifier.send_telegram_message_now('token', 'chat', 'hi')


def test_send_telegram_message_now_error_logged(monkeypatch, caplog):
    def fake_post(*args, **kwargs):
        raise RuntimeError('fail')

    monkeypatch.setattr(telegram_notifier.requests, 'post', fake_post)
    with caplog.at_level(logging.ERROR):
        assert telegram_notifier.send_telegram_message_now('t', 'c', 'x') is False
        assert 'Erro ao enviar mensagem Telegram' in caplog.text


def test_send_telegram_message_enqueues(monkeypatch):
    calls = []
    monkeypatch.setattr(
        telegram_notifier.OfflineNotificationQueue,
        'enqueue',
        lambda n, priority=False: calls.append((n, priority)),
    )
    telegram_notifier.send_telegram_message('t', 'c', 'msg', critical=True)
    assert calls
    n, pr = calls[0]
    assert n['type'] == 'telegram'
    assert pr is True


def test_discord_send_notification_success(monkeypatch):
    class FakeWebhook:
        def __init__(self, url, username=None):
            self.url = url
        def add_embed(self, e):
            pass
        def execute(self):
            return DummyResponse(200)

    monkeypatch.setattr(discord_notifier, 'DiscordWebhook', FakeWebhook)
    notif = discord_notifier.NotificationData(title='t', description='d')
    discord = discord_notifier.DiscordNotifier('http://webhook')
    assert asyncio.run(discord.send_notification(notif))


def test_discord_send_notification_logs_error(monkeypatch, caplog):
    class FakeWebhook:
        def __init__(self, url, username=None):
            pass
        def add_embed(self, e):
            pass
        def execute(self):
            return DummyResponse(500)

    monkeypatch.setattr(discord_notifier, 'DiscordWebhook', FakeWebhook)
    notif = discord_notifier.NotificationData(title='t', description='d')
    discord = discord_notifier.DiscordNotifier('http://webhook')
    with caplog.at_level(logging.ERROR):
        result = asyncio.run(discord.send_notification(notif))
        assert not result
        assert 'Erro ao enviar notificação Discord' in caplog.text


def test_send_discord_notification_enqueues(monkeypatch):
    calls = []
    monkeypatch.setattr(
        'bot_keydrop.backend.notifications.notification_worker.OfflineNotificationQueue.enqueue',
        lambda n, priority=False: calls.append((n, priority)),
    )
    asyncio.run(discord_notifier.send_discord_notification('t', 'd', critical=True))
    assert calls
    n, pr = calls[0]
    assert n['type'] == 'discord'
    assert pr is True
