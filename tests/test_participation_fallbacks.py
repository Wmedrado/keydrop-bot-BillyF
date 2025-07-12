import logging
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import types
from unittest.mock import AsyncMock
sys.modules.setdefault("psutil", types.ModuleType("psutil"))
async_api = types.ModuleType("playwright.async_api")
async_api.async_playwright = AsyncMock()
async_api.Browser = object
async_api.BrowserContext = object
async_api.Page = object
async_api.Playwright = object
sys.modules.setdefault("playwright", types.ModuleType("playwright"))
sys.modules.setdefault("playwright.async_api", async_api)

import pytest

from bot_keydrop.backend.bot_logic.automation_tasks import (
    KeydropAutomation,
    ParticipationAttempt,
    ParticipationResult,
)

@pytest.mark.asyncio
async def test_css_failure_falls_back_to_js(mocker, caplog):
    automation = KeydropAutomation(mocker.Mock())
    lottery = {'link': object(), 'info': {'type': 't', 'title': 't'}}

    css_attempt = ParticipationAttempt(1, 1, datetime.now(), ParticipationResult.FAILED)
    js_attempt = ParticipationAttempt(1, 1, datetime.now(), ParticipationResult.SUCCESS)

    mocker.patch.object(automation, '_attempt_participation', mocker.AsyncMock(return_value=css_attempt))
    mocker.patch.object(automation, '_attempt_participation_js', mocker.AsyncMock(return_value=js_attempt))
    image_mock = mocker.patch.object(automation, '_attempt_participation_image', mocker.AsyncMock())
    mocker.patch.object(automation.learner, 'best_method', return_value='css')

    caplog.set_level(logging.WARNING)
    result = await automation._try_participation_methods(mocker.Mock(), lottery, 1, 1)

    assert result.result == ParticipationResult.SUCCESS
    image_mock.assert_not_called()
    assert any('Método css falhou' in r.message for r in caplog.records)


@pytest.mark.asyncio
async def test_js_failure_falls_back_to_image(mocker, caplog):
    automation = KeydropAutomation(mocker.Mock())
    lottery = {'link': object(), 'info': {'type': 't', 'title': 't'}}

    css_attempt = ParticipationAttempt(1, 1, datetime.now(), ParticipationResult.FAILED)
    js_attempt = ParticipationAttempt(1, 1, datetime.now(), ParticipationResult.FAILED)
    image_attempt = ParticipationAttempt(1, 1, datetime.now(), ParticipationResult.SUCCESS)

    mocker.patch.object(automation, '_attempt_participation', mocker.AsyncMock(return_value=css_attempt))
    mocker.patch.object(automation, '_attempt_participation_js', mocker.AsyncMock(return_value=js_attempt))
    mocker.patch.object(automation, '_attempt_participation_image', mocker.AsyncMock(return_value=image_attempt))
    mocker.patch.object(automation.learner, 'best_method', return_value='css')

    caplog.set_level(logging.WARNING)
    result = await automation._try_participation_methods(mocker.Mock(), lottery, 1, 1)

    assert result.result == ParticipationResult.SUCCESS
    assert sum('Método css falhou' in r.message for r in caplog.records) == 1
    assert sum('Método js falhou' in r.message for r in caplog.records) == 1
