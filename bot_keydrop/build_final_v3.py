#!/usr/bin/env python3
"""
Script para build final do Keydrop Bot Professional v3.0.0
Gera executável otimizado e organiza em dist/
"""

import PyInstaller.__main__
import os
import sys
import shutil
import zipfile
from pathlib import Path

def clean_build():
    """Limpar builds anteriores"""
    try:
        paths_to_clean = ['build', 'dist', '__pycache__']
        for path in paths_to_clean:
            if os.path.exists(path):
                shutil.rmtree(path, ignore_errors=True)
                print(f"✅ Removido: {path}")
        
        # Remover executáveis antigos
        for exe in Path('.').glob('*.exe'):
            exe.unlink()
            print(f"✅ Removido: {exe}")
            
    except Exception as e:
        print(f"⚠️ Erro na limpeza: {e}")

def build_executable():
    """Gerar executável final"""
    try:
        print("🚀 Iniciando build do Keydrop Bot Professional v3.0.0...")
        
        # Parâmetros do PyInstaller
        args = [
            'keydrop_bot_desktop.py',
            '--onefile',
            '--windowed',
            '--name=KeydropBot_Professional_v3.0.0',
            '--icon=bot-icone.ico',
            '--distpath=dist',
            '--workpath=build',
            '--specpath=.',
            '--clean',
            '--optimize=2',
            '--strip',
            '--noupx',
            '--add-data=bot-icone.ico;.',
            '--add-data=config.json;.',
            '--hidden-import=tkinter',
            '--hidden-import=tkinter.ttk',
            '--hidden-import=tkinter.messagebox',
            '--hidden-import=tkinter.scrolledtext',
            '--hidden-import=tkinter.filedialog',
            '--hidden-import=threading',
            '--hidden-import=subprocess',
            '--hidden-import=psutil',
            '--hidden-import=requests',
            '--hidden-import=json',
            '--hidden-import=datetime',
            '--hidden-import=pathlib',
            '--hidden-import=webbrowser',
            '--hidden-import=zipfile',
            '--hidden-import=shutil',
            '--hidden-import=urllib.parse',
            '--hidden-import=random',
            '--exclude-module=matplotlib',
            '--exclude-module=numpy',
            '--exclude-module=pandas',
            '--exclude-module=scipy',
            '--exclude-module=PIL',
            '--exclude-module=cv2'
        ]
        
        print("📦 Executando PyInstaller...")
        PyInstaller.__main__.run(args)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no build: {e}")
        return False

def create_zip():
    """Criar arquivo ZIP do executável"""
    try:
        exe_path = Path("dist/KeydropBot_Professional_v3.0.0.exe")
        if not exe_path.exists():
            print("❌ Executável não encontrado!")
            return False
        
        zip_path = Path("dist/KeydropBot_Professional_v3.0.0.zip")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Adicionar executável
            zipf.write(exe_path, exe_path.name)
            
            # Adicionar arquivos de configuração se existirem
            if Path("config.json").exists():
                zipf.write("config.json", "config.json")
            if Path("bot-icone.ico").exists():
                zipf.write("bot-icone.ico", "bot-icone.ico")
            if Path("README.md").exists():
                zipf.write("README.md", "README.md")
        
        print(f"✅ ZIP criado: {zip_path}")
        print(f"📊 Tamanho do ZIP: {zip_path.stat().st_size / 1024 / 1024:.1f} MB")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar ZIP: {e}")
        return False

def organize_dist():
    """Organizar pasta dist/ conforme solicitado"""
    try:
        dist_path = Path("dist")
        if not dist_path.exists():
            print("❌ Pasta dist não existe!")
            return False
        
        # Listar conteúdo
        files = list(dist_path.glob("*"))
        print(f"\n📁 Conteúdo de dist/:")
        for file in files:
            if file.is_file():
                size_mb = file.stat().st_size / 1024 / 1024
                print(f"   {file.name} ({size_mb:.1f} MB)")
        
        # Verificar se temos o executável e o ZIP
        exe_exists = any(f.name.endswith('.exe') for f in files)
        zip_exists = any(f.name.endswith('.zip') for f in files)
        
        if exe_exists and zip_exists:
            print("✅ Organização concluída: executável e ZIP em dist/")
            return True
        else:
            print("⚠️ Arquivos esperados não encontrados em dist/")
            return False
            
    except Exception as e:
        print(f"❌ Erro na organização: {e}")
        return False

def main():
    """Função principal"""
    try:
        print("🎯 KEYDROP BOT PROFESSIONAL v3.0.0 - BUILD FINAL")
        print("=" * 60)
        
        # Etapa 1: Limpeza
        print("\n1️⃣ Limpando builds anteriores...")
        clean_build()
        
        # Etapa 2: Build
        print("\n2️⃣ Gerando executável...")
        if not build_executable():
            print("❌ Falha no build!")
            sys.exit(1)
        
        # Etapa 3: ZIP
        print("\n3️⃣ Criando arquivo ZIP...")
        if not create_zip():
            print("❌ Falha ao criar ZIP!")
            sys.exit(1)
        
        # Etapa 4: Organização
        print("\n4️⃣ Organizando dist/...")
        if not organize_dist():
            print("❌ Falha na organização!")
            sys.exit(1)
        
        print("\n🎉 BUILD CONCLUÍDO COM SUCESSO!")
        print("📦 Executável: dist/KeydropBot_Professional_v3.0.0.exe")
        print("🗜️ ZIP: dist/KeydropBot_Professional_v3.0.0.zip")
        print("\n✅ Pronto para distribuição!")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
