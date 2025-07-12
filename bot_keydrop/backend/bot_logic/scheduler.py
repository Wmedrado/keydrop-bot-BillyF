"""
Agendador de tarefas
Gerencia a execução assíncrona das tarefas em cada guia e controla o ciclo entre as guias
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BotStatus(Enum):
    """Status do bot"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    PAUSING = "pausing"
    PAUSED = "paused"
    STOPPING = "stopping"
    ERROR = "error"


class TaskStatus(Enum):
    """Status de uma tarefa"""
    PENDING = "pending"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ScheduledTask:
    """Representa uma tarefa agendada"""
    task_id: str
    tab_id: int
    task_type: str  # 'participate', 'navigate', 'wait'
    next_execution: datetime
    interval: timedelta
    status: TaskStatus = TaskStatus.PENDING
    retry_count: int = 0
    max_retries: int = 5
    last_execution: Optional[datetime] = None
    last_result: Optional[str] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'task_id': self.task_id,
            'tab_id': self.tab_id,
            'task_type': self.task_type,
            'next_execution': self.next_execution.isoformat(),
            'interval': self.interval.total_seconds(),
            'status': self.status.value,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'last_execution': self.last_execution.isoformat() if self.last_execution else None,
            'last_result': self.last_result,
            'error_message': self.error_message
        }


@dataclass
class BotStatistics:
    """Estatísticas do bot"""
    start_time: Optional[datetime] = None
    total_tasks_executed: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    active_tabs: int = 0
    current_cycle: int = 0
    last_activity: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        uptime = datetime.now() - self.start_time if self.start_time else timedelta(0)
        success_rate = (self.successful_tasks / self.total_tasks_executed * 100) if self.total_tasks_executed > 0 else 0
        
        return {
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'uptime': str(uptime),
            'total_tasks_executed': self.total_tasks_executed,
            'successful_tasks': self.successful_tasks,
            'failed_tasks': self.failed_tasks,
            'success_rate': round(success_rate, 2),
            'active_tabs': self.active_tabs,
            'current_cycle': self.current_cycle,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None
        }


