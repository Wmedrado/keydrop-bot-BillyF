import sys
import tempfile
import asyncio
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.backend.config.config_manager import ConfigManager
from bot_keydrop.backend.bot_logic.scheduler import BotScheduler, BotStatus
from bot_keydrop.backend.bot_logic.automation_tasks import ParticipationAttempt, ParticipationResult


class DummyTabInfo:
    def __init__(self, tab_id):
        from datetime import datetime
        self.tab_id = tab_id
        self.page = True
        self.status = 'ready'
        self.last_activity = datetime.now()
        self.error_count = 0
        self.participation_count = 0


class DummyBrowserManager:
    def __init__(self):
        self.is_running = False
        self.tabs = {}

    async def start_browser(self, headless=False, mini_window=False, user_data_dir=None):
        self.is_running = True
        return True

    async def stop_browser(self):
        self.is_running = False
        return True

    async def create_tab(self, tab_id, proxy=None):
        info = DummyTabInfo(tab_id)
        self.tabs[tab_id] = info
        return info

    async def restart_tab(self, tab_id):
        return True

    async def clear_cache(self, preserve_login=True):
        return True

    async def emergency_stop(self):
        self.is_running = False

    def get_tab_info(self, tab_id):
        return self.tabs.get(tab_id)

    def get_tab_count(self):
        return len(self.tabs)

    def is_tab_ready(self, tab_id):
        return True

    def get_all_tabs_info(self):
        return [tab.__dict__ for tab in self.tabs.values()]


class DummyAutomation:
    async def navigate_to_lotteries(self, tab_id):
        return True

    async def participate_in_lottery(self, tab_id, max_retries=1):
        from datetime import datetime
        return ParticipationAttempt(
            tab_id=tab_id,
            attempt_number=1,
            timestamp=datetime.now(),
            result=ParticipationResult.SUCCESS
        )

    async def setup_login_tabs(self):
        return False, []


class TestBotScheduler(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.config = ConfigManager(config_dir=self.tmp.name)
        self.config.update_config(num_tabs=1, amateur_lottery_wait_time=60, execution_speed=10)
        self.browser = DummyBrowserManager()
        self.automation = DummyAutomation()
        self.scheduler = BotScheduler(self.browser, self.automation, self.config)

    async def asyncTearDown(self):
        await self.scheduler.stop_bot()
        self.tmp.cleanup()

    async def test_start_and_stop(self):
        started = await self.scheduler.start_bot()
        self.assertTrue(started)
        self.assertEqual(self.scheduler.status, BotStatus.RUNNING)
        self.assertTrue(self.browser.is_running)
        self.assertEqual(len(self.scheduler.tasks), self.config.get_config().num_tabs)

        await asyncio.sleep(0.1)

        stopped = await self.scheduler.stop_bot()
        self.assertTrue(stopped)
        self.assertEqual(self.scheduler.status, BotStatus.STOPPED)
        self.assertFalse(self.browser.is_running)


if __name__ == '__main__':
    unittest.main()
