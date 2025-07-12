"""
API FastAPI para o Bot Keydrop
Fornece endpoints para comunicação com o frontend
"""

import asyncio
import logging
import sys
from datetime import datetime, date
from typing import Dict, List, Optional, Any
import json

from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    BackgroundTasks,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
import uvicorn
import httpx

# Importar módulos do bot
from config import ConfigManager, get_config, save_config
from system_monitor import (
    SystemMonitor,
    get_system_metrics,
    start_system_monitoring,
    stop_system_monitoring,
)
from discord_integration import configure_discord_webhook, send_discord_notification
from bot_logic import (
    browser_manager,
    create_keydrop_automation,
    create_bot_scheduler,
    BotStatus,
    TabWatchdog,
)
from cloud.permissions import (
    fetch_permissions,
    has_premium_access,
    has_telegram_access,
    subscription_active,
)
from tools.proxy_manager import ProxyManager
from . import premium

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="Keydrop Bot Professional API",
    description="API para controle do bot de automação Keydrop",
    version="2.1.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir painel web opcional
ui_directory = Path(__file__).parent / "dashboard"
if ui_directory.exists():
    app.mount("/ui", StaticFiles(directory=str(ui_directory), html=True), name="ui")

# Instâncias globais
config_manager = ConfigManager()
system_monitor = SystemMonitor()
automation_engine = None
bot_scheduler = None
tab_watchdog = None
telegram_bot = None
proxy_manager = None
permissions_data: Dict[str, Any] = {}


# Gerenciamento de WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem WebSocket: {e}")

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Erro ao enviar broadcast: {e}")
                disconnected.append(connection)

        # Remover conexões mortas
        for connection in disconnected:
            self.disconnect(connection)


manager = ConnectionManager()


# Modelos Pydantic
class ConfigUpdateRequest(BaseModel):
    num_tabs: Optional[int] = None
    execution_speed: Optional[float] = None
    retry_attempts: Optional[int] = None
    headless_mode: Optional[bool] = None
    stealth_headless_mode: Optional[bool] = None
    mini_window_mode: Optional[bool] = None
    enable_login_tabs: Optional[bool] = None
    tab_proxies: Optional[Dict[int, str]] = None
    discord_webhook_url: Optional[str] = None
    discord_notifications: Optional[bool] = None
    telegram_enabled: Optional[bool] = None
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    authorized_chat_ids: Optional[List[int]] = None
    watchdog_enabled: Optional[bool] = None
    watchdog_timeout: Optional[int] = None


class BotControlRequest(BaseModel):
    action: str  # 'start', 'stop', 'pause', 'resume', 'emergency_stop'


class TabControlRequest(BaseModel):
    tab_id: int
    action: str  # 'restart', 'close'


class CacheControlRequest(BaseModel):
    preserve_login: bool = True


class WinningRequest(BaseModel):
    amount: float
    lottery_type: str



class ProxyTestRequest(BaseModel):
    proxy: str


class MacroSaveRequest(BaseModel):
    use_first: bool = False

