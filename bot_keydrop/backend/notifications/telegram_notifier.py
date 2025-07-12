import logging
import requests

from .notification_worker import OfflineNotificationQueue

logger = logging.getLogger(__name__)


def send_telegram_message_now(token: str, chat_id: str, text: str) -> bool:
    """Send a Telegram message immediately."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, data={'chat_id': chat_id, 'text': text}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('ok', False)
        return False
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem Telegram: {e}")
        return False


def send_telegram_message(token: str, chat_id: str, text: str, critical: bool = False) -> bool:
    """Queue a Telegram message to be sent by the NotificationWorker."""
    notification = {
        "type": "telegram",
        "data": {"token": token, "chat_id": chat_id, "text": text},
        "critical": critical,
        "retries": 0,
    }
    OfflineNotificationQueue.enqueue(notification, priority=critical)
    return True