class BotScheduler:
    """Agendador principal do bot"""
    
    def __init__(self, browser_manager, automation_engine, config_manager, proxy_manager=None):
        """
        Inicializa o agendador
        
        Args:
            browser_manager: Gerenciador de navegador
            automation_engine: Engine de automação
            config_manager: Gerenciador de configurações
        """
        self.browser_manager = browser_manager
        self.automation_engine = automation_engine
        self.config_manager = config_manager
        self.proxy_manager = proxy_manager
        
        self.status = BotStatus.STOPPED
        self.tasks: Dict[str, ScheduledTask] = {}
        self.statistics = BotStatistics()

        # Histórico de falhas por aba
        self.last_lottery_type: Dict[int, Optional[str]] = {}
        self.consecutive_failures: Dict[int, int] = {}
        
        # Configurações
        self.config = self.config_manager.get_config()
        self.update_config()
        
        # Controle de execução
        self.is_running = False
        self.should_stop = False
        self.main_task: Optional[asyncio.Task] = None
        self.task_semaphore = asyncio.Semaphore(10)  # Limitar tarefas concorrentes
        
        # Callbacks
        self.status_callbacks: List[Callable] = []
        self.task_callbacks: List[Callable] = []
        
        logger.info("Bot Scheduler inicializado")
    
    def update_config(self):
        """Atualiza configurações do agendador"""
        self.config = self.config_manager.get_config()
        self.num_tabs = self.config.num_tabs
        self.execution_speed = self.config.execution_speed
        self.retry_attempts = self.config.retry_attempts
        self.amateur_wait_time = self.config.amateur_lottery_wait_time
        self.action_delay = self.config.wait_time_between_actions
        self.tab_proxies = self.config.tab_proxies
        self.proxy_timeout = self.config.proxy_timeout
        if self.proxy_manager:
            self.proxy_manager.timeout = self.proxy_timeout
        self.failure_threshold = self.config.failure_reschedule_threshold
        self.reschedule_delay = self.config.failure_reschedule_delay

        logger.info("Configurações do agendador atualizadas")
    
    async def start_bot(self) -> bool:
        """
        Inicia o bot
        
        Returns:
            True se iniciou com sucesso
        """
        if self.status != BotStatus.STOPPED:
            logger.warning("Bot já está rodando ou em processo de inicialização")
            return False
        
        try:
            logger.info("Iniciando bot...")
            self.status = BotStatus.STARTING
            await self._notify_status_change()
            
            # Atualizar configurações
            self.update_config()

            # Resetar histórico de falhas
            self.last_lottery_type.clear()
            self.consecutive_failures.clear()

            # Inicializar estatísticas
            self.statistics = BotStatistics(start_time=datetime.now())
            
            # Iniciar navegador se não estiver rodando
            if not self.browser_manager.is_running:
                params = {
                    "headless": self.config.headless_mode or self.config.stealth_headless_mode,
                    "mini_window": self.config.mini_window_mode,
                }
                import inspect
                if "stealth" in inspect.signature(self.browser_manager.start_browser).parameters:
                    params["stealth"] = self.config.stealth_headless_mode

                browser_started = await self.browser_manager.start_browser(**params)
                if not browser_started:
                    self.status = BotStatus.ERROR
                    await self._notify_status_change()
                    return False
            
            # Configurar guias de login se necessário
            if self.config.enable_login_tabs:
                success, login_tabs = await self.automation_engine.setup_login_tabs()
                if success:
                    logger.info(f"Aguardando login manual nas guias: {login_tabs}")
                    # Aguardar um tempo para login manual
                    await asyncio.sleep(30)  # 30 segundos para login
            
            # Criar guias e tarefas
            await self._create_tabs_and_tasks()
            
            # Iniciar loop principal
            self.is_running = True
            self.should_stop = False
            self.main_task = asyncio.create_task(self._main_loop())
            
            self.status = BotStatus.RUNNING
            await self._notify_status_change()
            
            logger.info(f"Bot iniciado com sucesso - {self.num_tabs} guias configuradas")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao iniciar bot: {e}")
            self.status = BotStatus.ERROR
            await self._notify_status_change()
            return False
    
    async def stop_bot(self, emergency: bool = False) -> bool:
        """
        Para o bot
        
        Args:
            emergency: Parada de emergência
            
        Returns:
            True se parou com sucesso
        """
        if self.status == BotStatus.STOPPED:
            logger.info("Bot já está parado")
            return True
        
        try:
            logger.info(f"Parando bot - Emergência: {emergency}")
            self.status = BotStatus.STOPPING
            await self._notify_status_change()
            
            # Parar loop principal
            self.should_stop = True
            self.is_running = False
            
            if self.main_task and not self.main_task.done():
                self.main_task.cancel()
                try:
                    await self.main_task
                except asyncio.CancelledError:
                    pass
            
            # Cancelar todas as tarefas
            await self._cancel_all_tasks()
            
            # Parar navegador
            if emergency:
                await self.browser_manager.emergency_stop()
            else:
                await self.browser_manager.stop_browser()
            
            self.status = BotStatus.STOPPED
            await self._notify_status_change()
            
            logger.info("Bot parado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao parar bot: {e}")
            return False
    
    async def pause_bot(self) -> bool:
        """
        Pausa o bot
        
        Returns:
            True se pausou com sucesso
        """
        if self.status != BotStatus.RUNNING:
            return False
        
        try:
            self.status = BotStatus.PAUSING
            await self._notify_status_change()
            
            self.is_running = False
            
            self.status = BotStatus.PAUSED
            await self._notify_status_change()
            
            logger.info("Bot pausado")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao pausar bot: {e}")
            return False
    
    async def resume_bot(self) -> bool:
        """
        Resume o bot
        
        Returns:
            True se resumiu com sucesso
        """
        if self.status != BotStatus.PAUSED:
            return False
        
        try:
            self.is_running = True
            
            if not self.main_task or self.main_task.done():
                self.main_task = asyncio.create_task(self._main_loop())
            
            self.status = BotStatus.RUNNING
            await self._notify_status_change()
            
            logger.info("Bot resumido")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao resumir bot: {e}")
            return False
    
    async def restart_tab(self, tab_id: int, proxy: Optional[str] = None) -> bool:
        """
        Reinicia uma guia específica
        
        Args:
            tab_id: ID da guia
            
        Returns:
            True se reiniciou com sucesso
        """
        try:
            # Cancelar tarefas da guia
            tasks_to_cancel = [
                task for task in self.tasks.values()
                if task.tab_id == tab_id
            ]
            
            for task in tasks_to_cancel:
                task.status = TaskStatus.CANCELLED

            # Reiniciar guia no navegador
            success = await self.browser_manager.restart_tab(tab_id, proxy=proxy)

            if success:
                # Recriar tarefas para a guia
                await self._create_tasks_for_tab(tab_id)
                self.consecutive_failures.pop(tab_id, None)
                self.last_lottery_type.pop(tab_id, None)
                logger.info(f"Guia {tab_id} reiniciada com sucesso")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao reiniciar guia {tab_id}: {e}")
            return False
    
    async def clear_cache(self, preserve_login: bool = True) -> bool:
        """
        Limpa cache do navegador
        
        Args:
            preserve_login: Manter dados de login
            
        Returns:
            True se limpou com sucesso
        """
        try:
            success = await self.browser_manager.clear_cache(preserve_login)
            if success:
                logger.info(f"Cache limpo - Login preservado: {preserve_login}")
            return success
            
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {e}")
            return False
    
    async def _create_tabs_and_tasks(self):
        """Cria guias e tarefas iniciais"""
        logger.info(f"Criando {self.num_tabs} guias e tarefas...")
        
        for tab_id in range(1, self.num_tabs + 1):
            proxy = None
            if self.proxy_manager:
                proxy = self.proxy_manager.get_proxy(tab_id)
            else:
                proxy = self.tab_proxies.get(tab_id)

            tab_info = await self.browser_manager.create_tab(tab_id, proxy=proxy)
            if tab_info:
                self.statistics.active_tabs += 1
                
                # Navegar para página de sorteios
                await self.automation_engine.navigate_to_lotteries(tab_id)
                
                # Criar tarefas para a guia
                await self._create_tasks_for_tab(tab_id)
                
                # Delay entre criação de guias para evitar sobrecarga
                await asyncio.sleep(self.action_delay / self.execution_speed)
            else:
                logger.error(f"Falha ao criar guia {tab_id}")
    
    async def _create_tasks_for_tab(self, tab_id: int):
        """
        Cria tarefas para uma guia específica
        
        Args:
            tab_id: ID da guia
        """
        # Calcular próxima execução (distribuir guias ao longo do tempo)
        base_delay = (tab_id - 1) * (self.amateur_wait_time / self.num_tabs)
        next_execution = datetime.now() + timedelta(seconds=base_delay)
        
        # Criar tarefa de participação
        task_id = f"participate_{tab_id}"
        participate_task = ScheduledTask(
            task_id=task_id,
            tab_id=tab_id,
            task_type="participate",
            next_execution=next_execution,
            interval=timedelta(seconds=self.amateur_wait_time),
            max_retries=self.retry_attempts
        )
        
        self.tasks[task_id] = participate_task
        logger.debug(f"Tarefa {task_id} criada para execução em {next_execution}")
    
    async def _main_loop(self):
        """Loop principal do agendador"""
        logger.info("Loop principal do agendador iniciado")
        
        try:
            while self.is_running and not self.should_stop:
                current_time = datetime.now()
                
                # Processar tarefas pendentes
                ready_tasks = [
                    task for task in self.tasks.values()
                    if task.status == TaskStatus.PENDING and task.next_execution <= current_time
                ]
                
                # Executar tarefas prontas
                if ready_tasks:
                    await self._execute_tasks(ready_tasks)
                
                # Atualizar estatísticas
                self.statistics.last_activity = current_time
                self.statistics.active_tabs = self.browser_manager.get_tab_count()
                
                # Aguardar antes da próxima verificação
                await asyncio.sleep(1.0 / self.execution_speed)
                
        except asyncio.CancelledError:
            logger.info("Loop principal cancelado")
        except Exception as e:
            logger.error(f"Erro no loop principal: {e}")
            self.status = BotStatus.ERROR
            await self._notify_status_change()
    
    async def _execute_tasks(self, tasks: List[ScheduledTask]):
        """
        Executa uma lista de tarefas
        
        Args:
            tasks: Lista de tarefas para executar
        """
        # Limitar número de tarefas concorrentes
        semaphore_tasks = []
        
        for task in tasks[:10]:  # Máximo 10 tarefas por vez
            semaphore_task = asyncio.create_task(
                self._execute_single_task(task)
            )
            semaphore_tasks.append(semaphore_task)
        
        # Aguardar conclusão de todas as tarefas
        if semaphore_tasks:
            await asyncio.gather(*semaphore_tasks, return_exceptions=True)
    
    async def _execute_single_task(self, task: ScheduledTask):
        """
        Executa uma única tarefa
        
        Args:
            task: Tarefa a ser executada
        """
        async with self.task_semaphore:
            try:
                task.status = TaskStatus.RUNNING
                task.last_execution = datetime.now()
                
                logger.debug(f"Executando tarefa {task.task_id}")
                
                success = False
                
                if task.task_type == "participate":
                    # Verificar se a guia está pronta
                    if self.browser_manager.is_tab_ready(task.tab_id):
                        result = await self.automation_engine.participate_in_lottery(
                            task.tab_id,
                            max_retries=1  # Uma tentativa por execução da tarefa
                        )
                        success = result.result.value == "success"
                        task.last_result = result.result.value

                        # Atualizar histórico de falhas para reagendamento inteligente
                        lot_type = result.lottery_type
                        if success:
                            self.consecutive_failures[task.tab_id] = 0
                            self.last_lottery_type[task.tab_id] = None
                        else:
                            if lot_type == self.last_lottery_type.get(task.tab_id):
                                self.consecutive_failures[task.tab_id] = self.consecutive_failures.get(task.tab_id, 0) + 1
                            else:
                                self.consecutive_failures[task.tab_id] = 1
                                self.last_lottery_type[task.tab_id] = lot_type
                        
                        if result.error_message:
                            task.error_message = result.error_message
                    else:
                        task.error_message = "Guia não está pronta"
                
                # Atualizar estatísticas
                self.statistics.total_tasks_executed += 1
                
                if success:
                    task.status = TaskStatus.COMPLETED
                    task.retry_count = 0
                    self.statistics.successful_tasks += 1

                    # Agendar próxima execução
                    task.next_execution = datetime.now() + task.interval
                    task.status = TaskStatus.PENDING

                else:
                    task.retry_count += 1
                    self.statistics.failed_tasks += 1

                    if task.retry_count >= task.max_retries:
                        # Reiniciar guia após múltiplas falhas
                        logger.warning(
                            f"Reiniciando guia {task.tab_id} após {task.retry_count} falhas"
                        )
                        new_proxy = None
                        if self.proxy_manager:
                            new_proxy = self.proxy_manager.report_failure(
                                task.tab_id, task.error_message or ""
                            )
                        await self.restart_tab(task.tab_id, proxy=new_proxy)
                    else:
                        # Verificar falhas consecutivas para reagendar com atraso maior
                        fail_count = self.consecutive_failures.get(task.tab_id, 0)
                        if fail_count >= self.failure_threshold:
                            task.next_execution = datetime.now() + timedelta(seconds=self.reschedule_delay)
                            self.consecutive_failures[task.tab_id] = 0
                        else:
                            retry_delay = timedelta(seconds=30 * task.retry_count)
                            task.next_execution = datetime.now() + retry_delay
                        task.status = TaskStatus.PENDING
                
                # Notificar callbacks
                await self._notify_task_completion(task)
                
            except Exception as e:
                logger.error(f"Erro ao executar tarefa {task.task_id}: {e}")
                task.status = TaskStatus.FAILED
                task.error_message = str(e)
                task.retry_count += 1
                
                if task.retry_count < task.max_retries:
                    task.next_execution = datetime.now() + timedelta(seconds=60)
                    task.status = TaskStatus.PENDING
    
    async def _cancel_all_tasks(self):
        """Cancela todas as tarefas ativas"""
        for task in self.tasks.values():
            if task.status in [TaskStatus.PENDING, TaskStatus.RUNNING]:
                task.status = TaskStatus.CANCELLED
        
        logger.info("Todas as tarefas canceladas")
    
    async def _notify_status_change(self):
        """Notifica mudança de status para callbacks"""
        for callback in self.status_callbacks:
            try:
                await callback(self.status, self.statistics)
            except Exception as e:
                logger.error(f"Erro em callback de status: {e}")
    
    async def _notify_task_completion(self, task: ScheduledTask):
        """Notifica conclusão de tarefa para callbacks"""
        for callback in self.task_callbacks:
            try:
                await callback(task)
            except Exception as e:
                logger.error(f"Erro em callback de tarefa: {e}")
    
    def add_status_callback(self, callback: Callable):
        """Adiciona callback para mudanças de status"""
        self.status_callbacks.append(callback)
    
    def add_task_callback(self, callback: Callable):
        """Adiciona callback para conclusão de tarefas"""
        self.task_callbacks.append(callback)
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual do bot"""
        return {
            'status': self.status.value,
            'is_running': self.is_running,
            'statistics': self.statistics.to_dict(),
            'active_tasks': len([t for t in self.tasks.values() if t.status != TaskStatus.CANCELLED]),
            'config': {
                'num_tabs': self.num_tabs,
                'execution_speed': self.execution_speed,
                'retry_attempts': self.retry_attempts
            }
        }
    
    def get_tasks_status(self) -> List[Dict[str, Any]]:
        """Retorna status de todas as tarefas"""
        return [task.to_dict() for task in self.tasks.values()]
    
    def get_tabs_status(self) -> List[Dict[str, Any]]:
        """Retorna status de todas as guias"""
        return self.browser_manager.get_all_tabs_info()


# Função utilitária para criar instância do agendador
def create_bot_scheduler(browser_manager, automation_engine, config_manager, proxy_manager=None) -> BotScheduler:
    """
    Cria instância do agendador do bot
    
    Args:
        browser_manager: Gerenciador de navegador
        automation_engine: Engine de automação
        config_manager: Gerenciador de configurações
        
    Returns:
        Instância do agendador
    """
    return BotScheduler(browser_manager, automation_engine, config_manager, proxy_manager)
