"""
Inicializador do módulo de lógica do bot
"""

from .browser_manager import BrowserManager, TabInfo, browser_manager
from .automation_tasks import KeydropAutomation, ParticipationResult, ParticipationAttempt, create_keydrop_automation
from .scheduler import BotScheduler, BotStatus, TaskStatus, ScheduledTask, BotStatistics, create_bot_scheduler

__all__ = [
    'BrowserManager', 'TabInfo', 'browser_manager',
    'KeydropAutomation', 'ParticipationResult', 'ParticipationAttempt', 'create_keydrop_automation',
    'BotScheduler', 'BotStatus', 'TaskStatus', 'ScheduledTask', 'BotStatistics', 'create_bot_scheduler'
]
