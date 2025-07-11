#!/usr/bin/env python3
"""
Build script for creating executable from Keydrop Bot Professional
Generates a single executable file for easy distribution
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"

class ExecutableBuilder:
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.spec_file = None

    def check_pyinstaller(self):
        """Check if PyInstaller is available"""
        try:
            import PyInstaller
            print("✅ PyInstaller encontrado")
            return True
        except ImportError:
            print("❌ PyInstaller não encontrado")
            print("💡 Instale com: pip install pyinstaller")
            return False

    def prepare_frontend_assets(self):
        """Prepare frontend assets for inclusion"""
        print("📦 Preparando assets do frontend...")
        
        assets_dir = BACKEND_DIR / "static"
        assets_dir.mkdir(exist_ok=True)
        
        # Copy frontend files
        if FRONTEND_DIR.exists():
            # Copy all frontend files to backend/static
            shutil.copytree(
                FRONTEND_DIR, 
                assets_dir, 
                dirs_exist_ok=True
            )
            print("✅ Assets do frontend copiados")
        
        return assets_dir

    def create_pyinstaller_spec(self):
        """Create PyInstaller spec file"""
        print("📝 Criando arquivo .spec...")
        
        assets_dir = self.prepare_frontend_assets()
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [r'{BACKEND_DIR / "main.py"}'],
    pathex=[r'{BACKEND_DIR}'],
    binaries=[],
    datas=[
        (r'{assets_dir}', 'static'),
        (r'{BACKEND_DIR / "config"}', 'config'),
        (r'{PROJECT_ROOT / "profiles"}', 'profiles'),
        (r'{PROJECT_ROOT / "resources"}', 'resources'),
    ],
    hiddenimports=[
        'fastapi',
        'uvicorn',
        'playwright',
        'psutil',
        'asyncio',
        'json',
        'datetime',
        'pathlib',
        'logging',
        'multiprocessing',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KeydropBot_Professional',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
        
        spec_file = PROJECT_ROOT / "keydrop_bot.spec"
        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        self.spec_file = spec_file
        print(f"✅ Arquivo spec criado: {spec_file}")
        return spec_file

    def build_executable(self):
        """Build the executable using PyInstaller"""
        print("🔨 Construindo executável...")
        
        if not self.spec_file:
            print("❌ Arquivo .spec não encontrado")
            return False
        
        try:
            # Change to project directory
            os.chdir(self.project_root)
            
            # Run PyInstaller
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--clean",
                "--noconfirm",
                str(self.spec_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Executável construído com sucesso!")
                
                # Check if executable exists
                exe_path = DIST_DIR / "KeydropBot_Professional.exe"
                if exe_path.exists():
                    print(f"📦 Executável criado: {exe_path}")
                    print(f"📊 Tamanho: {exe_path.stat().st_size / (1024*1024):.1f} MB")
                    return True
                else:
                    print("❌ Executável não encontrado após build")
                    return False
            else:
                print(f"❌ Erro no build: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Erro durante build: {e}")
            return False

    def cleanup(self):
        """Clean up build artifacts"""
        print("🧹 Limpando arquivos temporários...")
        
        # Remove build directory
        if BUILD_DIR.exists():
            shutil.rmtree(BUILD_DIR)
            print("✅ Diretório build removido")
        
        # Remove spec file
        if self.spec_file and self.spec_file.exists():
            self.spec_file.unlink()
            print("✅ Arquivo .spec removido")

    def create_installer_info(self):
        """Create installer information file"""
        info_content = f"""# Keydrop Bot Professional v2.1.0
## Executável Standalone

### Informações do Build:
- **Versão:** 2.1.0
- **Data:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Desenvolvedor:** William Medrado (wmedrado)
- **Plataforma:** Windows

### Como Usar:
1. Execute `KeydropBot_Professional.exe`
2. Aguarde a inicialização do servidor
3. Acesse http://localhost:8000 no navegador
4. Configure e inicie o bot

### Requisitos:
- Windows 10/11
- Chrome/Chromium instalado
- Conexão com internet

### Funcionalidades:
- Interface web moderna
- Gerenciamento de até 100 guias Chrome
- Perfis únicos por guia
- Monitoramento em tempo real
- Integração Discord
- Sistema de relatórios
- Stop de emergência

### Suporte:
GitHub: https://github.com/wmedrado
"""
        
        info_file = DIST_DIR / "README_EXECUTAVEL.md"
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(info_content)
        
        print(f"✅ Informações do executável: {info_file}")

def main():
    """Main build process"""
    print("🚀 Keydrop Bot Professional - Build Executable")
    print("=" * 60)
    
    builder = ExecutableBuilder()
    
    # Check dependencies
    if not builder.check_pyinstaller():
        sys.exit(1)
    
    try:
        # Create spec file
        builder.create_pyinstaller_spec()
        
        # Build executable
        if builder.build_executable():
            # Create installer info
            builder.create_installer_info()
            print("\n🎉 Build concluído com sucesso!")
            print(f"📁 Executável disponível em: {DIST_DIR}")
        else:
            print("\n❌ Falha no build")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n🛑 Build cancelado pelo usuário")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
    
    finally:
        # Cleanup
        builder.cleanup()

if __name__ == "__main__":
    main()
