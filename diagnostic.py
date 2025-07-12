# -*- coding: utf-8 -*-
"""Simple environment diagnostic utility."""

from __future__ import annotations

import socket
import sys
from pathlib import Path
from typing import List

from bot_keydrop.system_safety.environment_checker import (
    verificar_conexao_internet,
    verificar_arquivos_obrigatorios,
)
from bot_keydrop.system_safety.dependency_validator import (
    get_available_browser,
    WEBDRIVER_FILES,
)

try:
    from colorama import Fore, Style, init as colorama_init
except Exception:  # pragma: no cover - optional dependency
    class _Dummy:
        def __getattr__(self, name):
            return ""

    Fore = Style = _Dummy()
    def colorama_init():
        pass

colorama_init()


CHECK_PORT = 8000
ESSENTIAL_FILES = ["config.json", ".env", "firebase_credentials.json"]


class DiagnosticResult:
    def __init__(self) -> None:
        self.errors: List[str] = []

    def ok(self, message: str) -> None:
        print(Fore.GREEN + "✔" + Style.RESET_ALL, message)

    def fail(self, message: str) -> None:
        self.errors.append(message)
        print(Fore.RED + "✖" + Style.RESET_ALL, message)

    @property
    def success(self) -> bool:
        return not self.errors


def _check_files(res: DiagnosticResult) -> None:
    missing = [f for f in ESSENTIAL_FILES if not Path(f).exists()]
    if missing:
        res.fail("Arquivos ausentes: " + ", ".join(missing))
    else:
        res.ok("Arquivos essenciais presentes")


def _check_port(res: DiagnosticResult, port: int = CHECK_PORT) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("127.0.0.1", port)) == 0:
            res.fail(f"Porta {port} em uso")
        else:
            res.ok(f"Porta {port} livre")


def _check_internet(res: DiagnosticResult) -> None:
    if verificar_conexao_internet():
        res.ok("Conexao com internet")
    else:
        res.fail("Sem conexao de internet")


def _check_browser_and_driver(res: DiagnosticResult) -> None:
    browser = get_available_browser()
    if browser:
        res.ok(f"Navegador detectado: {browser}")
    else:
        res.fail("Navegador Chrome/Edge nao encontrado")

    driver_found = any(Path(f).exists() for f in WEBDRIVER_FILES)
    if driver_found:
        res.ok("WebDriver presente")
    else:
        res.fail("WebDriver nao encontrado")


def run_diagnostic() -> bool:
    res = DiagnosticResult()
    print("=== Diagnostico do Sistema ===")
    _check_files(res)
    _check_port(res)
    _check_internet(res)
    _check_browser_and_driver(res)

    if not verificar_arquivos_obrigatorios():
        res.fail("Arquivos obrigatorios do projeto ausentes")

    if res.success:
        print(Fore.GREEN + "Tudo pronto para iniciar." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Problemas encontrados: {len(res.errors)}" + Style.RESET_ALL)
    return res.success


if __name__ == "__main__":
    success = run_diagnostic()
    sys.exit(0 if success else 1)