# Inicialização da aplicação
@app.on_event("startup")
async def startup_event():
    """Inicialização da aplicação"""
    global automation_engine, bot_scheduler, tab_watchdog, telegram_bot, proxy_manager

    logger.info("Iniciando API do Keydrop Bot...")

    # Configura gerenciador de proxies e timeout
    config = get_config()
    proxy_manager = ProxyManager(config.proxy_pool, timeout=config.proxy_timeout)
    browser_manager.proxy_manager = proxy_manager
    browser_manager.page_load_timeout = config.page_load_timeout * 1000

    # Carregar permissoes do usuario se houver sessao
    session_file = Path("user_session.json")
    if session_file.exists():
        try:
            uid = json.loads(session_file.read_text()).get("localId")
            if uid:
                permissions_data.update(fetch_permissions(uid))
                if not subscription_active(permissions_data):
                    permissions_data["premium_access"] = False
                    permissions_data["telegram_access"] = False
                if not has_premium_access(permissions_data) and config.num_tabs > 20:
                    config_manager.update_config(num_tabs=20)
                if not has_telegram_access(permissions_data):
                    config_manager.update_config(telegram_enabled=False)
        except Exception as exc:  # pragma: no cover - network or parse errors
            logger.error("Erro ao verificar permissoes: %s", exc)

    # Criar instâncias do bot
    automation_engine = create_keydrop_automation(browser_manager)
    bot_scheduler = create_bot_scheduler(
        browser_manager, automation_engine, config_manager, proxy_manager
    )

    # Inicializar watchdog de abas
    tab_watchdog = TabWatchdog(
        browser_manager,
        bot_scheduler,
        timeout_seconds=config.watchdog_timeout,
        enabled=config.watchdog_enabled,
        telegram_token=config.telegram_bot_token,
        telegram_chat_id=config.telegram_chat_id,
        discord_notifications=config.discord_notifications,
    )
    tab_watchdog.start()

    # Iniciar bot do Telegram se configurado e permitido pelo premium
    if (
        config.telegram_enabled
        and config.telegram_bot_token
        and premium.has_permission("default", "telegram_access")
    ):
        from telegram_control import TelegramControl

        telegram_bot = TelegramControl(
            config.telegram_bot_token,
            config.authorized_chat_ids,
            bot_scheduler,
            browser_manager,
        )
        asyncio.create_task(telegram_bot.start())

    # Configurar callbacks
    bot_scheduler.add_status_callback(on_bot_status_change)
    bot_scheduler.add_task_callback(on_task_completion)

    # Configurar Discord webhook
    if config.discord_webhook_url:
        configure_discord_webhook(config.discord_webhook_url)

    # Iniciar monitoramento de sistema
    asyncio.create_task(start_monitoring_loop())

    logger.info("API iniciada com sucesso")


@app.on_event("shutdown")
async def shutdown_event():
    """Limpeza durante shutdown"""
    logger.info("Encerrando API...")

    # Parar bot se estiver rodando
    if bot_scheduler and bot_scheduler.status != BotStatus.STOPPED:
        await bot_scheduler.stop_bot()

    if tab_watchdog:
        await tab_watchdog.stop()

    if telegram_bot:
        await telegram_bot.stop()

    # Parar monitoramento
    stop_system_monitoring()

    logger.info("API encerrada")


# Callbacks para eventos do bot
async def on_bot_status_change(status: BotStatus, statistics: Any):
    """Callback para mudanças de status do bot"""
    await manager.broadcast(
        {
            "type": "bot_status",
            "data": {
                "status": status.value,
                "statistics": statistics.to_dict(),
                "timestamp": datetime.now().isoformat(),
            },
        }
    )


async def on_task_completion(task: Any):
    """Callback para conclusão de tarefas"""
    await manager.broadcast({"type": "task_completed", "data": task.to_dict()})


# Loop de monitoramento
async def start_monitoring_loop():
    """Inicia loop de monitoramento de sistema"""

    async def metrics_callback(metrics):
        await manager.broadcast(
            {"type": "system_metrics", "data": metrics.to_human_readable()}
        )

    await start_system_monitoring(metrics_callback)


# Endpoints da API


@app.get("/")
def root():
    """Endpoint raiz"""
    return {
        "message": "Keydrop Bot Professional API",
        "version": "2.1.0",
        "developer": "William Medrado (wmedrado) github",
        "status": "online",
    }


@app.get("/health")
def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "bot_status": (
            bot_scheduler.status.value if bot_scheduler else "not_initialized"
        ),
        "browser_running": browser_manager.is_running,
        "active_tabs": browser_manager.get_tab_count(),
    }


# Endpoints de configuração
@app.get("/config")
def get_configuration():
    """Obtém configuração atual"""
    config = get_config()
    return config.dict()


