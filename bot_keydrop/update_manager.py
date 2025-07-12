#!/usr/bin/env python3
"""Gerenciador de atualiza\xc3\xa7\xc3\xb5es do Keydrop Bot Professional.

O script verifica um JSON remoto com informa\xc3\xa7\xc3\xb5es de vers\xc3\xa3o e download.
Se a vers\xc3\xa3o local estiver desatualizada, baixa o pacote (ZIP ou EXE)
e reinicia o programa automaticamente.
"""

from __future__ import annotations

import os
import sys
import tempfile
import subprocess
import zipfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

import requests

# URL do arquivo JSON contendo informa\xc3\xa7\xc3\xb5es da \xc3\xbaltima vers\xc3\xa3o
UPDATE_INFO_URL = "https://example.com/update_info.json"

# Vers\xc3\xa3o atual do bot lida do arquivo VERSION
VERSION_FILE = Path(__file__).resolve().parents[1] / "VERSION"
if VERSION_FILE.exists():
    CURRENT_VERSION = VERSION_FILE.read_text().strip()
else:
    CURRENT_VERSION = "0.0.0"


def _parse_version(version: str) -> Tuple[int, ...]:
    """Converter string de vers\u00e3o em tupla compar\u00e1vel."""
    if not version:
        raise ValueError("Vers\u00e3o vazia")
    try:
        return tuple(int(part) for part in version.split("."))
    except ValueError as exc:  # Not numeric
        raise ValueError(f"Vers\u00e3o inv\u00e1lida: {version}") from exc


def fetch_update_info(url: str = UPDATE_INFO_URL) -> Optional[Dict[str, Any]]:
    """Baixar informa\u00e7\u00f5es de atualiza\u00e7\u00e3o do servidor."""
    if not url:
        raise ValueError("URL de atualiza\u00e7\u00e3o n\u00e3o informada")
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        print(
            f"\u26a0\ufe0f Falha ao obter informa\u00e7\u00f5es de atualiza\u00e7\u00e3o: {exc}"
        )
        return None


def download_file(url: str, destination: Path) -> None:
    """Realizar download do arquivo indicado para o caminho destino."""
    if not url:
        raise ValueError("URL de download vazia")
    if destination is None:
        raise ValueError("Caminho de destino n\u00e3o pode ser None")
    with requests.get(url, stream=True, timeout=10) as r:
        r.raise_for_status()
        with open(destination, "wb") as f:
            shutil.copyfileobj(r.raw, f)


def apply_update(package_path: Path) -> None:
    """Aplicar pacote de atualiza\u00e7\u00e3o (.zip ou .exe)."""
    if not package_path.exists():
        raise FileNotFoundError(str(package_path))
    if package_path.suffix == ".zip":
        with zipfile.ZipFile(package_path, "r") as zf:
            zf.extractall(package_path.parent)
    elif package_path.suffix == ".exe" and os.name == "nt":
        subprocess.Popen([str(package_path)])
    else:
        raise RuntimeError("Formato de pacote n\u00e3o suportado")


def check_for_update() -> None:
    """Verificar se h\u00e1 nova vers\u00e3o e aplicar se necess\u00e1rio."""
    info = fetch_update_info()
    if not info:
        return

    remote_version = info.get("version")
    download_url = info.get("download_url")
    if not remote_version or not download_url:
        print("❌ JSON de atualiza\xc3\xa7\xc3\xa3o inv\xc3\xa1lido")
        return

    if _parse_version(remote_version) <= _parse_version(CURRENT_VERSION):
        print("✅ Nenhuma atualiza\xc3\xa7\xc3\xa3o dispon\xc3\xadvel")
        return

    print(f"🔄 Atualiza\xc3\xa7\xc3\xa3o encontrada: {remote_version}")
    temp_dir = Path(tempfile.gettempdir())
    package_name = Path(download_url).name
    package_path = temp_dir / package_name

    try:
        print("⬇️  Baixando pacote de atualiza\xc3\xa7\xc3\xa3o...")
        download_file(download_url, package_path)
        print("✅ Download conclu\xc3\xaddo")
        apply_update(package_path)
        print("🚀 Atualiza\xc3\xa7\xc3\xa3o aplicada. Reiniciando...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as exc:
        print(f"❌ Falha ao aplicar atualiza\xc3\xa7\xc3\xa3o: {exc}")


if __name__ == "__main__":
    check_for_update()
