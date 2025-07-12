"""Simple execution history recorder."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def record_history(profile: str, message: str, logs_dir: str | Path = "logs") -> None:
    """Append *message* to the history log for *profile*."""
    path = Path(logs_dir) / f"{profile}_history.log"
    path.parent.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"{ts} | {message}\n")
