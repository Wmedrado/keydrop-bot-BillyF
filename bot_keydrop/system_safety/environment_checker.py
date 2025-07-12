import os
import platform
import socket
import sys
import logging
from pathlib import Path
from tkinter import messagebox
import psutil

logger = logging.getLogger(__name__)


def verificar_conexao_internet(timeout: float = 3.0) -> bool:
    """Check basic internet connectivity."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        return False


def ambiente_compativel() -> bool:
    """Validate OS and Python version requirements."""
    if platform.system() != "Windows":
        return False
    if sys.version_info < (3, 10):
        return False
    return True


def verificar_arquivos_obrigatorios() -> bool:
    """Ensure key files are present and warn the user if not."""
    required = [
        Path("firebase_credentials.json"),
        Path("config.json"),
        Path("release_info.json"),
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        msg = "Os seguintes arquivos estao faltando:\n" + "\n".join(missing)
        try:
            messagebox.showerror("Arquivos Ausentes", msg)
        except Exception:
            pass
        logger.error(msg)
        return False
    return True


class LockFile:
    """Simple lockfile mechanism to avoid multiple instances."""
    def __init__(self, path: Path = Path("temp/keydrop.lock")):
        self.path = path
        self.path.parent.mkdir(exist_ok=True)

    def acquire(self) -> bool:
        if self.path.exists():
            try:
                pid = int(self.path.read_text())
                if pid and pid != os.getpid() and pid in [p.pid for p in psutil.process_iter()]:
                    return False
            except Exception:
                return False
        self.path.write_text(str(os.getpid()))
        return True

    def release(self) -> None:
        if self.path.exists():
            try:
                self.path.unlink()
            except Exception:
                pass


def executando_no_diretorio_correto(expected: list[str] | None = None) -> bool:
    """Check if the application is running from its original directory."""
    expected = expected or ["launcher.py", "bot_keydrop", "config.json"]
    return all(Path(item).exists() for item in expected)

