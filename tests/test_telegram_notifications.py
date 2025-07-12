import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.backend.notifications import telegram_notifier
from bot_keydrop.backend.notifications import notification_worker

class DummyResponse:
    status_code = 200
    def json(self):
        return {"ok": True}

def test_send_telegram_message_now(monkeypatch):
    def fake_post(url, data=None, timeout=0):
        return DummyResponse()
    monkeypatch.setattr(telegram_notifier.requests, "post", fake_post)
    assert telegram_notifier.send_telegram_message_now("t", "c", "msg")

def test_send_telegram_message_queues(tmp_path, monkeypatch):
    qfile = tmp_path / "q.json"
    monkeypatch.setattr(notification_worker, "QUEUE_FILE", qfile)
    telegram_notifier.send_telegram_message("t", "c", "msg")
    try:
        qcontent = qfile.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        qcontent = qfile.read_text(encoding="latin-1")
    data = json.loads(qcontent)
    assert data[0]["type"] == "telegram"
