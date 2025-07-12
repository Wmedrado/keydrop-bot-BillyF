#!/usr/bin/env python3
"""
Production launcher for Keydrop Bot Professional
Handles both development and executable modes
"""

import os
import sys
import time
import webbrowser
import threading
import subprocess
import asyncio
import httpx
from pathlib import Path
import importlib.util
from log_utils import setup_logger

logger = setup_logger("production_launcher")

from bot_keydrop.system_safety.environment_checker import (
    verificar_conexao_internet,
    ambiente_compativel,
    executando_no_diretorio_correto,
    LockFile,
)
from bot_keydrop.system_safety.permissions_validator import validar_permissoes
from bot_keydrop.system_safety.backups import backup_arquivo
from bot_keydrop.system_safety.watchdog import ProcessWatchdog
from bot_keydrop.system_safety.error_reporter import error_reporter

BACKEND_PORT = 8000
FRONTEND_URL = f"http://localhost:{BACKEND_PORT}"
lock = LockFile()

class ProductionLauncher:
    def __init__(self):
        self.is_executable = getattr(sys, "frozen", False)
        # Handle PyInstaller temp directory
        if self.is_executable and hasattr(sys, "_MEIPASS"):
            self.base_path = Path(sys._MEIPASS)
        else:
            self.base_path = Path(__file__).parent
    def show_startup_banner(self):
        """Show startup banner"""
        print("🔥" * 60)
        print("🚀 KEYDROP BOT PROFESSIONAL v2.1.0")
        print("⚡ Desenvolvido por William Medrado (wmedrado)")
        print("🔥" * 60)
        print()
        
        if self.is_executable:
            print("📦 Modo: Executável Standalone")
        else:
            print("🛠️  Modo: Desenvolvimento")
        
        print(f"🌐 Interface: {FRONTEND_URL}")
        print(f"📂 Diretório: {self.base_path}")
        print()

    def animate_robot(self, message: str = "Carregando"):
        """Display a simple dancing robot animation"""
        frames = [
            r"[¬º-°]¬",
            r"[¬º-°]¬ ",
            r"[¬º-°]¬♪",
            r"[¬º-°]¬ ",
        ]
        for frame in frames:
            print(f"\r{frame} {message}", end="", flush=True)
            time.sleep(0.25)
        print("\r", end="", flush=True)

    def install_package(self, package: str):
        """Install a package showing progress"""
        cmd = [sys.executable, "-m", "pip", "install", package]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        bar_length = 20
        pos = 0
        while process.poll() is None:
            bar = "=" * pos + ">" + " " * (bar_length - pos)
            self.animate_robot(f"Instalando {package} [{bar}]")
            pos = (pos + 1) % bar_length
        process.communicate()
        if process.returncode == 0:
            print(f"✅ {package} instalado")
        else:
            print(f"❌ Falha ao instalar {package}")

    def verify_python_dependencies(self):
        """Check for required Python packages and install if missing"""
        print("🤖 Verificando dependências do Python...")

        req_file = self.base_path / "backend" / "requirements.txt"
        packages = []
        if req_file.exists():
            for line in req_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    pkg = line.split("==")[0]
                    pkg = pkg.split("[")[0]
                    packages.append(pkg)
        else:
            packages = ["fastapi", "uvicorn", "playwright", "psutil"]

        missing = []
        for pkg in packages:
            if importlib.util.find_spec(pkg) is None:
                missing.append(pkg)
                print(f"❌ {pkg} ausente")
            else:
                print(f"✅ {pkg} disponível")

        if missing:
            print("\n🔧 Instalando dependências...")
            for pkg in missing:
                self.install_package(pkg)
        else:
            print("✅ Todas as dependências já estão instaladas")

    def check_chrome_installation(self):
        """Check if Chrome is installed"""
        print("🔍 Verificando Chrome...")
        
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"),
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"✅ Chrome encontrado: {path}")
                return True
        
        print("⚠️  Chrome não encontrado automaticamente")
        print("💡 Certifique-se de que o Chrome está instalado")
        return False

    def setup_directories(self):
        """Setup required directories"""
        print("📁 Configurando diretórios...")
        
        required_dirs = [
            self.base_path / "profiles",
            self.base_path / "resources",
            self.base_path / "logs",
            self.base_path / "data",
            self.base_path / "__cache__",
        ]
        
        for dir_path in required_dirs:
            dir_path.mkdir(exist_ok=True)
            print(f"✅ {dir_path.name}/")
        
        print()

    def start_backend_server(self):
        """Start the backend server"""
        logger.info("➡️ Iniciando servidor backend...")
        
        try:
            if self.is_executable:
                # In executable mode, start the FastAPI app directly
                sys.path.insert(0, str(self.base_path))
                
                # Import and start the FastAPI app
                try:
                    from main import app
                    import uvicorn
                except ImportError:
                    print("❌ Erro ao importar módulos do backend")
                    return False
                
                # Start server in a thread
                def run_server():
                    uvicorn.run(
                        app, 
                        host="localhost", 
                        port=BACKEND_PORT,
                        log_level="info"
                    )
                
                server_thread = threading.Thread(target=run_server, daemon=True)
                server_thread.start()
                logger.debug("Backend iniciado em thread (modo execut\u00e1vel)")
                
            else:
                # In development mode, use subprocess
                backend_dir = self.base_path / "backend"
                os.chdir(backend_dir)
                
                cmd = [
                    sys.executable, "-m", "uvicorn",
                    "main:app",
                    "--host", "localhost",
                    "--port", str(BACKEND_PORT),
                    "--log-level", "info"
                ]
                
                subprocess.Popen(cmd)
                logger.debug("Backend iniciado via subprocess em %s", backend_dir)
            
            logger.info("✅ Servidor backend iniciado na porta %s", BACKEND_PORT)
            return True
            
        except Exception as e:
            logger.exception("Erro ao iniciar backend: %s", e)
            return False

    async def wait_for_server(self, max_wait: int = 30) -> bool:
        """Wait asynchronously for the backend server to be ready"""
        print("⏳ Aguardando servidor estar pronto...")

        async with httpx.AsyncClient(timeout=2) as client:
            for i in range(max_wait):
                try:
                    response = await client.get(f"{FRONTEND_URL}/health")
                    if response.status_code == 200:
                        print("✅ Servidor pronto!")
                        return True
                except Exception:
                    pass

                await asyncio.sleep(1)
                if i % 5 == 0 and i > 0:
                    print(f"⏳ Aguardando... ({i}s)")

        print("⚠️  Servidor não respondeu em tempo hábil")
        return False

    def open_browser(self):
        """Open browser with the application"""
        logger.info("➡️ Abrindo navegador na URL %s", FRONTEND_URL)
        
        try:
            webbrowser.open(FRONTEND_URL)
            logger.info("✅ Navegador aberto: %s", FRONTEND_URL)
        except Exception as e:
            logger.exception("Erro ao abrir navegador: %s", e)
            logger.info("💡 Abra manualmente: %s", FRONTEND_URL)

    def show_instructions(self):
        """Show usage instructions"""
        print("\n" + "=" * 60)
        print("📖 INSTRUÇÕES DE USO:")
        print("=" * 60)
        print("1. Configure o bot na aba 'Configurações'")
        print("2. Defina a quantidade de guias (1-100)")
        print("3. Configure webhook Discord (opcional)")
        print("4. Clique em 'Iniciar Bot' para começar")
        print("5. Monitore estatísticas em tempo real")
        print("6. Use 'Stop de Emergência' se necessário")
        print()
        print("🔗 Atalhos Úteis:")
        print(f"   Interface: {FRONTEND_URL}")
        print(f"   API Docs:  {FRONTEND_URL}/docs")
        print()
        print("❓ Para sair: Pressione Ctrl+C")
        print("=" * 60)

    async def main_loop(self):
        """Main asynchronous application loop"""
        while True:
            await asyncio.sleep(1)

