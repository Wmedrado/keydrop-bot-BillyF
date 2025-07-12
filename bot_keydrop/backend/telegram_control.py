import logging
from typing import List, Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from bot_logic import BrowserManager, BotScheduler, BotStatus

logger = logging.getLogger(__name__)


class TelegramControl:
    """Bot de controle via Telegram."""

    def __init__(
        self,
        token: str,
        allowed_chat_ids: List[int],
        scheduler: Optional[BotScheduler],
        browser_manager: BrowserManager,
    ):
        self.scheduler = scheduler
        self.browser_manager = browser_manager
        self.allowed_chat_ids = set(allowed_chat_ids)
        self.app = Application.builder().token(token).build()
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("reiniciar", self.cmd_reiniciar))
        self.app.add_handler(CommandHandler("desligar", self.cmd_desligar))
        self.app.add_handler(CommandHandler("logs", self.cmd_logs))
        self.app.add_handler(CommandHandler("saldo", self.cmd_saldo))
        self.app.add_handler(CommandHandler("relatorio", self.cmd_relatorio))
        self.app.add_handler(CallbackQueryHandler(self.on_button))

    def _authorized(self, update: Update) -> bool:
        if not self.allowed_chat_ids:
            return True
        chat = update.effective_chat
        return chat and chat.id in self.allowed_chat_ids

    async def start(self) -> None:
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()

    async def stop(self) -> None:
        await self.app.updater.stop()
        await self.app.stop()

    async def cmd_status(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not self._authorized(update):
            return
        tabs = self.browser_manager.get_all_tabs_info()
        lines = ["🔍 Status das Guias\n"]
        buttons = []
        for tab in tabs:
            tid = tab.get("tab_id")
            status = tab.get("status")
            icon = "🟢" if status != "closed" else "❌"
            lines.append(f"{icon} Guia {tid} — {status}")
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"🔁 Reiniciar Guia {tid}", callback_data=f"restart:{tid}"
                    )
                ]
            )
        text = "\n".join(lines)
        markup = InlineKeyboardMarkup(buttons) if buttons else None
        if update.message:
            await update.message.reply_text(text, reply_markup=markup)
        else:
            await update.callback_query.message.edit_text(text, reply_markup=markup)

    def _parse_tab_id(self, args: List[str]) -> Optional[int]:
        if not args:
            return None
        if args[0].lower() == "guia" and len(args) >= 2 and args[1].isdigit():
            return int(args[1])
        if args[0].isdigit():
            return int(args[0])
        return None

    async def _restart_tab(self, tab_id: int) -> bool:
        if tab_id < 1 or tab_id > self.browser_manager.get_tab_count():
            return False
        if self.scheduler and self.scheduler.status != BotStatus.STOPPED:
            return await self.scheduler.restart_tab(tab_id)
        return await self.browser_manager.restart_tab(tab_id)

    async def cmd_reiniciar(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not self._authorized(update):
            return
        tab_id = self._parse_tab_id(context.args)
        if tab_id is None:
            await update.message.reply_text("Uso: /reiniciar guia <número>")
            return
        success = await self._restart_tab(tab_id)
        if success:
            await update.message.reply_text(f"✅ Guia {tab_id} reiniciada com sucesso")
        else:
            await update.message.reply_text(f"⚠️ Guia {tab_id} não existe")

    async def on_button(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not self._authorized(update):
            return
        query = update.callback_query
        await query.answer()
        data = query.data
        if data.startswith("restart:"):
            tab_id = int(data.split(":", 1)[1])
            success = await self._restart_tab(tab_id)
            if success:
                await query.edit_message_text(
                    f"✅ Guia {tab_id} reiniciada com sucesso"
                )
            else:
                await query.edit_message_text(f"⚠️ Guia {tab_id} não existe")

    async def cmd_desligar(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not self._authorized(update):
            return
        if self.scheduler:
            success = await self.scheduler.stop_bot(emergency=False)
            msg = "✅ Bot desligado" if success else "❌ Falha ao desligar"
        else:
            success = await self.browser_manager.stop_browser()
            msg = "✅ Bot desligado" if success else "❌ Falha ao desligar"
        await update.message.reply_text(msg)

    async def cmd_logs(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not self._authorized(update):
            return
        tab_id = self._parse_tab_id(context.args)
        if tab_id is None:
            await update.message.reply_text("Uso: /logs guia <número>")
            return
        await update.message.reply_text(f"Logs da guia {tab_id} não disponíveis.")

    async def cmd_saldo(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not self._authorized(update):
            return
        await update.message.reply_text("Saldo atual não disponível.")

    async def cmd_relatorio(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        if not self._authorized(update):
            return
        if self.scheduler:
            stats = self.scheduler.statistics.to_dict()
            text = (
                "📊 Relatório Atual\n"
                f"Tarefas executadas: {stats.get('total_tasks_executed')}\n"
                f"Sucessos: {stats.get('successful_tasks')}\n"
                f"Falhas: {stats.get('failed_tasks')}\n"
                f"Uptime: {stats.get('uptime')}"
            )
        else:
            text = "Relatório indisponível"
        await update.message.reply_text(text)