@app.post("/config")
async def update_configuration(request: ConfigUpdateRequest):
    """Atualiza configuração"""
    global tab_watchdog
    try:
        # Converter para dict e remover valores None
        updates = {k: v for k, v in request.dict().items() if v is not None}

        # Atualizar configuração
        success = save_config(**updates)

        if success:
            # Configurar Discord webhook se atualizado
            if "discord_webhook_url" in updates:
                configure_discord_webhook(updates["discord_webhook_url"])

            if tab_watchdog:
                tab_watchdog.update_config(
                    timeout_seconds=updates.get("watchdog_timeout"),
                    enabled=updates.get("watchdog_enabled"),
                    telegram_token=updates.get("telegram_bot_token"),
                    telegram_chat_id=updates.get("telegram_chat_id"),
                    discord_notifications=updates.get("discord_notifications"),
                )

            # Atualizar configuração do agendador se estiver rodando
            if bot_scheduler:
                bot_scheduler.update_config()

            if (
                "telegram_enabled" in updates
                or "telegram_bot_token" in updates
                or "authorized_chat_ids" in updates
            ):
                if telegram_bot:
                    await telegram_bot.stop()
                cfg = get_config()
                if (
                    cfg.telegram_enabled
                    and cfg.telegram_bot_token
                    and premium.has_permission("default", "telegram_access")
                ):
                    from telegram_control import TelegramControl

                    telegram_bot = TelegramControl(
                        cfg.telegram_bot_token,
                        cfg.authorized_chat_ids,
                        bot_scheduler,
                        browser_manager,
                    )
                    asyncio.create_task(telegram_bot.start())

            return {"success": True, "message": "Configuração atualizada com sucesso"}
        else:
            raise HTTPException(status_code=500, detail="Erro ao salvar configuração")

    except Exception as e:
        logger.error(f"Erro ao atualizar configuração: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/config/reset")
