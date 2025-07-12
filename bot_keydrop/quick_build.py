#!/usr/bin/env python3
"""
Build simples para Keydrop Bot Professional v4.0.0
"""

import subprocess
import sys
import os

def main():
    print("🔧 Gerando executável Keydrop Bot Professional v4.0.0...")
    
    try:
        # Instalar PyInstaller se necessário
        try:
            import PyInstaller
            print("✅ PyInstaller disponível")
        except ImportError:
            print("📦 Instalando PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        
        # Build command
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed", 
            "--name", "KeydropBot_v4.0.0",
            "keydrop_bot_desktop.py"
        ]
        
        # Adicionar ícone se existir
        if os.path.exists("../bot-keydrop-main/bot-icone.ico"):
            cmd.extend(["--icon", "../bot-keydrop-main/bot-icone.ico"])
            print("✅ Ícone adicionado")
        
        print("🚀 Executando PyInstaller...")
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("🎉 EXECUTÁVEL CRIADO COM SUCESSO!")
            print("📂 Localização: dist/KeydropBot_v4.0.0.exe")
        else:
            print("❌ Erro no build")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
