"""Stability utilities for recovery and monitoring."""
from __future__ import annotations

import asyncio
import json
import platform
import threading
import time
from pathlib import Path
from typing import Callable, Any, List

import psutil

from datetime import datetime
from ..backend.discord_integration import send_discord_notification


# ---------------------------------------------------------------------------
# Automatic retry wrapper
# ---------------------------------------------------------------------------

def auto_retry(
    max_attempts: int = 3, delay: float = 0.5
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorate a callable to automatically retry on failure."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if asyncio.iscoroutinefunction(func):

            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                attempts = 0
                while attempts < max_attempts:
                    try:
                        return await func(*args, **kwargs)
                    except Exception:  # pragma: no cover - re-raise last
                        attempts += 1
                        if attempts >= max_attempts:
                            raise
                        await asyncio.sleep(delay)

            return async_wrapper

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception:  # pragma: no cover - re-raise last
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# Simple watchdog to restart when a check fails repeatedly
# ---------------------------------------------------------------------------

class BotWatchdog(threading.Thread):
    """Monitor a bot using callbacks to check liveness and restart."""

    def __init__(
        self,
        is_alive: Callable[[], bool],
        restart_cb: Callable[[], None],
        interval: float = 30.0,
        timeout: float = 120.0,
    ) -> None:
        super().__init__(daemon=True)
        self.is_alive = is_alive
        self.restart_cb = restart_cb
        self.interval = interval
        self.timeout = timeout
        self._running = False

    def run(self) -> None:  # pragma: no cover - timing dependent
        self._running = True
        last_ok = time.time()
        while self._running:
            time.sleep(self.interval)
            if self.is_alive():
                last_ok = time.time()
                continue
            if time.time() - last_ok > self.timeout:
                try:
                    self.restart_cb()
                finally:
                    last_ok = time.time()

    def stop(self) -> None:
        self._running = False


# ---------------------------------------------------------------------------
# Configuration backup and environment snapshot
# ---------------------------------------------------------------------------

def backup_config(
    profile: str = "default", config_path: Path | None = None
) -> Path:
    """Backup the config.json file for the given profile."""
    cfg = config_path or Path("config.json")
    dest_dir = cfg.parent / "backups"
    dest_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    dest = dest_dir / f"{cfg.stem}_{timestamp}{cfg.suffix}"
    dest.write_bytes(cfg.read_bytes())
    return dest


def snapshot_environment(path: Path) -> None:
    """Save a basic snapshot of system information and bot state."""
    data = {
        "os": platform.platform(),
        "python": platform.python_version(),
        "timestamp": int(time.time()),
        "version": Path("VERSION").read_text(encoding="utf-8").strip()
        if Path("VERSION").exists()
        else "unknown",
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Crash counter and rollback flag
# ---------------------------------------------------------------------------

def check_crash_and_mark(version: str, state_file: Path) -> bool:
    """Increment crash count and mark version for rollback if repeated."""
    state: dict[str, int] = {}
    if state_file.exists():
        state = json.loads(state_file.read_text(encoding="utf-8"))
    count = state.get(version, 0) + 1
    state[version] = count
    state_file.write_text(json.dumps(state), encoding="utf-8")
    if count >= 2:
        Path("rollback.flag").write_text(version, encoding="utf-8")
        return True
    return False


# ---------------------------------------------------------------------------
# Basic anomaly detection
# ---------------------------------------------------------------------------

def detect_anomalies(metrics: List[dict]) -> List[str]:
    """Return list of anomaly descriptions from a list of metric dicts."""
    alerts: List[str] = []
    for m in metrics:
        if m.get("cpu_percent", 0) > 90:
            alerts.append("CPU acima de 90%")
        if m.get("memory_percent", 0) > 90:
            alerts.append("Uso de RAM acima de 90%")
    return alerts


# ---------------------------------------------------------------------------
# Memory leak detection
# ---------------------------------------------------------------------------

def detect_memory_leak(usages: List[float], threshold: int = 3) -> bool:
    """Return True if memory usage keeps growing for `threshold` samples."""
    if len(usages) < threshold:
        return False
    last = usages[-threshold:]
    return all(x < y for x, y in zip(last, last[1:]))


# ---------------------------------------------------------------------------
# Utility to send logs to Discord
# ---------------------------------------------------------------------------

def send_log_to_discord(log_path: Path) -> None:
    if not log_path.exists():
        return
    content = log_path.read_text(encoding="utf-8")
    asyncio.run(send_discord_notification("📄 Logs", content[:1900], "system"))
