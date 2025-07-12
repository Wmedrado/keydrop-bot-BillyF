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
import importlib.util
from pathlib import Path

# Configuration
BACKEND_PORT = 8000
FRONTEND_URL = f"http://localhost:{BACKEND_PORT}"

class ProductionLauncher:
    def __init__(self):
        self.is_executable = getattr(sys, 'frozen', False)
        # Handle PyInstaller temp directory
        if self.is_executable and hasattr(sys, '_MEIPASS'):
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
        """Display a small dancing robot animation"""
        frames = [
            r"[¬º-°]¬",
            r"[¬º-°]¬ ",
            r"[¬º-°]¬♪",
            r"[¬º-°]¬ ",
        ]
        for frame in frames:
            print(f"\r{frame} {message}", end="", flush=True)
            time.sleep(0.3)
        print("\r", end="", flush=True)

    def install_package(self, package: str):
        """Install a Python package showing a progress animation"""
        cmd = [sys.executable, "-m", "pip", "install", package]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
        """Check and install Python dependencies"""
        print("🤖 Verificando dependências Python...")

        req_file = self.base_path / "backend" / "requirements.txt"
        packages = []
        if req_file.exists():
            for line in req_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    pkg = line.split("==")[0]
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
        ]
        
        for dir_path in required_dirs:
            dir_path.mkdir(exist_ok=True)
            print(f"✅ {dir_path.name}/")
        
        print()

    def start_backend_server(self):
        """Start the backend server"""
        print("🚀 Iniciando servidor backend...")
        
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
            
            print(f"✅ Servidor backend iniciado na porta {BACKEND_PORT}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao iniciar backend: {e}")
            return False

    def wait_for_server(self, max_wait=30):
        """Wait for server to be ready"""
        print("⏳ Aguardando servidor estar pronto...")
        
        import requests
        
        for i in range(max_wait):
            try:
                response = requests.get(f"{FRONTEND_URL}/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Servidor pronto!")
                    return True
            except:
                pass
            
            time.sleep(1)
            if i % 5 == 0 and i > 0:
                print(f"⏳ Aguardando... ({i}s)")
        
        print("⚠️  Servidor não respondeu em tempo hábil")
        return False

    def open_browser(self):
        """Open browser with the application"""
        print("🌐 Abrindo navegador...")
        
        try:
            webbrowser.open(FRONTEND_URL)
            print(f"✅ Navegador aberto: {FRONTEND_URL}")
        except Exception as e:
            print(f"❌ Erro ao abrir navegador: {e}")
            print(f"💡 Abra manualmente: {FRONTEND_URL}")

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

    def main_loop(self):
        """Main application loop"""
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Parando aplicação...")
            print("👋 Obrigado por usar Keydrop Bot Professional!")
            sys.exit(0)

def main():
    """Main launcher function"""
    launcher = ProductionLauncher()

    # Show banner
    launcher.show_startup_banner()

    # Verify Python requirements
    launcher.verify_python_dependencies()

    # Check dependencies
    launcher.check_chrome_installation()
    
    # Setup directories
    launcher.setup_directories()
    
    # Start backend
    if not launcher.start_backend_server():
        input("❌ Falha ao iniciar. Pressione Enter para sair...")
        sys.exit(1)
    
    # Wait for server
    if not launcher.wait_for_server():
        input("❌ Servidor não iniciou. Pressione Enter para sair...")
        sys.exit(1)
    
    # Open browser
    launcher.open_browser()
    
    # Show instructions
    launcher.show_instructions()
    
    # Main loop
    launcher.main_loop()

if __name__ == "__main__":
    main()
