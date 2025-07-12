import sys
from pathlib import Path
import unittest
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.backend.bot_logic.automation_tasks import (
    KeydropAutomation,
    ParticipationAttempt,
    ParticipationResult
)


class DummyBrowserManager:
    def get_tab_info(self, tab_id):
        class Info:
            page = True
        return Info()


def make_attempt(tab_id, result):
    return ParticipationAttempt(
        tab_id=tab_id,
        attempt_number=1,
        timestamp=datetime.now(),
        result=result
    )


class FakeElement:
    def __init__(self, text=None, amateur=False):
        self._text = text
        self._amateur = amateur

    async def query_selector(self, selector):
        from bot_keydrop.backend.bot_logic.automation_tasks import KeydropAutomation
        if selector == KeydropAutomation.SELECTORS['lottery_title']:
            return FakeElement(self._text)
        if selector == KeydropAutomation.SELECTORS['amateur_lottery'] and self._amateur:
            return FakeElement()
        return None

    async def inner_text(self):
        return self._text


class TestKeydropAutomation(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.auto = KeydropAutomation(DummyBrowserManager())

    async def test_add_history_and_stats(self):
        self.auto._add_to_history(make_attempt(1, ParticipationResult.SUCCESS))
        self.auto._add_to_history(make_attempt(1, ParticipationResult.FAILED))
        stats = self.auto.get_participation_stats(hours=1)
        self.assertEqual(stats['total_attempts'], 2)
        self.assertEqual(stats['successful_participations'], 1)
        self.assertEqual(stats['failed_participations'], 1)

    async def test_record_and_get_winnings(self):
        self.auto.record_winning(10.0, 'amateur')
        self.auto.record_winning(5.0, 'pro')
        all_wins = self.auto.get_winnings_history()
        self.assertEqual(len(all_wins), 2)
        latest = self.auto.get_winnings_history(limit=1)
        self.assertEqual(len(latest), 1)
        self.assertEqual(latest[0]['amount'], 5.0)

    async def test_extract_lottery_info(self):
        card = FakeElement('Amateur Test', amateur=True)
        info = await self.auto._extract_lottery_info(card)
        self.assertEqual(info['title'], 'Amateur Test')
        self.assertTrue(info['is_amateur'])
        self.assertEqual(info['type'], 'amateur')


if __name__ == '__main__':
    unittest.main()
