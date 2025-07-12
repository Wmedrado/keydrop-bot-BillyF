import os
import sys
import types
from datetime import datetime, timedelta
from unittest.mock import AsyncMock

import pytest

# Ensure project root is on sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Provide dummy Playwright modules to satisfy imports
async_api = types.ModuleType("playwright.async_api")
async_api.async_playwright = AsyncMock()
async_api.Browser = object
async_api.BrowserContext = object
async_api.Page = object
async_api.Playwright = object
sys.modules.setdefault("playwright", types.ModuleType("playwright"))
sys.modules.setdefault("playwright.async_api", async_api)

from bot_keydrop.backend.bot_logic.automation_tasks import (
    KeydropAutomation,
    ParticipationAttempt,
    ParticipationResult,
)
from bot_keydrop.backend.bot_logic.scheduler import (
    BotScheduler,
    ScheduledTask,
    TaskStatus,
)
from bot_keydrop.backend.config.config_manager import BotConfig


@pytest.mark.asyncio
async def test_participate_in_lottery_success(mocker):
    browser_manager = mocker.Mock()
    page = mocker.Mock()
    page.goto = AsyncMock()
    tab_info = types.SimpleNamespace(
        page=page,
        status='ready',
        last_activity=datetime.now(),
        error_count=0,
        participation_count=0,
    )
    browser_manager.get_tab_info.return_value = tab_info

    automation = KeydropAutomation(browser_manager)

    mocker.patch.object(automation, '_check_login_required', AsyncMock(return_value=False))
    mocker.patch.object(automation, '_find_available_lotteries', AsyncMock(return_value=['lottery']))
    expected = ParticipationAttempt(tab_id=1, attempt_number=1, timestamp=datetime.now(), result=ParticipationResult.SUCCESS)
    mocker.patch.object(automation, '_try_participation_methods', AsyncMock(return_value=expected))
    add_history = mocker.patch.object(automation, '_add_to_history')

    result = await automation.participate_in_lottery(1, max_retries=1)

    assert result.result == ParticipationResult.SUCCESS
    add_history.assert_called_once_with(expected)


@pytest.mark.asyncio
async def test_participate_in_lottery_button_failure(mocker):
    browser_manager = mocker.Mock()
    page = mocker.Mock()
    page.goto = AsyncMock()
    tab_info = types.SimpleNamespace(
        page=page,
        status='ready',
        last_activity=datetime.now(),
        error_count=0,
        participation_count=0,
    )
    browser_manager.get_tab_info.return_value = tab_info

    automation = KeydropAutomation(browser_manager)

    mocker.patch.object(automation, '_check_login_required', AsyncMock(return_value=False))
    mocker.patch.object(automation, '_find_available_lotteries', AsyncMock(return_value=[]))
    add_history = mocker.patch.object(automation, '_add_to_history')

    result = await automation.participate_in_lottery(1, max_retries=1)

    assert result.result == ParticipationResult.BUTTON_NOT_FOUND
    add_history.assert_not_called()


@pytest.mark.asyncio
async def test_restart_tab_recreates_tasks(mocker):
    browser_manager = mocker.Mock()
    browser_manager.restart_tab = AsyncMock(return_value=True)

    config = BotConfig()
    config_manager = mocker.Mock()
    config_manager.get_config.return_value = config

    automation_engine = mocker.Mock()
    scheduler = BotScheduler(browser_manager, automation_engine, config_manager)

    task = ScheduledTask(
        task_id='participate_1',
        tab_id=1,
        task_type='participate',
        next_execution=datetime.now(),
        interval=timedelta(seconds=60)
    )
    scheduler.tasks[task.task_id] = task

    create_tasks = mocker.patch.object(scheduler, '_create_tasks_for_tab', AsyncMock())

    result = await scheduler.restart_tab(1)

    assert result is True
    assert task.status == TaskStatus.CANCELLED
    browser_manager.restart_tab.assert_called_once_with(1)
    create_tasks.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_learn_participation(mocker):
    browser_manager = mocker.Mock()
    tab_info = mocker.Mock(page=mocker.Mock())
    browser_manager.get_tab_info.return_value = tab_info

    automation = KeydropAutomation(browser_manager)

    recorder = mocker.Mock()
    recorder.actions = [{"selector": "#mybutton"}]
    recorder.start = AsyncMock()
    recorder.stop = AsyncMock()
    mocker.patch('bot_keydrop.backend.learning.action_recorder.ActionRecorder', return_value=recorder)
    set_selector = mocker.patch.object(automation.learner, 'set_selector')
    mocker.patch('asyncio.sleep', AsyncMock())

    result = await automation.learn_participation(1, learn_time=0)

    assert result is True
    set_selector.assert_called_once_with('#mybutton')

