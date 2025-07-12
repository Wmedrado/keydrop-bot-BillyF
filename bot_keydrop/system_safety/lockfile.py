from pathlib import Path
import os
import psutil

LOCK_PATH = Path("temp/keydrop.lock")


def check_single_instance():
    """Create a lockfile to avoid multiple instances."""
    LOCK_PATH.parent.mkdir(exist_ok=True)
    if LOCK_PATH.exists():
        try:
            pid = int(LOCK_PATH.read_text())
            if psutil.pid_exists(pid):
                raise RuntimeError("O Keydrop Bot já está em execução!")
        except Exception:
            pass
    with open(LOCK_PATH, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))


def release_lock():
    if LOCK_PATH.exists():
        try:
            LOCK_PATH.unlink()
        except Exception:
            pass
