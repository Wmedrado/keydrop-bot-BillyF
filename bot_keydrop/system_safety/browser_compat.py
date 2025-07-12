"""Utilities to verify browser and driver compatibility."""

from __future__ import annotations
import re
import subprocess
from pathlib import Path


def _get_version(cmd: list[str]) -> str:
    try:
        out = subprocess.check_output(cmd, text=True)
    except Exception:
        return "0"
    match = re.search(r"(\d+\.\d+\.\d+\.\d+|\d+\.\d+)", out)
    return match.group(1) if match else "0"


def browser_driver_compatible(browser_path: Path, driver_path: Path) -> bool:
    """Return True if major versions match."""
    b_ver = _get_version([str(browser_path), "--version"])
    d_ver = _get_version([str(driver_path), "--version"])
    b_major = b_ver.split(".")[0]
    d_major = d_ver.split(".")[0]
    return b_major == d_major and b_major != "0"
