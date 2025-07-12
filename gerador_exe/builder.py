import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from log_utils import setup_logger

INSTALLER_SCRIPT = Path(__file__).resolve().with_name("installer_builder.py")

try:
    import importlib
    import psutil
except ImportError:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "psutil"], stdout=subprocess.DEVNULL
    )
    import psutil

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "gerador_exe" / "build_config.json"
BIN_DIR = BASE_DIR / "gerador_exe" / "binario_final"
TEMP_DIR = BASE_DIR / "gerador_exe" / "temp"
LOG_FILE = BASE_DIR / "logs" / "builder.log"

logger = setup_logger("builder")

error_count = 0
warning_count = 0


def log_error(message: str) -> None:
    """Log error and increment counter."""
    global error_count
    error_count += 1
    logger.error(message)


def log_warning(message: str) -> None:
    """Log warning and increment counter."""
    global warning_count
    warning_count += 1
    logger.warning(message)


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


def check_required_files() -> bool:
    """Ensure main project files exist."""
    logger.info("Verificando arquivos essenciais...")
    reqs = {
        "launcher.py": BASE_DIR / "launcher.py",
        "config.json": BASE_DIR / "config.json",
        "requirements.txt": (
            BASE_DIR / "requirements.txt"
            if (BASE_DIR / "requirements.txt").exists()
            else BASE_DIR / "bot_keydrop" / "requirements.txt"
        ),
    }
    cred = BASE_DIR / "firebase_credentials.json"
    if not cred.exists():
        cred = BASE_DIR / "firebase_credentials.json.example"
    reqs["firebase_credentials.json"] = cred

    missing = [name for name, path in reqs.items() if not path.exists()]
    if missing:
        for name in missing:
            log_error(f"Arquivo obrigatório não encontrado: {name}")
        return False
    return True


