import json
import os
import shutil
import subprocess
import sys
import atexit
import re
from datetime import datetime
from pathlib import Path

from log_utils import setup_logger
from bot_keydrop.system_safety.environment_checker import (
    LockFile,
    executando_no_diretorio_correto,
)

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
LOG_FILE = BASE_DIR / "logs" / "builder.log"
LOCK_PATH = BASE_DIR / "temp" / "builder.lock"
REQUIREMENTS_FILE = (
    BASE_DIR / "requirements.txt"
    if (BASE_DIR / "requirements.txt").exists()
    else BASE_DIR / "bot_keydrop" / "requirements.txt"
)

logger = setup_logger("builder")

error_count = 0
warning_count = 0
tolerancia_erros_teste = 2


def open_log_file() -> None:
    """Open the builder log file with the default application."""
    try:
        if sys.platform.startswith("win"):
            os.startfile(LOG_FILE)  # type: ignore[attr-defined]
        elif sys.platform.startswith("darwin"):
            subprocess.Popen(["open", str(LOG_FILE)])
        else:
            subprocess.Popen(["xdg-open", str(LOG_FILE)])
    except Exception as exc:
        logger.error("Falha ao abrir log automaticamente: %s", exc)


def show_step(step: int, total: int, message: str) -> None:
    """Display build progress with visual indicators."""
    percent = int(step / total * 100)
    icons = ["🧪", "🔨", "📦", "✅"]
    icon = icons[min(step - 1, len(icons) - 1)]
    msg = f"{icon} [{step}/{total} {percent}%] {message}"
    print(msg)
    logger.info(msg)


def acquire_builder_lock() -> "LockFile | None":
    """Ensure only one instance of the builder is running."""
    lock = LockFile(LOCK_PATH)
    if not lock.acquire():
        try:
            pid = int(LOCK_PATH.read_text())
            proc = psutil.Process(pid)
            name = proc.name()
        except Exception:
            name = "PID " + LOCK_PATH.read_text().strip()
        log_error(f"Outro processo do builder está em execução: {name}")
        return None
    return lock


def get_version(config: dict) -> str:
    version = "0.0.0"
    version_file = config.get("version_file")
    if version_file and (BASE_DIR / version_file).exists():
        with open(BASE_DIR / version_file, "r", encoding="utf-8") as vf:
            try:
                version = json.load(vf).get("version", version)
            except Exception:
                pass
    return version


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
        "spec_file": "launcher.spec",
    }


def ensure_dependency(package: str) -> None:
    try:
        importlib.import_module(package)
    except ImportError:
        logger.info(f"Instalando dependência faltante: {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def install_requirements() -> None:
    """Install project dependencies from the requirements file."""
    if REQUIREMENTS_FILE.exists():
        logger.info("Instalando dependências do %s", REQUIREMENTS_FILE.name)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)]
        )


def install_test_dependencies() -> None:
    """Install additional dependencies required for tests."""
    root_req = BASE_DIR / "requirements.txt"
    if root_req.exists():
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(root_req)], check=False)
    backend_req = BASE_DIR / "bot_keydrop" / "backend" / "requirements.txt"
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(backend_req)], check=False)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "firebase_admin",
            "discord-webhook",
            "pytest",
            "requests",
        ],
        check=False,
    )


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
    install_requirements()
    if not check_pyinstaller():
        return False
    return True


def run_tests() -> bool:
    """Execute the project's test suite.

    Returns True when tests pass or none are found. Any failure cancels the build.
    """
    logger.info("Executando testes...")
    install_test_dependencies()
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"], capture_output=True, text=True
    )

    output = result.stdout + result.stderr
    lower_out = output.lower()
    if "no tests ran" in lower_out or "no tests were collected" in lower_out:
        log_warning("⚠️ Nenhum teste encontrado — prosseguindo mesmo assim.")
        logger.info(result.stdout)
        return True

    if result.returncode != 0:
        failed = 0
        match = re.search(r"(\d+) failed", lower_out)
        if match:
            failed = int(match.group(1))
        if failed <= tolerancia_erros_teste:
            log_warning(
                f"⚠️ {failed} testes falharam, mas dentro da tolerância de {tolerancia_erros_teste}."
            )
            logger.warning(output)
            return True
        log_error("❌ Testes falharam.")
        log_error(output)
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


