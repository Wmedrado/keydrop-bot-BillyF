from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class SessionRecord:
    """Basic information recorded for each bot session."""

    start_time: str
    end_time: str
    bot_id: str = "default"
    profit: float = 0.0
    participations: int = 0
    successes: int = 0
    failures: int = 0
    active_time: float = 0.0  # seconds
    initial_balance: Optional[float] = None


class PerformanceHistory:
    """Manage historical performance stats stored in JSON files."""

    def __init__(self, profile_id: str, base_dir: str = "logs/performance_stats"):
        self.profile_id = str(profile_id)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _file_path(self, day: date) -> Path:
        return self.base_dir / f"{self.profile_id}_{day.isoformat()}.json"

    def record_session(self, record: SessionRecord, day: Optional[date] = None) -> None:
        day = day or date.fromisoformat(record.start_time.split("T")[0])
        path = self._file_path(day)
        data: List[Dict[str, Any]] = []
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                data = []
        data.append(asdict(record))
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def load_history(self, start: date, end: date) -> List[Dict[str, Any]]:
        current = start
        records: List[Dict[str, Any]] = []
        while current <= end:
            path = self._file_path(current)
            if path.exists():
                try:
                    records.extend(json.loads(path.read_text(encoding="utf-8")))
                except Exception:
                    pass
            current += timedelta(days=1)
        return records

    def summarize(self, start: date, end: date) -> Dict[str, Any]:
        sessions = self.load_history(start, end)
        total_profit = sum(s.get("profit", 0) for s in sessions)
        total_participations = sum(s.get("participations", 0) for s in sessions)
        total_successes = sum(s.get("successes", 0) for s in sessions)
        total_failures = sum(s.get("failures", 0) for s in sessions)
        total_active_time = sum(s.get("active_time", 0) for s in sessions)
        num_days = (end - start).days + 1
        average_daily_profit = total_profit / num_days if num_days else 0
        initial_balance = None
        for s in sessions:
            if s.get("initial_balance") is not None:
                initial_balance = s["initial_balance"]
                break
        roi = None
        if initial_balance is not None and initial_balance > 0:
            roi = ((initial_balance + total_profit) - initial_balance) / initial_balance * 100
        return {
            "total_profit": total_profit,
            "average_daily_profit": average_daily_profit,
            "total_participations": total_participations,
            "total_successes": total_successes,
            "total_failures": total_failures,
            "total_active_time": total_active_time,
            "roi": roi,
            "num_days": num_days,
        }
