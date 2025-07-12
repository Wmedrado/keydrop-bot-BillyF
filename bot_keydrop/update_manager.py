#!/usr/bin/env python3
"""Gerenciador de atualiza\xc3\xa7\xc3\xb5es do Keydrop Bot Professional.

O script verifica um JSON remoto com informa\xc3\xa7\xc3\xb5es de vers\xc3\xa3o e download.
Se a vers\xc3\xa3o local estiver desatualizada, baixa o pacote (ZIP ou EXE)
e reinicia o programa automaticamente.
"""

import os
import sys
import tempfile
import subprocess
import zipfile
import shutil
from pathlib import Path

import requests

# URL do arquivo JSON contendo informa\xc3\xa7\xc3\xb5es da \xc3\xbaltima vers\xc3\xa3o
UPDATE_INFO_URL = "https://example.com/update_info.json"

# Vers\xc3\xa3o atual do bot
CURRENT_VERSION = "2.1.0"


def _parse_version(version: str):
    """Converter string de vers\xc3\xa3o em tupla compar\xc3\xa1vel."""
    return tuple(int(part) for part in version.split("."))


def fetch_update_info():
    """Baixar informa\xc3\xa7\xc3\xb5es de atualiza\xc3\xa7\xc3\xa3o do servidor."""
    try:
        response = requests.get(UPDATE_INFO_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        print(f"\u26a0\ufe0f Falha ao obter informa\xc3\xa7\xc3\xb5es de atualiza\xc3\xa7\xc3\xa3o: {exc}")
        return None


def download_file(url: str, destination: Path):
    """Realizar download do arquivo indicado para o caminho destino."""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(destination, "wb") as f:
            shutil.copyfileobj(r.raw, f)


def apply_update(package_path: Path):
    """Aplicar pacote de atualiza\xc3\xa7\xc3\xa3o (.zip ou .exe)."""
    if package_path.suffix == ".zip":
        with zipfile.ZipFile(package_path, "r") as zf:
            zf.extractall(package_path.parent)
    elif package_path.suffix == ".exe" and os.name == "nt":
        subprocess.Popen([str(package_path)], shell=True)
    else:
        raise RuntimeError("Formato de pacote n\xc3\xa3o suportado")


def check_for_update():
    """Verificar se h\xc3\xa1 nova vers\xc3\xa3o e aplicar se necess\xc3\xa1rio."""
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