def check_pyinstaller() -> bool:
    """Verify PyInstaller availability."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            log_error("PyInstaller não está funcional.")
            log_error(result.stdout + result.stderr)
            return False
        logger.debug("PyInstaller %s", result.stdout.strip())
        return True
    except Exception as exc:
        log_error(f"Erro ao verificar PyInstaller: {exc}")
        return False


def validate_environment(min_version=(3, 10)) -> bool:
    logger.info("Verificando ambiente de build...")
    if sys.version_info < min_version:
        log_error(f"Python {min_version[0]}.{min_version[1]}+ é requerido.")
        return False
    for pkg in ("pyinstaller", "pytest", "psutil", "requests"):
        ensure_dependency(pkg)
    if not check_pyinstaller():
        return False
    return True


def run_tests() -> bool:
    """Execute the project's test suite.

    Returns True when tests pass or none are found. Any failure cancels the build.
    """
    logger.info("Executando testes...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"], capture_output=True, text=True
    )

    output = (result.stdout + result.stderr).lower()
    if "no tests ran" in output or "no tests were collected" in output:
        log_warning("⚠️ Nenhum teste encontrado — prosseguindo mesmo assim.")
        logger.info(result.stdout)
        return True

    if result.returncode != 0:
        log_error("❌ Testes falharam.")
        log_error(result.stdout + result.stderr)
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

    main_script = BASE_DIR / config.get("main_script", "")
    if not main_script.exists():
        log_error(f"Arquivo principal '{main_script}' não encontrado.")
        return Path()

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name",
        exe_name,
    ]
    if os.getenv("MODO_DEBUG") == "1":
        cmd.remove("--noconsole")
        cmd.append("--console")
        debug_tester = BASE_DIR / "debug_tester.py"
        if debug_tester.exists():
            cmd.extend(["--add-data", f"{debug_tester};."])
        else:
            log_warning("debug_tester.py não encontrado - modo debug limitado")
        logger.info("Modo debug ativado para o build")
    icon = config.get("icon")
    if icon:
        icon_path = BASE_DIR / icon
        if icon_path.exists():
            cmd.extend(["--icon", str(icon_path)])
        else:
            log_warning(f"Ícone '{icon}' não encontrado. Continuando sem ícone.")

    cmd.append(str(main_script))
    logger.info("Gerando executável...")
    result = subprocess.run(cmd, text=True, capture_output=True, cwd=BASE_DIR)
    if result.returncode != 0:
        log_error("Erro ao gerar executável:\n" + result.stdout + result.stderr)
        return Path()
    dist_path = BASE_DIR / "dist" / exe_name
    if not dist_path.exists():
        log_error("Executável não encontrado em 'dist'")
        return Path()
    return dist_path


def package_build(exe_path: Path, version: str, config: dict) -> Path:
    if not exe_path.exists():
        log_error("Arquivo executável não encontrado para empacotamento.")
        return Path()

    target_exe = BIN_DIR / exe_path.name
    try:
        shutil.copy2(exe_path, target_exe)
    except Exception as exc:
        log_error(f"Erro ao copiar executável: {exc}")
        return Path()

    instrucoes = TEMP_DIR / "INSTRUCOES.txt"
    try:
        instrucoes.write_text(
            "Execute o arquivo .exe para iniciar o Keydrop Bot.\n",
            encoding="utf-8",
        )
        shutil.copy2(exe_path, TEMP_DIR / exe_path.name)
        shutil.copy2(instrucoes, TEMP_DIR / instrucoes.name)
    except Exception as exc:
        log_error(f"Erro ao preparar arquivos temporários: {exc}")
        return Path()

    req_src = BASE_DIR / "bot_keydrop" / "backend" / "requirements.txt"
    if req_src.exists():
        try:
            shutil.copy2(req_src, TEMP_DIR / "requirements.txt")
        except Exception as exc:
            log_warning(f"Não foi possível copiar requirements: {exc}")

    zip_name = f"{config['output_name']}_v{version}_windows.zip"
    zip_path = BIN_DIR / zip_name
    try:
        shutil.make_archive(zip_path.with_suffix(""), "zip", TEMP_DIR)
    except Exception as exc:
        log_error(f"Erro ao criar arquivo zip: {exc}")
        return Path()
    return zip_path


def perform_build(config: dict, version: str, debug: bool = False) -> Path:
    """Compile and package the project for a single mode."""
    build_cfg = dict(config)
    if debug:
        os.environ["MODO_DEBUG"] = "1"
        build_cfg["output_name"] = f"{config['output_name']}_DEBUG"
    else:
        os.environ.pop("MODO_DEBUG", None)

    exe = build_executable(build_cfg, version)
    if not exe:
        return Path()

    zip_path = package_build(exe, version, build_cfg)

    final_exe = BIN_DIR / f"{build_cfg['output_name']}.exe"
    try:
        shutil.copy2(exe, final_exe)
    except Exception as exc:
        log_warning(f"Não foi possível copiar {final_exe.name}: {exc}")

    return zip_path


def generate_installers(exe: Path, version: str) -> None:
    """Create MSI and EXE installers for x64 and x86 architectures."""
    if not INSTALLER_SCRIPT.exists() or not exe.exists():
        log_warning(
            "Installer script ou executável não encontrado; pulando instaladores."
        )
        return

    if not shutil.which("makensis") or not shutil.which("wixl"):
        log_warning("makensis ou wixl ausentes no PATH; instaladores serão ignorados.")
        return

    for arch in ("x64", "x86"):
        logger.info("Gerando instalador %s...", arch)
        cmd = [
            sys.executable,
            str(INSTALLER_SCRIPT),
            "--exe",
            str(exe),
            "--arch",
            arch,
            "--version",
            version,
        ]
        result = subprocess.run(cmd, text=True, capture_output=True)
        if result.returncode != 0:
            log_warning(
                f"Falha ao gerar instalador {arch}:\n{result.stdout}{result.stderr}"
            )


def main():
    start_time = datetime.now()
    config = load_config()
    version = "0.0.0"
    if (BASE_DIR / config.get("version_file", "")).exists():
        with open(BASE_DIR / config["version_file"], "r", encoding="utf-8") as vf:
            version = json.load(vf).get("version", version)
    logger.info(f"Versão do build: {version}")

    if not check_required_files():
        log_error("Arquivos obrigatórios ausentes. Abortando build.")
        return
    if not validate_environment():
        log_error("Ambiente inválido.")
        return
    if not check_port(8000):
        log_error("Porta 8000 em uso. Abortando build.")
        return
    if not run_tests():
        log_error("Build cancelado devido a falhas nos testes.")
        return

    clean_previous_build()

    normal_zip = perform_build(config, version, debug=False)
    debug_zip = perform_build(config, version, debug=True)

    # Gerar instaladores usando o executável normal, se existir
    exe_normal = BIN_DIR / f"{config['output_name']}.exe"
    if exe_normal.exists():
        generate_installers(exe_normal, version)

    end_time = datetime.now()
    logger.info(f"Build normal: {normal_zip}")
    logger.info(f"Build debug: {debug_zip}")
    logger.info(f"Início: {start_time}")
    logger.info(f"Fim: {end_time}")
    logger.info(f"✅ {error_count} erros")
    logger.info(f"⚠️ {warning_count} avisos")
    logger.info(f"📋 Logs salvos em {LOG_FILE.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
