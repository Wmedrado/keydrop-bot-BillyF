"""Track last executed line before a crash."""
from __future__ import annotations
import traceback
from pathlib import Path

LOG_FILE = Path('logs/last_crash.log')


def log_last_line(exc: Exception) -> None:
    """Record the last stack frame from the exception to LOG_FILE."""
    stack = traceback.extract_tb(exc.__traceback__)
    if not stack:
        return
    frame = stack[-1]
    LOG_FILE.parent.mkdir(exist_ok=True)
    LOG_FILE.write_text(f"{frame.filename}:{frame.lineno}:{frame.name}", encoding='utf-8')
