import asyncio
import logging
from datetime import datetime
from typing import Optional

from .browser_manager import BrowserManager
from .scheduler import BotScheduler, BotStatus
from ..notifications import send_telegram_message
from ..discord_integration import send_discord_notification
from ..system_monitor.monitor import system_monitor

logger = logging.getLogger(__name__)


class TabWatchdog:
    """Monitora abas inativas e reinicia automaticamente."""

    def __init__(self,
                 browser_manager: BrowserManager,
                 bot_scheduler: Optional[BotScheduler] = None,
                 timeout_seconds: int = 300,
                 enabled: bool = True,
                 telegram_token: str = "",
                 telegram_chat_id: str = "",
                 discord_notifications: bool = False):
        self.browser_manager = browser_manager
        self.bot_scheduler = bot_scheduler
        self.timeout_seconds = timeout_seconds
        self.enabled = enabled
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.discord_notifications = discord_notifications
        self._task: Optional[asyncio.Task] = None
        self._running = False

    def update_config(self,
                      timeout_seconds: Optional[int] = None,
                      enabled: Optional[bool] = None,
                      telegram_token: Optional[str] = None,
                      telegram_chat_id: Optional[str] = None,
                      discord_notifications: Optional[bool] = None):
        if timeout_seconds is not None:
            self.timeout_seconds = timeout_seconds
        if enabled is not None:
            self.enabled = enabled
        if telegram_token is not None:
            self.telegram_token = telegram_token
        if telegram_chat_id is not None:
            self.telegram_chat_id = telegram_chat_id
        if discord_notifications is not None:
            self.discord_notifications = discord_notifications

    def start(self):
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._watch_loop())

    async def stop(self):
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _watch_loop(self):
        logger.info("Watchdog iniciado")
        try:
            while self._running:
                if self.enabled:
                    await self._check_tabs()
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Erro no watchdog: {e}")
        finally:
            logger.info("Watchdog parado")

    async def _check_tabs(self):
        now = datetime.now()

        chrome_processes = system_monitor.get_chrome_processes()
        for proc in chrome_processes:
            if proc.get("memory_mb", 0) > 180:
                for tab_id in list(self.browser_manager.tabs.keys()):
                    await self.browser_manager.restart_tab(tab_id)
                break

        for tab_id, info in list(self.browser_manager.tabs.items()):
            inactivity = (now - info.last_activity).total_seconds()
            if inactivity > self.timeout_seconds and info.status != "closed":
                await self._restart_tab(tab_id, inactivity)

    async def _restart_tab(self, tab_id: int, inactivity: float):
        msg = f"Guia {tab_id} reiniciada após {int(inactivity)}s de inatividade"
        logger.warning(f"{msg} - reinício forçado pelo watchdog")
        restarted = False
        if self.bot_scheduler and self.bot_scheduler.status != BotStatus.STOPPED:
            restarted = await self.bot_scheduler.restart_tab(tab_id)
        else:
            restarted = await self.browser_manager.restart_tab(tab_id)
        if restarted:
            if self.discord_notifications:
                await send_discord_notification("🚨 Aba Reiniciada", msg, "warning")
            if self.telegram_token and self.telegram_chat_id:
                await send_telegram_message(self.telegram_token, self.telegram_chat_id, msg)

