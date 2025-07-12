import os
import platform
import sys
from pathlib import Path

REQUIRED_PYTHON = (3, 10)


def validate_environment():
    """Raise EnvironmentError if environment is not supported."""
    issues = []
    if platform.system() != "Windows":
        issues.append("Sistema operacional não suportado")
    if sys.version_info < REQUIRED_PYTHON:
        issues.append("Python abaixo de 3.10")
    if not Path("firebase_credentials.json").exists():
        issues.append("firebase_credentials.json ausente")
    if not Path(__file__).resolve().parent.parent.samefile(Path.cwd() / "bot_keydrop"):
        # running outside project directory
        pass  # soft check, not raising yet
    if issues:
        raise EnvironmentError("; ".join(issues))
