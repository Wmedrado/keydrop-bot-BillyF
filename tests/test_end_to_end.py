import sys
import asyncio
import tempfile
from datetime import datetime
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.backend.config.config_manager import ConfigManager
from bot_keydrop.backend.bot_logic.scheduler import BotScheduler, BotStatus
from bot_keydrop.backend.bot_logic.automation_tasks import KeydropAutomation, ParticipationAttempt, ParticipationResult


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
        class TabInfo:
            """Simple object tracking a tab used in tests."""

            def __init__(self, tab_id):
                self.tab_id = tab_id
                self.page = True
                self.status = 'ready'
                self.last_activity = datetime.now()
                self.participation_count = 0
                self.error_count = 0

        info = TabInfo(tab_id)
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


def make_success_attempt(tab_id):
    return ParticipationAttempt(
        tab_id=tab_id,
        attempt_number=1,
        timestamp=datetime.now(),
        result=ParticipationResult.SUCCESS
    )


class EndToEndTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.config = ConfigManager(config_dir=self.tmp.name)
        self.config.update_config(num_tabs=1, execution_speed=10, amateur_lottery_wait_time=60)
        self.browser = DummyBrowserManager()
        self.automation = KeydropAutomation(self.browser)

        async def fake_nav(tab_id):
            return True

        async def fake_participate(tab_id, max_retries=1):
            attempt = make_success_attempt(tab_id)
            self.automation._add_to_history(attempt)
            return attempt

        async def fake_setup():
            return False, []

        self.automation.navigate_to_lotteries = fake_nav
        self.automation.participate_in_lottery = fake_participate
        self.automation.setup_login_tabs = fake_setup

        self.scheduler = BotScheduler(self.browser, self.automation, self.config)

    async def asyncTearDown(self):
        await self.scheduler.stop_bot()
        self.tmp.cleanup()

    async def test_full_flow(self):
        self.assertTrue(await self.scheduler.start_bot())
        await asyncio.sleep(0.2)
        await self.scheduler.stop_bot()
        self.assertEqual(self.scheduler.status, BotStatus.STOPPED)
        history = self.automation.get_participation_history()
        self.assertTrue(len(history) >= 1)
        self.assertEqual(self.scheduler.statistics.successful_tasks, 1)


if __name__ == '__main__':
    unittest.main()
