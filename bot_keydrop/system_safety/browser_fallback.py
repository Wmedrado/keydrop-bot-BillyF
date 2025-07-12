"""Launch browsers with fallback strategy."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable

from .dependency_validator import BROWSER_PATHS


def launch_browser_with_fallback(primary: str | None = None, extra: Iterable[str] | None = None) -> str | None:
    """Try launching *primary* or fallbacks. Return path used or ``None``."""
    paths = []
    if primary:
        paths.append(primary)
    paths.extend(extra or [])
    paths.extend(BROWSER_PATHS)
    for path in paths:
        if not path:
            continue
        if Path(path).exists():
            try:
                subprocess.Popen([path])
                return path
            except Exception:
                continue
    return None
