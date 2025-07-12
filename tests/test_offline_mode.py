import sys
import json
import asyncio
from pathlib import Path
from unittest import mock
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.backend.discord_integration.notifier import send_discord_notification
from bot_keydrop.backend.notifications.telegram_notifier import send_telegram_message
from bot_keydrop.backend.notifications import notification_worker
from bot_keydrop.keydrop_bot_desktop_v4 import KeydropBotGUI


@pytest.mark.asyncio
async def test_discord_notification_queued_offline(tmp_path, monkeypatch):
    queue_file = tmp_path / "queue.json"
    monkeypatch.setattr(notification_worker, "QUEUE_FILE", queue_file)
    await send_discord_notification("Title", "Desc")
    try:
        qcontent = queue_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        qcontent = queue_file.read_text(encoding="latin-1")
    data = json.loads(qcontent)
    assert data[0]["type"] == "discord"


def test_telegram_notification_queued_offline(tmp_path, monkeypatch):
    queue_file = tmp_path / "queue.json"
    monkeypatch.setattr(notification_worker, "QUEUE_FILE", queue_file)
    send_telegram_message("tok", "chat", "msg")
    try:
        qcontent = queue_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        qcontent = queue_file.read_text(encoding="latin-1")
    data = json.loads(qcontent)
    assert data[0]["type"] == "telegram"


@pytest.mark.asyncio
async def test_worker_retry_on_failure(monkeypatch, tmp_path):
    queue_file = tmp_path / "queue.json"
    monkeypatch.setattr(notification_worker, "QUEUE_FILE", queue_file)
    notification_worker.OfflineNotificationQueue.enqueue({"type": "discord", "data": {"title": "t", "description": "d"}, "retries": 0})

    async def fail_send(**kwargs):
        raise RuntimeError("offline")

    monkeypatch.setattr(notification_worker, "send_discord_notification_now", fail_send)
    worker = notification_worker.NotificationWorker(interval=0)
    await worker.process_queue()
    try:
        qcontent = queue_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        qcontent = queue_file.read_text(encoding="latin-1")
    data = json.loads(qcontent)
    assert data[0]["retries"] == 1


def test_gui_starts_with_failed_integrations(monkeypatch):
    monkeypatch.setattr(KeydropBotGUI, 'start_monitoring', lambda self: None)
    dummy = mock.MagicMock()
    monkeypatch.setattr('tkinter.Tk', dummy)
    monkeypatch.setattr('tkinter.StringVar', dummy)
    monkeypatch.setattr('tkinter.BooleanVar', dummy)
    with mock.patch('cloud.firebase_client.initialize_firebase', side_effect=RuntimeError('offline')):
        gui = KeydropBotGUI()
    assert dummy.called
