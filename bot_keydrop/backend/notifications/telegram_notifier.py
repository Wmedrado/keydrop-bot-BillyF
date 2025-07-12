import logging
import httpx

from .notification_worker import OfflineNotificationQueue

logger = logging.getLogger(__name__)


async def send_telegram_message_now(token: str, chat_id: str, text: str) -> bool:
    """Send a Telegram message immediately without blocking the event loop."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, data={"chat_id": chat_id, "text": text})
        if resp.status_code == 200:
            data = resp.json()
            return data.get("ok", False)
        return False
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem Telegram: {e}")
        return False


async def send_telegram_message(token: str, chat_id: str, text: str, critical: bool = False) -> bool:
    """Queue a Telegram message to be sent by the NotificationWorker."""
    notification = {
        "type": "telegram",
        "data": {"token": token, "chat_id": chat_id, "text": text},
        "critical": critical,
        "retries": 0,
    }
    await OfflineNotificationQueue.enqueue(notification, priority=critical)
    return True
