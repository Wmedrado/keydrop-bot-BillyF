"""Track last executed line before an unhandled exception."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Tuple

LAST_LINE: Tuple[str, int] = ("", 0)
_log_file: Path | None = None
_prev_hook = None

def _trace(frame, event, arg):
    global LAST_LINE
    if event == "line":
        LAST_LINE = (frame.f_code.co_name, frame.f_lineno)
    return _trace


def _hook(exc_type, exc, tb):
    if _log_file:
        with _log_file.open("a", encoding="utf-8") as fh:
            fh.write(f"{exc_type.__name__}: {exc} at {LAST_LINE[0]}:{LAST_LINE[1]}\n")
    if _prev_hook:
        _prev_hook(exc_type, exc, tb)


def start_crash_tracker(log_file: Path = Path("logs/crash.log")) -> None:
    """Enable crash tracking globally."""
    global _log_file, _prev_hook
    _log_file = log_file
    log_file.parent.mkdir(exist_ok=True)
    _prev_hook = sys.excepthook
    sys.settrace(_trace)
    sys.excepthook = _hook


def log_exception(exc: Exception) -> None:
    """Log *exc* using the last recorded line."""
    func, line = LAST_LINE
    if exc.__traceback__:
        tb = exc.__traceback__
        while tb.tb_next:
            tb = tb.tb_next
        func = tb.tb_frame.f_code.co_name
        line = tb.tb_lineno
    if _log_file:
        with _log_file.open("a", encoding="utf-8") as fh:
            fh.write(f"{type(exc).__name__}: {exc} at {func}:{line}\n")

