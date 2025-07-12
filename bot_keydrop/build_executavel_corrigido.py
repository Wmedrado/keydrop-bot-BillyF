#!/usr/bin/env python3
"""
Script para compilar o Keydrop Bot v3.0.0 CORRIGIDO
Gera executável com todas as correções aplicadas
"""

import PyInstaller.__main__
import os
import shutil

def build_executable():
    """Compilar executável corrigido"""
    print("🔨 Compilando Keydrop Bot Professional v3.0.0 CORRIGIDO...")
    
    # Configurações do build
    script_name = "keydrop_bot_desktop.py"
    exe_name = "KeydropBot_v3.0.0_CORRIGIDO"
    
    # Verificar se o arquivo principal existe
    if not os.path.exists(script_name):
        print(f"❌ Erro: {script_name} não encontrado!")
        return False
    
    # Limpar builds anteriores
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Argumentos do PyInstaller
    args = [
        script_name,
        '--onefile',  # Executável único
        '--windowed',  # Sem console
        f'--name={exe_name}',
        '--icon=bot-icone.ico',
        '--add-data=bot-icone.ico;.',
        '--add-data=config.json;.',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=psutil',
        '--hidden-import=requests',
        '--hidden-import=threading',
        '--hidden-import=subprocess',
        '--hidden-import=json',
        '--hidden-import=time',
        '--hidden-import=datetime',
        '--hidden-import=pathlib',
        '--hidden-import=os',
        '--hidden-import=sys',
        '--hidden-import=shutil',
        '--hidden-import=zipfile',
        '--hidden-import=webbrowser',
        '--hidden-import=urllib.parse',
        '--hidden-import=logging',
        '--hidden-import=traceback',
        '--distpath=dist',
        '--workpath=build',
        '--clean',
        '--noconfirm'
    ]
    
    print("📦 Iniciando compilação...")
    print(f"📄 Script: {script_name}")
    print(f"🎯 Executável: {exe_name}.exe")
    
    try:
        # Executar PyInstaller
        PyInstaller.__main__.run(args)
        
        # Verificar se foi criado
        exe_path = f"dist/{exe_name}.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"✅ Executável criado com sucesso!")
            print(f"📍 Local: {os.path.abspath(exe_path)}")
            print(f"📊 Tamanho: {size_mb:.1f} MB")
            
            # Copiar ícone para o diretório dist
            if os.path.exists("bot-icone.ico"):
                shutil.copy2("bot-icone.ico", "dist/")
                print("🎨 Ícone copiado para dist/")
            
            # Copiar config para o diretório dist
            if os.path.exists("config.json"):
                shutil.copy2("config.json", "dist/")
                print("⚙️ Config copiado para dist/")
            
            return True
        else:
            print("❌ Erro: Executável não foi criado!")
            return False
            
    except Exception as e:
        print(f"❌ Erro na compilação: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Build Script - Keydrop Bot v3.0.0 CORRIGIDO")
    print("=" * 50)
    
    # Verificar dependências
    try:
        import PyInstaller
        print(f"✅ PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller não instalado!")
        print("💡 Execute: pip install pyinstaller")
        return
    
    # Verificar arquivos necessários
    required_files = ["keydrop_bot_desktop.py", "bot-icone.ico"]
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"⚠️ {file} (opcional)")
    
    print("=" * 50)
    
    # Compilar
    if build_executable():
        print("\n🎉 BUILD CONCLUÍDO COM SUCESSO!")
        print("🔥 Executável corrigido pronto para uso!")
        print("\n📋 Próximos passos:")
        print("1. Navegue até a pasta 'dist'")
        print("2. Execute KeydropBot_v3.0.0_CORRIGIDO.exe")
        print("3. Teste todas as funcionalidades")
    else:
        print("\n❌ FALHA NO BUILD!")
        print("🔧 Verifique os erros acima")

if __name__ == "__main__":
    main()