async def reset_configuration():
    """Reseta configuração para padrão"""
    global tab_watchdog, telegram_bot
    try:
        success = config_manager.reset_to_defaults()
        if success:
            if tab_watchdog:
                cfg = get_config()
                tab_watchdog.update_config(
                    timeout_seconds=cfg.watchdog_timeout,
                    enabled=cfg.watchdog_enabled,
                    telegram_token=cfg.telegram_bot_token,
                    telegram_chat_id=cfg.telegram_chat_id,
                    discord_notifications=cfg.discord_notifications,
                )
            if telegram_bot:
                await telegram_bot.stop()
            cfg = get_config()
            if (
                cfg.telegram_enabled
                and cfg.telegram_bot_token
                and premium.has_permission("default", "telegram_access")
            ):
                from telegram_control import TelegramControl

                telegram_bot = TelegramControl(
                    cfg.telegram_bot_token,
                    cfg.authorized_chat_ids,
                    bot_scheduler,
                    browser_manager,
                )
                asyncio.create_task(telegram_bot.start())
            return {"success": True, "message": "Configuração resetada para padrão"}
        else:
            raise HTTPException(status_code=500, detail="Erro ao resetar configuração")
    except Exception as e:
        logger.error(f"Erro ao resetar configuração: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints de controle do bot
@app.post("/bot/control")
async def control_bot(request: BotControlRequest, background_tasks: BackgroundTasks):
    """Controla o bot (start, stop, pause, resume)"""
    if not bot_scheduler:
        raise HTTPException(status_code=500, detail="Bot não inicializado")

    try:
        action = request.action.lower()

        if action == "start":
            if bot_scheduler.status == BotStatus.STOPPED:
                background_tasks.add_task(start_bot_background)
                return {"success": True, "message": "Iniciando bot..."}
            else:
                return {"success": False, "message": "Bot já está rodando"}

        elif action == "stop":
            success = await bot_scheduler.stop_bot(emergency=False)
            return {
                "success": success,
                "message": "Bot parado" if success else "Erro ao parar bot",
            }

        elif action == "emergency_stop":
            success = await bot_scheduler.stop_bot(emergency=True)
            return {
                "success": success,
                "message": (
                    "Parada de emergência executada"
                    if success
                    else "Erro na parada de emergência"
                ),
            }

        elif action == "pause":
            success = await bot_scheduler.pause_bot()
            return {
                "success": success,
                "message": "Bot pausado" if success else "Erro ao pausar bot",
            }

        elif action == "resume":
            success = await bot_scheduler.resume_bot()
            return {
                "success": success,
                "message": "Bot resumido" if success else "Erro ao resumir bot",
            }

        else:
            raise HTTPException(status_code=400, detail="Ação inválida")

    except Exception as e:
        logger.error(f"Erro ao controlar bot: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def start_bot_background():
    """Inicia o bot em background"""
    try:
        config = get_config()

        # Enviar notificação de início
        if config.discord_notifications:
            await send_discord_notification(
                "🚀 Bot Iniciado", "O Keydrop Bot foi iniciado com sucesso!", "success"
            )

        success = await bot_scheduler.start_bot()

        if not success and config.discord_notifications:
            await send_discord_notification(
                "❌ Erro ao Iniciar", "Falha ao iniciar o bot", "error"
            )

    except Exception as e:
        logger.error(f"Erro ao iniciar bot em background: {e}")


@app.get("/bot/status")
def get_bot_status():
    """Obtém status atual do bot"""
    if not bot_scheduler:
        return {"status": "not_initialized"}

    return bot_scheduler.get_status()


@app.get("/bot/tasks")
def get_bot_tasks():
    """Obtém status das tarefas do bot"""
    if not bot_scheduler:
        return []

    return bot_scheduler.get_tasks_status()


@app.get("/bot/tabs")
def get_bot_tabs():
    """Obtém status das guias do bot"""
    return browser_manager.get_all_tabs_info()


# Endpoints de controle de guias
@app.post("/tabs/control")
async def control_tab(request: TabControlRequest):
    """Controla uma guia específica"""
    try:
        tab_id = request.tab_id
        action = request.action.lower()

        if action == "restart":
            if bot_scheduler:
                success = await bot_scheduler.restart_tab(tab_id)
            else:
                success = await browser_manager.restart_tab(tab_id)
            return {
                "success": success,
                "message": (
                    f"Guia {tab_id} reiniciada"
                    if success
                    else f"Erro ao reiniciar guia {tab_id}"
                ),
            }

        elif action == "close":
            success = await browser_manager.close_tab(tab_id)
            return {
                "success": success,
                "message": (
                    f"Guia {tab_id} fechada"
                    if success
                    else f"Erro ao fechar guia {tab_id}"
                ),
            }

        else:
            raise HTTPException(status_code=400, detail="Ação inválida")

    except Exception as e:
        logger.error(f"Erro ao controlar guia: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cache/clear")
async def clear_cache(request: CacheControlRequest):
    """Limpa cache do navegador"""
    try:
        if bot_scheduler:
            success = await bot_scheduler.clear_cache(request.preserve_login)
        else:
            success = await browser_manager.clear_cache(request.preserve_login)

        return {
            "success": success,
            "message": (
                f"Cache limpo {'preservando login' if request.preserve_login else 'removendo login'}"
                if success
                else "Erro ao limpar cache"
            ),
        }

    except Exception as e:
        logger.error(f"Erro ao limpar cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints de estatísticas
@app.get("/stats/system")
async def get_system_stats():
    """Obtém estatísticas do sistema"""
    try:
        metrics = await get_system_metrics()
        return metrics.to_human_readable()
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas do sistema: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats/participation")
def get_participation_stats():
    """Obtém estatísticas de participação"""
    if not automation_engine:
        return {"error": "Bot não inicializado"}

    try:
        return automation_engine.get_participation_stats()
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de participação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats/participation/history")
def get_participation_history(limit: Optional[int] = 100):
    """Obtém histórico de participações"""
    if not automation_engine:
        return []

    try:
        return automation_engine.get_participation_history(limit)
    except Exception as e:
        logger.error(f"Erro ao obter histórico de participação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints de ganhos
@app.post("/winnings")
def register_winning(request: WinningRequest):
    """Registra um ganho manualmente"""
    if not automation_engine:
        raise HTTPException(status_code=400, detail="Bot não inicializado")
    try:
        automation_engine.record_winning(request.amount, request.lottery_type)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Erro ao registrar ganho: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/winnings")
def get_winnings_history(limit: Optional[int] = 100):
    """Obtém histórico de ganhos"""
    if not automation_engine:
        return []
    try:
        return automation_engine.get_winnings_history(limit)
    except Exception as e:
        logger.error(f"Erro ao obter histórico de ganhos: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints de relatórios
@app.get("/reports/summary")
async def get_reports_summary():
    """Obtém resumo de relatórios"""
    try:
        bot_status = (
            bot_scheduler.get_status()
            if bot_scheduler
            else {"status": "not_initialized"}
        )
        system_stats = (await get_system_metrics()).to_human_readable()
        participation_stats = (
            automation_engine.get_participation_stats() if automation_engine else {}
        )

        return {
            "bot": bot_status,
            "system": system_stats,
            "participation": participation_stats,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Erro ao gerar resumo de relatórios: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint de análise histórica
@app.get("/analytics/performance")
def get_performance_summary(start_date: Optional[str] = None, end_date: Optional[str] = None):
    """Retorna resumo de performance a partir dos registros históricos."""
    try:
        from tools import PerformanceHistory

        start = datetime.fromisoformat(start_date).date() if start_date else date.today()
        end = datetime.fromisoformat(end_date).date() if end_date else date.today()

        history = PerformanceHistory("default")
        summary = history.summarize(start, end)
        summary["start_date"] = start.isoformat()
        summary["end_date"] = end.isoformat()
        return summary
    except Exception as e:
        logger.error(f"Erro ao obter análise histórica: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint de Discord
@app.post("/discord/test")
async def test_discord_notification():
    """Testa notificação do Discord"""
    try:
        success = await send_discord_notification(
            "🧪 Teste de Notificação",
            "Esta é uma notificação de teste do Keydrop Bot!",
            "info",
        )

        return {
            "success": success,
            "message": (
                "Notificação enviada" if success else "Falha ao enviar notificação"
            ),
        }

    except Exception as e:
        logger.error(f"Erro ao testar Discord: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Diagnostic endpoints
@app.get("/diagnostics/keydrop")
async def diagnostics_keydrop():
    """Teste de conexão com o site Keydrop"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(get_config().keydrop_url)
        return {"success": resp.status_code == 200, "status_code": resp.status_code}
    except Exception as e:
        logger.error(f"Erro no diagnóstico Keydrop: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/diagnostics/login")
async def diagnostics_login():
    """Teste rápido de abertura da página de login"""
    started = False
    try:
        if not browser_manager.is_running:
            started = await browser_manager.start_browser(headless=True)
        await browser_manager.create_tab(-100, automation_engine.URLS['keydrop_main'])
        await asyncio.sleep(5)
        await browser_manager.close_tab(-100)
        if started:
            await browser_manager.stop_browser()
        return {"success": True, "message": "Página de login aberta"}
    except Exception as e:
        logger.error(f"Erro no diagnóstico de login: {e}")
        if started:
            await browser_manager.stop_browser()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/diagnostics/notification")
async def diagnostics_notification():
    """Teste de envio de notificação Discord"""
    try:
        success = await send_discord_notification(
            "🧪 Teste de Notificação",
            "Diagnóstico de integrações do Keydrop Bot",
            "info"
        )
        return {"success": success, "message": "Notificação enviada" if success else "Falha ao enviar"}
    except Exception as e:
        logger.error(f"Erro no diagnóstico de notificação: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/diagnostics/proxy")
async def diagnostics_proxy(request: ProxyTestRequest):
    """Teste de abertura de aba utilizando proxy"""
    started = False
    try:
        if not browser_manager.is_running:
            started = await browser_manager.start_browser(headless=True)
        await browser_manager.create_tab(-101, automation_engine.URLS['keydrop_main'], proxy=request.proxy)
        await asyncio.sleep(5)
        await browser_manager.close_tab(-101)
        if started:
            await browser_manager.stop_browser()
        return {"success": True, "message": "Aba aberta com proxy"}
    except Exception as e:
        logger.error(f"Erro no diagnóstico de proxy: {e}")
        if started:
            await browser_manager.stop_browser()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to teach the bot participation sequence
@app.post("/learning/teach")
async def teach_ai():
    """Open a temporary tab for the user to demonstrate participation."""
    try:
        tab = await browser_manager.create_tab(
            -99, automation_engine.URLS["keydrop_lotteries"]
        )
        if not tab:
            raise Exception("Falha ao criar guia de ensino")
        await automation_engine.learn_participation(-99, learn_time=20)
        await browser_manager.close_tab(-99)
        return {"success": True}
    except Exception as e:
        logger.error(f"Erro no modo de ensino: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Macro recording endpoints
# ---------------------------------------------------------------------------

@app.post("/macros/{tab_id}/start")
async def start_macro(tab_id: int):
    try:
        success = await browser_manager.start_macro_recording(tab_id)
        return {"success": success}
    except Exception as e:
        logger.error(f"Erro ao iniciar macro: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/macros/{tab_id}/pause")
async def pause_macro(tab_id: int):
    try:
        success = await browser_manager.pause_macro_recording(tab_id)
        return {"success": success}
    except Exception as e:
        logger.error(f"Erro ao pausar macro: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/macros/{tab_id}/resume")
async def resume_macro(tab_id: int):
    try:
        success = await browser_manager.resume_macro_recording(tab_id)
        return {"success": success}
    except Exception as e:
        logger.error(f"Erro ao retomar macro: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/macros/{tab_id}/save")
async def save_macro(tab_id: int, request: MacroSaveRequest):
    try:
        path = await browser_manager.save_macro(tab_id, request.use_first)
        if not path:
            raise Exception("Macro não encontrada")
        return {"success": True, "path": str(path)}
    except Exception as e:
        logger.error(f"Erro ao salvar macro: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket para comunicação em tempo real
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para comunicação em tempo real"""
    await manager.connect(websocket)

    try:
        # Enviar status inicial
        initial_data = {
            "type": "initial_data",
            "data": {
                "bot_status": (
                    bot_scheduler.get_status()
                    if bot_scheduler
                    else {"status": "not_initialized"}
                ),
                "config": get_config().dict(),
                "system_metrics": (await get_system_metrics()).to_human_readable(),
            },
        }
        await manager.send_personal_message(initial_data, websocket)

        # Manter conexão ativa
        while True:
            try:
                await websocket.receive_text()
                # Processar mensagens do cliente se necessário
            except WebSocketDisconnect:
                break

    except Exception as e:
        logger.error(f"Erro no WebSocket: {e}")
    finally:
        manager.disconnect(websocket)


# Função para executar a aplicação
def run_server(host: str = "127.0.0.1", port: int = 8000, debug: bool = False):
    """
    Executa o servidor FastAPI

    Args:
        host: Host para bind
        port: Porta para bind
        debug: Modo debug
    """
    uvicorn.run("main:app", host=host, port=port, reload=debug, log_level="info")


if __name__ == "__main__":
    # Detectar se está rodando como executável empacotado
    is_executable = getattr(sys, "frozen", False)
    run_server(debug=not is_executable)
