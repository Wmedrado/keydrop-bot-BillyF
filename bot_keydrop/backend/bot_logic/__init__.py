"""
Inicializador do módulo de lógica do bot
"""

from .browser_manager import BrowserManager, TabInfo, browser_manager
from .macro_recorder import MacroRecorder
from .automation_tasks import KeydropAutomation, ParticipationResult, ParticipationAttempt, create_keydrop_automation
from .scheduler import BotScheduler, BotStatus, TaskStatus, ScheduledTask, BotStatistics, create_bot_scheduler
from .tab_watchdog import TabWatchdog

__all__ = [
    'BrowserManager', 'TabInfo', 'browser_manager',
    'KeydropAutomation', 'ParticipationResult', 'ParticipationAttempt', 'create_keydrop_automation',
    'BotScheduler', 'BotStatus', 'TaskStatus', 'ScheduledTask', 'BotStatistics', 'create_bot_scheduler',
    'TabWatchdog', 'MacroRecorder'
]
