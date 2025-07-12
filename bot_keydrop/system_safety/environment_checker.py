import os
import platform
import socket
import sys
from pathlib import Path
import psutil


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
    """Ensure key files are present."""
    required = [Path("firebase_credentials.json"), Path("bot_config.json"), Path("user_session.json")]
    return all(p.exists() for p in required)


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

