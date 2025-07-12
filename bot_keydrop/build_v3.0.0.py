#!/usr/bin/env python3
"""
Script de Build para Keydrop Bot Professional v3.0.0
Gera executável otimizado com ícone personalizado
"""

import subprocess
import sys
import os
import shutil

def build_executable():
    """Construir executável v3.0.0 otimizado"""
    print("🔨 Iniciando build do Keydrop Bot Professional v3.0.0...")
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print(f"✅ PyInstaller encontrado: versão {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller instalado com sucesso!")
    
    # Verificar arquivos necessários
    script_file = "keydrop_bot_desktop.py"
    icon_file = "bot-icone.ico"
    
    if not os.path.exists(script_file):
        print(f"❌ Arquivo principal não encontrado: {script_file}")
        return False
    
    if not os.path.exists(icon_file):
        print(f"⚠️ Ícone não encontrado: {icon_file}")
        print("   O executável será criado sem ícone personalizado")
        icon_file = None
    else:
        print(f"✅ Ícone encontrado: {icon_file}")
    
    # Limpar build anterior
    build_dirs = ["build", "dist", "__pycache__"]
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            print(f"🧹 Limpando diretório: {dir_name}")
            shutil.rmtree(dir_name)
    
    # Limpar arquivos .spec anteriores
    spec_files = [f for f in os.listdir(".") if f.endswith(".spec")]
    for spec_file in spec_files:
        print(f"🧹 Removendo spec antigo: {spec_file}")
        os.remove(spec_file)
    
    # Configurar comando do PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Arquivo único
        "--windowed",  # Interface gráfica (sem console)
        "--name", "KeydropBot_Desktop_v3.0.0",  # Nome do executável
        "--clean",  # Limpeza antes do build
        "--noconfirm",  # Não pedir confirmação
    ]
    
    # Adicionar ícone se disponível
    if icon_file:
        cmd.extend(["--icon", icon_file])
        # Também adicionar como dados para garantir que seja incluído
        cmd.extend(["--add-data", f"{icon_file};."])
    
    # Adicionar metadados do Windows
    if os.name == 'nt':
        cmd.extend([
            "--version-file", "version_info.txt"  # Se houver arquivo de versão
        ])
    
    # Otimizações adicionais
    cmd.extend([
        "--optimize", "2",  # Otimização Python
        "--strip",  # Remover símbolos de debug
        "--upx-dir", "upx" if shutil.which("upx") else "",  # Compressão UPX se disponível
    ])
    
    # Filtrar argumentos vazios
    cmd = [arg for arg in cmd if arg]
    
    # Adicionar arquivo principal
    cmd.append(script_file)
    
    print("🚀 Executando PyInstaller...")
    print(f"📋 Comando: {' '.join(cmd[:5])}... (simplificado)")
    
    try:
        # Executar build
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ Build concluído com sucesso!")
            
            # Verificar se executável foi criado
            exe_name = "KeydropBot_Desktop_v3.0.0.exe"
            exe_path = os.path.join("dist", exe_name)
            
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                print(f"🎉 Executável criado: {exe_path}")
                print(f"📏 Tamanho: {file_size:.1f} MB")
                
                # Testar se executável abre
                print("🧪 Testando executável...")
                test_result = subprocess.run([exe_path, "--version"], 
                                           capture_output=True, text=True, timeout=10)
                
                if test_result.returncode == 0:
                    print("✅ Executável testado com sucesso!")
                else:
                    print("⚠️ Aviso: Executável criado, mas teste falhou")
                
                return True
            else:
                print("❌ Executável não foi criado no local esperado")
                return False
        else:
            print("❌ Erro durante o build:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro inesperado durante build: {e}")
        return False

def create_version_info():
    """Criar arquivo de informações de versão para Windows"""
    version_content = """
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(3, 0, 0, 0),
    prodvers=(3, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'William Medrado'),
        StringStruct(u'FileDescription', u'Keydrop Bot Professional'),
        StringStruct(u'FileVersion', u'3.0.0'),
        StringStruct(u'InternalName', u'KeydropBot'),
        StringStruct(u'LegalCopyright', u'Copyright © 2025 William Medrado'),
        StringStruct(u'OriginalFilename', u'KeydropBot_Desktop_v3.0.0.exe'),
        StringStruct(u'ProductName', u'Keydrop Bot Professional'),
        StringStruct(u'ProductVersion', u'3.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    try:
        with open("version_info.txt", "w", encoding="utf-8") as f:
            f.write(version_content)
        print("✅ Arquivo de versão criado")
    except Exception as e:
        print(f"⚠️ Erro ao criar arquivo de versão: {e}")

def main():
    """Função principal do build"""
    print("=" * 60)
    print("🤖 KEYDROP BOT PROFESSIONAL v3.0.0 - BUILD SCRIPT")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("keydrop_bot_desktop.py"):
        print("❌ Execute este script no diretório do projeto!")
        return
    
    # Criar arquivo de versão
    create_version_info()
    
    # Executar build
    success = build_executable()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 BUILD CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print("📁 Executável localizado em: dist/KeydropBot_Desktop_v3.0.0.exe")
        print("🚀 O app está pronto para distribuição!")
        print("=" * 60)
        
        # Instruções finais
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Teste o executável manualmente")
        print("2. Verifique se o ícone aparece corretamente")
        print("3. Teste a automação do Chrome")
        print("4. Distribua o arquivo .exe")
        
    else:
        print("\n" + "=" * 60)
        print("❌ BUILD FALHOU!")
        print("=" * 60)
        print("🔧 Verifique os erros acima e tente novamente")

if __name__ == "__main__":
    main()
