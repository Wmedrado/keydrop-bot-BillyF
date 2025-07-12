#!/usr/bin/env python3
"""
Startup script for Keydrop Bot Professional
Starts both backend and frontend for development/testing
"""

import os
import sys
import subprocess
import time
import threading
import signal
from pathlib import Path
import atexit

from bot_keydrop.system_safety import LockFile

# Configuration
BACKEND_DIR = Path(__file__).parent / "backend"
FRONTEND_DIR = Path(__file__).parent / "frontend"
BACKEND_PORT = 8000
FRONTEND_PORT = 3000

lock = LockFile()
atexit.register(lock.release)


class BotStarter:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True

    def check_dependencies(self):
        """Check if all dependencies are available"""
        print("🔍 Verificando dependências...")

        # Check Python
        try:
            import sys

            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            print(f"✅ Python {python_version}")
        except Exception as e:
            print(f"❌ Erro no Python: {e}")
            return False

        # Check if requirements are installed
        requirements_file = BACKEND_DIR / "requirements.txt"
        if requirements_file.exists():
            try:
                import importlib.util

                required_modules = ["fastapi", "playwright", "psutil"]
                for module in required_modules:
                    if importlib.util.find_spec(module) is None:
                        print(f"❌ Dependência não encontrada: {module}")
                        print("💡 Execute: pip install -r backend/requirements.txt")
                        return False

                print("✅ Dependências básicas disponíveis")

            except ImportError as e:
                print(f"❌ Dependência não encontrada: {e}")
                print("💡 Execute: pip install -r backend/requirements.txt")
                return False

        return True

    def start_backend(self):
        """Start the backend FastAPI server"""
        print("🚀 Iniciando backend...")

        try:
            os.chdir(BACKEND_DIR)

            # Command to start FastAPI with uvicorn
            cmd = [
                sys.executable,
                "-m",
                "uvicorn",
                "main:app",
                "--host",
                "localhost",
                "--port",
                str(BACKEND_PORT),
                "--reload",
                "--log-level",
                "info",
            ]

            self.backend_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            print(f"✅ Backend iniciado na porta {BACKEND_PORT}")
            print(f"📡 API: http://localhost:{BACKEND_PORT}")
            print(f"📚 Docs: http://localhost:{BACKEND_PORT}/docs")

            return True

        except Exception as e:
            print(f"❌ Erro ao iniciar backend: {e}")
            return False

    def start_frontend(self):
        """Start the frontend development server"""
        print("🎨 Iniciando frontend...")

        try:
            os.chdir(FRONTEND_DIR)

            # Command to start simple HTTP server
            cmd = [sys.executable, "-m", "http.server", str(FRONTEND_PORT)]

            self.frontend_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            print(f"✅ Frontend iniciado na porta {FRONTEND_PORT}")
            print(f"🌐 Interface: http://localhost:{FRONTEND_PORT}")

            return True

        except Exception as e:
            print(f"❌ Erro ao iniciar frontend: {e}")
            return False

    def wait_for_backend(self, max_retries=30):
        """Wait for backend to be ready"""
        print("⏳ Aguardando backend ficar disponível...")

        import requests

        for i in range(max_retries):
            try:
                resp = requests.get(
                    f"http://localhost:{BACKEND_PORT}/health",
                    timeout=2,
                )
                resp.raise_for_status()
                print("✅ Backend está pronto!")
                return True
            except (requests.RequestException, ConnectionRefusedError):
                time.sleep(1)
                if i % 5 == 0:
                    print(f"⏳ Tentativa {i+1}/{max_retries}...")

        print("❌ Backend não ficou disponível a tempo")
        return False

    def open_browser(self):
        """Open the frontend in the default browser"""
        try:
            import webbrowser

            time.sleep(2)  # Wait a bit for servers to stabilize
            webbrowser.open(f"http://localhost:{FRONTEND_PORT}")
            print("🌐 Interface aberta no navegador")
        except Exception as e:
            print(f"⚠️ Não foi possível abrir o navegador: {e}")

    def monitor_processes(self):
        """Monitor backend and frontend processes"""
        while self.running:
            time.sleep(5)

            # Check backend
            if self.backend_process and self.backend_process.poll() is not None:
                print("❌ Backend parou inesperadamente")
                self.running = False
                break

            # Check frontend
            if self.frontend_process and self.frontend_process.poll() is not None:
                print("❌ Frontend parou inesperadamente")
                self.running = False
                break

    def stop_all(self):
        """Stop all processes"""
        print("\n🛑 Parando serviços...")

        self.running = False

        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend parado")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                print("🔥 Backend forçado a parar")
            except Exception as e:
                print(f"⚠️ Erro ao parar backend: {e}")

        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend parado")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                print("🔥 Frontend forçado a parar")
            except Exception as e:
                print(f"⚠️ Erro ao parar frontend: {e}")

    def signal_handler(self, signum, frame):
        """Handle interrupt signals"""
        print("\n🔄 Recebido sinal de interrupção...")
        self.stop_all()
        sys.exit(0)

    def run(self):
        """Main execution method"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        print("🚀 Keydrop Bot Professional - Startup")
        print("=" * 50)

        # Check dependencies
        if not self.check_dependencies():
            print("❌ Dependências não atendidas. Abortando...")
            return False

        # Start backend
        if not self.start_backend():
            print("❌ Falha ao iniciar backend. Abortando...")
            return False

        # Wait for backend to be ready
        if not self.wait_for_backend():
            print("❌ Backend não ficou pronto. Abortando...")
            self.stop_all()
            return False

        # Start frontend
        if not self.start_frontend():
            print("❌ Falha ao iniciar frontend. Parando backend...")
            self.stop_all()
            return False

        # Open browser
        browser_thread = threading.Thread(target=self.open_browser)
        browser_thread.daemon = True
        browser_thread.start()

        # Start monitoring
        monitor_thread = threading.Thread(target=self.monitor_processes)
        monitor_thread.daemon = True
        monitor_thread.start()

        print("\n✅ Todos os serviços iniciados com sucesso!")
        print("=" * 50)
        print(f"🔗 Backend API: http://localhost:{BACKEND_PORT}")
        print(f"🔗 Backend Docs: http://localhost:{BACKEND_PORT}/docs")
        print(f"🔗 Frontend: http://localhost:{FRONTEND_PORT}")
        print("=" * 50)
        print("💡 Pressione Ctrl+C para parar todos os serviços")
        print()

        try:
            # Keep main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all()

        return True


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print("Keydrop Bot Professional - Startup Script")
        print()
        print("Uso: python startup.py")
        print()
        print("Este script inicia tanto o backend (FastAPI) quanto o frontend")
        print("(servidor HTTP simples) para desenvolvimento e teste da aplicação.")
        print()
        print("Requisitos:")
        print("- Python 3.8+")
        print("- Dependências em backend/requirements.txt instaladas")
        print()
        print("Portas utilizadas:")
        print(f"- Backend: {BACKEND_PORT}")
        print(f"- Frontend: {FRONTEND_PORT}")
        return

    if not lock.acquire():
        print("O Keydrop Bot já está em execução!")
        return

    starter = BotStarter()
    success = starter.run()

    if success:
        print("👋 Keydrop Bot Professional encerrado com sucesso")
    else:
        print("❌ Keydrop Bot Professional encerrado com erros")
        sys.exit(1)

    lock.release()


if __name__ == "__main__":
    main()
