import csv
import json
import logging
from datetime import datetime, date, timedelta, time
from pathlib import Path
from typing import Optional

from ..bot_logic.automation_tasks import ParticipationResult

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)
logger = logging.getLogger(__name__)


def export_daily_summary(automation_engine, target_date: Optional[date] = None, as_json: bool = False) -> Path:
    """Export participation summary for a given date."""
    if automation_engine is None:
        raise ValueError("Automation engine not initialized")

    target_date = target_date or date.today()
    attempts = [
        a for a in automation_engine.participation_history
        if a.timestamp.date() == target_date
    ]
    total = len(attempts)
    success = len([a for a in attempts if a.result == ParticipationResult.SUCCESS])
    failed = len([a for a in attempts if a.result == ParticipationResult.FAILED])

    data = {
        "date": target_date.isoformat(),
        "total_attempts": total,
        "successful": success,
        "failed": failed,
    }

    if as_json:
        file_path = EXPORT_DIR / f"report_{target_date}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        file_path = EXPORT_DIR / f"report_{target_date}.csv"
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)

    logger.info(f"Resumo diário exportado para {file_path}")
    return file_path


def start_daily_export_task(automation_engine, as_json: bool = False):
    """Start a background task to export a daily summary."""
    async def _loop():
        # export summary for yesterday at startup
        try:
            export_daily_summary(automation_engine, date.today() - timedelta(days=1), as_json)
        except Exception:
            pass
        while True:
            now = datetime.now()
            next_run = datetime.combine(now.date() + timedelta(days=1), time.min)
            await asyncio.sleep((next_run - now).total_seconds())
            try:
                export_daily_summary(automation_engine, now.date(), as_json)
            except Exception as e:
                logger.error(f"Erro ao exportar resumo diário: {e}")

    import asyncio
    return asyncio.create_task(_loop())
