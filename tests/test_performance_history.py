import tempfile
from datetime import date, timedelta

from bot_keydrop.backend.tools import PerformanceHistory, SessionRecord


def test_record_and_summarize():
    with tempfile.TemporaryDirectory() as tmp:
        history = PerformanceHistory("test", base_dir=tmp)
        today = date.today()
        record1 = SessionRecord(
            start_time=f"{today.isoformat()}T00:00:00",
            end_time=f"{today.isoformat()}T01:00:00",
            profit=10.0,
            participations=5,
            successes=4,
            failures=1,
            active_time=3600,
            bot_id="A",
            initial_balance=100.0,
        )
        history.record_session(record1)
        next_day = today + timedelta(days=1)
        record2 = SessionRecord(
            start_time=f"{next_day.isoformat()}T00:00:00",
            end_time=f"{next_day.isoformat()}T01:00:00",
            profit=5.0,
            participations=3,
            successes=2,
            failures=1,
            active_time=1800,
            bot_id="A",
        )
        history.record_session(record2, day=next_day)

        summary = history.summarize(today, next_day)
        assert summary["total_profit"] == 15.0
        assert summary["total_participations"] == 8
        assert summary["total_successes"] == 6
        assert summary["total_failures"] == 2
        assert summary["roi"] == 15.0
