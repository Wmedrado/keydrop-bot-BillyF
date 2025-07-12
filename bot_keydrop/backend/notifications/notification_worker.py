import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List
import aiofiles

from ..discord_integration.notifier import send_discord_notification_now

logger = logging.getLogger(__name__)

QUEUE_FILE = Path(__file__).parent / "notifications_queue.json"
MAX_RETRIES = 3


class OfflineNotificationQueue:
    """Simple persistent notification queue backed by a JSON file."""

    @classmethod
    async def load_queue(cls) -> List[Dict[str, Any]]:
        if QUEUE_FILE.exists():
            try:
                async with aiofiles.open(QUEUE_FILE, "r", encoding="utf-8") as f:
                    data = await f.read()
                    return json.loads(data)
            except Exception:
                return []
        return []

    @classmethod
    async def save_queue(cls, queue: List[Dict[str, Any]]) -> None:
        async with aiofiles.open(QUEUE_FILE, "w", encoding="utf-8") as f:
            await f.write(json.dumps(queue, indent=2, ensure_ascii=False))

    @classmethod
    async def enqueue(cls, notification: Dict[str, Any], priority: bool = False) -> None:
        queue = await cls.load_queue()
        if priority:
            queue.insert(0, notification)
        else:
            queue.append(notification)
        await cls.save_queue(queue)

    @classmethod
    async def dequeue(cls) -> Dict[str, Any] | None:
        queue = await cls.load_queue()
        if queue:
            item = queue.pop(0)
            await cls.save_queue(queue)
            return item
        return None


class NotificationWorker:
    """Background worker that processes the offline notification queue."""

    def __init__(self, interval: int = 5):
        self.interval = interval
        self.running = False

    async def start(self) -> None:
        self.running = True
        while self.running:
            await self.process_queue()
            await asyncio.sleep(self.interval)

    async def stop(self) -> None:
        self.running = False
        await asyncio.sleep(0)

    async def process_queue(self) -> None:
        queue = await OfflineNotificationQueue.load_queue()
        if not queue:
            return

        notification = queue[0]
        ntype = notification.get("type")
        data = notification.get("data", {})
        retries = notification.get("retries", 0)

        success = False
        try:
            if ntype == "telegram":
                from .telegram_notifier import send_telegram_message_now
                success = await send_telegram_message_now(**data)
            elif ntype == "discord":
                success = await send_discord_notification_now(**data)
            else:
                logger.error("Tipo de notificação desconhecido: %s", ntype)
                success = True  # descartá-la
        except Exception as e:
            logger.error("Erro ao processar notificação: %s", e)
            success = False

        if success:
            logger.info("Notificação enviada com sucesso: %s", ntype)
            queue.pop(0)
        else:
            retries += 1
            if retries >= MAX_RETRIES:
                logger.error("Falha ao enviar notificação após %d tentativas", retries)
                queue.pop(0)
            else:
                notification["retries"] = retries
                queue[0] = notification
                logger.warning("Tentativa %d falhou, nova tentativa posterior", retries)
        await OfflineNotificationQueue.save_queue(queue)
