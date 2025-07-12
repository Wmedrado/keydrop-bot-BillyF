from __future__ import annotations
from pathlib import Path
import json
import datetime

LOG_DIR = Path("logs")
REPORT_FILE = Path("fortnightly_report.json")


def collect_stats() -> dict:
    errors = 0
    profit = 0
    for log in LOG_DIR.glob("*.log"):
        text = log.read_text(errors="ignore")
        errors += text.lower().count("error")
    return {
        "date": datetime.date.today().isoformat(),
        "errors": errors,
        "profit": profit,
    }


def main() -> int:
    stats = collect_stats()
    data = []
    if REPORT_FILE.exists():
        data = json.loads(REPORT_FILE.read_text())
    data.append(stats)
    REPORT_FILE.write_text(json.dumps(data, indent=2))
    print("Fortnightly report updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