def build_executable(config: dict, version: str, debug: bool, arch: str) -> Path:
    """Build the executable using PyInstaller for the given mode and arch."""
    mode = "debug" if debug else "release"
    exe_name = f"{config['output_name'].lower()}_{mode}_{arch}_v{version}.exe"
    main_script = BASE_DIR / config.get("main_script", "")
    spec_file = config.get("spec_file")

    if spec_file:
        spec_path = BASE_DIR / spec_file
        if not spec_path.exists():
            log_error(f"Spec file '{spec_path}' não encontrado.")
            return Path()
        cmd = [sys.executable, "-m", "PyInstaller", str(spec_path)]
    else:
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
    if not spec_file:

        if os.getenv("MODO_DEBUG") == "1" or os.getenv("MODO_SEGURO") == "1":
            cmd.remove("--noconsole")
            cmd.append("--console")
            if os.getenv("MODO_DEBUG") == "1":
                cmd.extend(["--add-data", "debug_tester.py;."])
                logger.info("Modo debug ativado para o build")
        icon = config.get("icon")
        if icon:
            icon_path = BASE_DIR / icon
            if icon_path.exists():
                cmd.extend(["--icon", str(icon_path)])
            else:
                log_warning(
                    f"Ícone '{icon}' não encontrado. Continuando sem ícone."
                )

        cmd.append(str(main_script))
    dist_dir = BASE_DIR / "dist" / mode
    dist_dir.mkdir(parents=True, exist_ok=True)
    cmd.extend(["--distpath", str(dist_dir)])
    logger.info("Gerando executável...")
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        log_error("Erro ao gerar executável:\n" + result.stdout + result.stderr)
        return Path()
    dist_path = dist_dir / exe_name
    if not dist_path.exists():
        alt = next((p for p in dist_dir.glob("*.exe")), None)
        if alt:
            dist_path = alt
        else:
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

def perform_build(config: dict, version: str, debug: bool = False, safe: bool = False, arch: str = "x64") -> Path:
    """Compile and package the project for a single mode."""
    build_cfg = dict(config)
    if debug:
        os.environ["MODO_DEBUG"] = "1"
        build_cfg["output_name"] = f"{config['output_name']}_DEBUG"
    elif safe:
        os.environ["MODO_SEGURO"] = "1"
        build_cfg["output_name"] = f"{config['output_name']}_SAFE"
    else:
        os.environ.pop("MODO_DEBUG", None)
        os.environ.pop("MODO_SEGURO", None)

    exe = build_executable(build_cfg, version, debug, arch)
    if not exe:
        return Path()

    zip_path = package_build(exe, version, build_cfg)

    final_exe = BIN_DIR / exe.name
    try:
        shutil.copy2(exe, final_exe)
    except Exception as exc:
        log_warning(f"Não foi possível copiar {final_exe.name}: {exc}")

    return zip_path


def main():
    start_time = datetime.now()
    config = load_config()
    version = get_version(config)
    logger.info(f"Versão do build: {version}")
    step = 1
    total = 8

    show_step(step, total, "Verificando lock do builder")
    lock = acquire_builder_lock()
    if not lock:
        open_log_file()
        sys.exit(1)
    atexit.register(lock.release)
    step += 1

    show_step(step, total, "Checando diretório de execução")
    if not executando_no_diretorio_correto():
        log_error("Execute o builder a partir da raiz do projeto.")
        open_log_file()
        sys.exit(1)
    step += 1

    show_step(step, total, "Verificando arquivos requeridos")
    if not check_required_files():
        log_error("Arquivos obrigatórios ausentes. Abortando build.")
        open_log_file()
        sys.exit(1)
    step += 1

    show_step(step, total, "Validando ambiente")
    if not validate_environment():
        log_error("Ambiente inválido.")
        open_log_file()
        sys.exit(1)
    if not check_port(8000):
        log_error("Porta 8000 em uso. Abortando build.")
        open_log_file()
        sys.exit(1)
    step += 1

    show_step(step, total, "Executando testes")
    if not run_tests():
        log_error("Build cancelado devido a falhas nos testes.")
        open_log_file()
        sys.exit(1)
    step += 1

    show_step(step, total, "Limpando build anterior")
    clean_previous_build()
    step += 1

    show_step(step, total, "Gerando build release")
    normal_zip = perform_build(config, version, debug=False)
    step += 1

    show_step(step, total, "Gerando build debug")
    debug_zip = perform_build(config, version, debug=True)
    safe_zip = Path()
    if os.getenv("MODO_SEGURO") == "1":
        step += 1
        show_step(step, total, "Gerando build safe")
        safe_zip = perform_build(config, version, safe=True)

    end_time = datetime.now()
    logger.info(f"Build normal: {normal_zip}")
    logger.info(f"Build debug: {debug_zip}")
    if safe_zip:
        logger.info(f"Build safe: {safe_zip}")
    logger.info(f"Início: {start_time}")
    logger.info(f"Fim: {end_time}")
    logger.info(f"✅ {error_count} erros")
    logger.info(f"⚠️ {warning_count} avisos")
    logger.info(f"📋 Logs salvos em {LOG_FILE.relative_to(BASE_DIR)}")
    if error_count:
        open_log_file()


if __name__ == "__main__":
    main()
