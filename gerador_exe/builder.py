import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import logging

try:
    import importlib
    import psutil
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"], stdout=subprocess.DEVNULL)
    import psutil

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "gerador_exe" / "build_config.json"
BIN_DIR = BASE_DIR / "gerador_exe" / "binario_final"
TEMP_DIR = BASE_DIR / "gerador_exe" / "temp"
LOG_FILE = BASE_DIR / "gerador_exe" / "build_log.txt"

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("builder")


def load_config():
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "main_script": "launcher.py",
        "output_name": "KeydropBot",
        "version_file": "update_info_example.json",
        "icon": "bot-icone.ico",
    }


def ensure_dependency(package: str) -> None:
    try:
        importlib.import_module(package)
    except ImportError:
        logger.info(f"Instalando dependência faltante: {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def validate_environment(min_version=(3, 10)) -> bool:
    logger.info("Verificando ambiente de build...")
    if sys.version_info < min_version:
        logger.error(f"Python {min_version[0]}.{min_version[1]}+ é requerido.")
        return False
    for pkg in ("pyinstaller", "pytest", "psutil", "requests"):
        ensure_dependency(pkg)
    return True


def run_tests() -> bool:
    logger.info("Executando testes...")
    result = subprocess.run([sys.executable, "-m", "pytest", "-q"], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("Falha nos testes:\n" + result.stdout + result.stderr)
        return False
    logger.info(result.stdout)
    return True


def clean_previous_build():
    logger.info("Limpando build anterior...")
    for name in ["build", "dist", "__pycache__"]:
        path = BASE_DIR / name
        if path.exists():
            shutil.rmtree(path)
    for spec in BASE_DIR.glob("*.spec"):
        spec.unlink()
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    BIN_DIR.mkdir(parents=True, exist_ok=True)


def check_port(port: int = 8000) -> bool:
    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr and conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
            return False
    return True


def build_executable(config: dict, version: str) -> Path:
    exe_name = f"{config['output_name']}_v{version}.exe"
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name",
        exe_name,
    ]
    icon = config.get("icon")
    if icon and (BASE_DIR / icon).exists():
        cmd.extend(["--icon", str(BASE_DIR / icon)])
    cmd.append(str(BASE_DIR / config["main_script"]))
    logger.info("Gerando executável...")
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        logger.error("Erro ao gerar executável:\n" + result.stdout + result.stderr)
        return Path()
    dist_path = BASE_DIR / "dist" / exe_name
    if not dist_path.exists():
        logger.error("Executável não encontrado em 'dist'")
        return Path()
    return dist_path


def package_build(exe_path: Path, version: str, config: dict) -> Path:
    target_exe = BIN_DIR / exe_path.name
    shutil.copy2(exe_path, target_exe)

    instrucoes = TEMP_DIR / "INSTRUCOES.txt"
    instrucoes.write_text(
        "Execute o arquivo .exe para iniciar o Keydrop Bot.\n",
        encoding="utf-8",
    )

    shutil.copy2(exe_path, TEMP_DIR / exe_path.name)
    shutil.copy2(instrucoes, TEMP_DIR / instrucoes.name)
    req_src = BASE_DIR / "bot_keydrop" / "backend" / "requirements.txt"
    if req_src.exists():
        shutil.copy2(req_src, TEMP_DIR / "requirements.txt")

    zip_name = f"{config['output_name']}_v{version}_windows.zip"
    zip_path = BIN_DIR / zip_name
    shutil.make_archive(zip_path.with_suffix(""), "zip", TEMP_DIR)
    return zip_path


def main():
    start_time = datetime.now()
    with open(LOG_FILE, "w", encoding="utf-8") as log_file:
        handler = logging.StreamHandler(log_file)
        logger.addHandler(handler)
        config = load_config()
        version = "0.0.0"
        if (BASE_DIR / config.get("version_file", "")).exists():
            with open(BASE_DIR / config["version_file"], "r", encoding="utf-8") as vf:
                version = json.load(vf).get("version", version)
        logger.info(f"Versão do build: {version}")

        if not validate_environment():
            logger.error("Ambiente inválido.")
            return
        if not check_port(8000):
            logger.error("Porta 8000 em uso. Abortando build.")
            return
        if not run_tests():
            logger.error("Build cancelado devido a falhas nos testes.")
            return
        clean_previous_build()
        exe = build_executable(config, version)
        if not exe:
            logger.error("Build falhou.")
            return
        zip_path = package_build(exe, version, config)
        end_time = datetime.now()
        logger.info(f"Build concluído em {zip_path}")
        logger.info(f"Início: {start_time}")
        logger.info(f"Fim: {end_time}")


if __name__ == "__main__":
    main()
