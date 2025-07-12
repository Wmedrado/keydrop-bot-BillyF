import importlib.util
import logging
import os
from pathlib import Path
from tkinter import messagebox

from .environment_checker import verificar_conexao_internet

logger = logging.getLogger(__name__)

REQUIRED_LIBS = [
    "selenium",
    "pyautogui",
    "opencv_python",
    "requests",
    "psutil",
]

WEBDRIVER_FILES = [
    "chromedriver.exe",
    "msedgedriver.exe",
    "geckodriver.exe",
]

BROWSER_PATHS = [
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"),
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\Application\\msedge.exe"),
]

REQUIRED_DIRS = ["profiles", "logs"]


def _check_libs():
    missing = []
    for lib in REQUIRED_LIBS:
        if importlib.util.find_spec(lib) is None:
            missing.append(lib)
    return missing


def _check_webdriver():
    for name in WEBDRIVER_FILES:
        if Path(name).exists():
            return True
    return False


def _check_browsers() -> str | None:
    """Return first available browser executable or ``None``."""
    for path in BROWSER_PATHS:
        if os.path.exists(path):
            return path
    return None


def _check_dirs():
    missing = []
    for d in REQUIRED_DIRS:
        if not Path(d).exists():
            missing.append(d)
    return missing


def run_dependency_check():
    """Validate environment dependencies before starting the bot."""
    issues = []
    libs_missing = _check_libs()
    if libs_missing:
        issues.append("Bibliotecas ausentes: " + ", ".join(libs_missing))
    if not _check_webdriver():
        issues.append("WebDriver nao encontrado")
    browser = _check_browsers()
    if not browser:
        issues.append("Navegador compativel nao encontrado")
    dirs_missing = _check_dirs()
    if dirs_missing:
        issues.append("Pastas faltando: " + ", ".join(dirs_missing))
    if not verificar_conexao_internet():
        issues.append("Sem conexao com a internet")

    if issues:
        msg = "\n".join(issues)
        logger.warning("Problemas detectados:\n%s", msg)
        try:
            messagebox.showwarning("Dependencias", msg)
        except Exception:
            pass
        return False
    if browser:
        logger.info("Navegador detectado: %s", browser)
    return True


def get_available_browser() -> str | None:
    """Return path to available browser, trying fallbacks."""
    return _check_browsers()
