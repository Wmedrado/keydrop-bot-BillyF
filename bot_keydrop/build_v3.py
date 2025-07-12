#!/usr/bin/env python3
"""
Script de Build para Keydrop Bot Professional v3.0.0
Gera executável otimizado com ícone personalizado
"""

import sys
import shutil
import subprocess
from pathlib import Path

def main():
    print("🚀 BUILD KEYDROP BOT PROFESSIONAL v3.0.0")
    print("=" * 50)
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado!")
        print("💡 Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Paths
    script_dir = Path(__file__).parent
    main_script = script_dir / "keydrop_bot_desktop.py"
    icon_file = script_dir / "bot-icone.ico"
    dist_dir = script_dir / "dist"
    
    # Verificar arquivos necessários
    if not main_script.exists():
        print(f"❌ Script principal não encontrado: {main_script}")
        return False
    
    if not icon_file.exists():
        print(f"⚠️ Ícone não encontrado: {icon_file}")
        icon_param = ""
    else:
        print(f"✅ Ícone encontrado: {icon_file}")
        icon_param = f"--icon={icon_file}"
    
    # Limpar build anterior
    if dist_dir.exists():
        print("🧹 Limpando build anterior...")
        shutil.rmtree(dist_dir)
    
    build_dir = script_dir / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Comando PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name=KeydropBot_Desktop_v3.0.0",
        "--noconsole" if "--noconsole" in sys.argv else "--console",
        "--add-data=bot-icone.ico;." if icon_file.exists() else "",
        icon_param,
        "--distpath=dist",
        "--workpath=build",
        "--specpath=build",
        "--clean",
        str(main_script)
    ]
    
    # Remover parâmetros vazios
    cmd = [arg for arg in cmd if arg.strip()]
    
    print("🔧 Comando PyInstaller:")
    print(" ".join(cmd))
    print()
    
    # Executar build
    print("⚙️ Iniciando build...")
    try:
        subprocess.run(cmd, check=True, capture_output=False)
        print("✅ Build concluído com sucesso!")
        
        # Verificar executável gerado
        exe_path = dist_dir / "KeydropBot_Desktop_v3.0.0.exe"
        if exe_path.exists():
            exe_size = exe_path.stat().st_size / (1024 * 1024)  # MB
            print(f"📁 Executável: {exe_path}")
            print(f"📏 Tamanho: {exe_size:.1f} MB")
            
            # Copiar ícone para dist se existir
            if icon_file.exists():
                shutil.copy2(icon_file, dist_dir)
                print(f"📋 Ícone copiado para: {dist_dir / 'bot-icone.ico'}")
            
            # Criar script de teste
            test_script = dist_dir / "TESTAR_v3.0.0.bat"
            test_script.write_text(f"""@echo off
title Teste Keydrop Bot v3.0.0
echo.
echo   🤖 KEYDROP BOT PROFESSIONAL v3.0.0
echo   ======================================
echo.
echo   Testando executável...
echo.
if exist "KeydropBot_Desktop_v3.0.0.exe" (
    echo   ✅ Executável encontrado!
    echo   🚀 Iniciando aplicação...
    echo.
    start "" "KeydropBot_Desktop_v3.0.0.exe"
    echo   📱 Se a janela abrir, o build foi bem-sucedido!
) else (
    echo   ❌ Executável não encontrado!
)
echo.
pause
""")
            
            print("📝 Script de teste criado: TESTAR_v3.0.0.bat")
            print()
            print("🎉 BUILD v3.0.0 COMPLETO!")
            print("=" * 50)
            print("📂 Arquivos gerados:")
            print(f"   - KeydropBot_Desktop_v3.0.0.exe ({exe_size:.1f} MB)")
            print("   - bot-icone.ico")
            print("   - TESTAR_v3.0.0.bat")
            print()
            print("🚀 Para testar:")
            print("   1. Vá para a pasta 'dist'")
            print("   2. Execute: TESTAR_v3.0.0.bat")
            print("   3. Ou execute diretamente: KeydropBot_Desktop_v3.0.0.exe")
            
            return True
        else:
            print("❌ Executável não foi gerado!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no build: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if not success:
        print("\n❌ Build falhou!")
        print("💡 Possíveis soluções:")
        print("   - Verificar se todas as dependências estão instaladas")
        print("   - pip install -r requirements.txt")
        print("   - Verificar se o arquivo keydrop_bot_desktop.py existe")
        input("\nPressione Enter para sair...")
    else:
        print("\n✅ Build v3.0.0 concluído com sucesso!")
        input("\nPressione Enter para sair...")
