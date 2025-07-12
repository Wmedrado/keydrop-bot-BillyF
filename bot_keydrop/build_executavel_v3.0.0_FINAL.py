#!/usr/bin/env python3
"""
Script para gerar executável do Keydrop Bot Professional v3.0.0 FINAL
Versão completa com checkbox CONTENDER implementado
"""

import subprocess
import os
import shutil
from pathlib import Path

def build_executable():
    """Gerar executável usando PyInstaller"""
    print("🔨 Gerando executável do Keydrop Bot Professional v3.0.0 FINAL...")
    
    try:
        # Arquivos necessários
        main_file = "keydrop_bot_desktop.py"
        icon_file = "bot-icone.ico" 
        
        # Verificar arquivos
        if not os.path.exists(main_file):
            print(f"❌ Arquivo {main_file} não encontrado!")
            return False
            
        if not os.path.exists(icon_file):
            print(f"⚠️ Ícone {icon_file} não encontrado, continuando sem ícone...")
            icon_file = None
        
        # Comando PyInstaller
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name=KeydropBot_v3.0.0_FINAL_CONTENDER",
            "--distpath=./dist",
            "--workpath=./build",
            "--specpath=.",
        ]
        
        # Adicionar ícone se existir
        if icon_file:
            cmd.extend(["--icon", icon_file])
            cmd.extend(["--add-data", f"{icon_file};."])
        
        # Adicionar arquivo principal
        cmd.append(main_file)
        
        print(f"🚀 Executando: {' '.join(cmd)}")
        
        # Executar PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executável gerado com sucesso!")
            
            # Verificar se foi criado
            exe_path = Path("dist/KeydropBot_v3.0.0_FINAL_CONTENDER.exe")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📦 Executável criado: {exe_path}")
                print(f"📏 Tamanho: {size_mb:.1f} MB")
                
                # Copiar ícone para a pasta dist se existir
                if icon_file and os.path.exists(icon_file):
                    try:
                        shutil.copy2(icon_file, "dist/")
                        print("📋 Ícone copiado para dist/")
                    except Exception:
                        pass
                
                return True
            else:
                print("❌ Executável não foi encontrado após build!")
                return False
        else:
            print("❌ Erro ao gerar executável!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro durante build: {e}")
        return False

def main():
    """Função principal"""
    print("🎯 Build do Keydrop Bot Professional v3.0.0 FINAL")
    print("📋 Versão com checkbox CONTENDER implementado")
    print("-" * 50)
    
    # Verificar se PyInstaller está instalado
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
        print("✅ PyInstaller encontrado")
    except Exception:
        print("❌ PyInstaller não encontrado!")
        print("💡 Instale com: pip install pyinstaller")
        return
    
    # Gerar executável
    success = build_executable()
    
    if success:
        print("\n🎉 BUILD CONCLUÍDO COM SUCESSO!")
        print("📦 Executável: dist/KeydropBot_v3.0.0_FINAL_CONTENDER.exe")
        print("🏆 Checkbox CONTENDER implementado e funcional!")
        print("\n▶️ Para testar: execute o arquivo .exe na pasta dist/")
    else:
        print("\n❌ BUILD FALHOU!")
        print("🔧 Verifique os erros acima e tente novamente")

if __name__ == "__main__":
    main()