async def main():
    """Main launcher function"""
    launcher = ProductionLauncher()

    if not lock.acquire():
        print("O Keydrop Bot já está em execução!")
        return

    if not executando_no_diretorio_correto():
        print("Ambiente incompatível: Arquivos essenciais não encontrados.")
        return

    if not ambiente_compativel():
        print("Ambiente incompatível: Este bot foi projetado para Windows 10+ com Python 3.10+.")
        return

    if not validar_permissoes(["logs", "data", "profiles", "__cache__"]):
        print("Erro de permissão: execute o bot como administrador ou verifique as pastas.")
        return

    if not verificar_conexao_internet():
        print("Sem conexão com a internet. Tentando novamente em alguns segundos...")
        for _ in range(5):
            await asyncio.sleep(5)
            if verificar_conexao_internet():
                break
        else:
            print("Conexão indisponível. Abortando execução.")
            return

    watchdog = ProcessWatchdog()
    watchdog.start()

    # Show banner
    launcher.show_startup_banner()

    # Verify Python packages
    launcher.verify_python_dependencies()

    from bot_keydrop.system_safety import run_dependency_check
    if not run_dependency_check():
        print("Algumas dependências estão ausentes ou incorretas. Revise a mensagem acima.")

    # Check dependencies
    launcher.check_chrome_installation()
    
    # Setup directories
    launcher.setup_directories()

    for cfg_name in ("bot_config.json", "user_session.json", "firebase_credentials.json"):
        backup_arquivo(Path(cfg_name))
    
    # Start backend
    if not launcher.start_backend_server():
        input("❌ Falha ao iniciar. Pressione Enter para sair...")
        sys.exit(1)
    
    # Wait for server
    if not await launcher.wait_for_server():
        input("❌ Servidor não iniciou. Pressione Enter para sair...")
        sys.exit(1)
    
    # Open browser
    launcher.open_browser()
    
    # Show instructions
    launcher.show_instructions()
    
    # Main loop
    try:
        await launcher.main_loop()
    finally:
        watchdog.stop()
        lock.release()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Parando aplicação...")
        print("👋 Obrigado por usar Keydrop Bot Professional!")
        try:
            lock.release()
        except Exception:
            pass
    except Exception as exc:  # pragma: no cover - final fallback
        error_reporter.capture_exception(exc)
        print("Erro inesperado. Detalhes registrados em logs/error_report.log")
