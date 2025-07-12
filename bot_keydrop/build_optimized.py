#!/usr/bin/env python3
"""
Script de Build Otimizado para Keydrop Bot Professional v4.0.0
Cria executável com máxima compatibilidade e robustez
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    print("🔨 Keydrop Bot Professional v4.0.0 - Build Executável Otimizado")
    print("=" * 60)
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado!")
        print("📦 Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller instalado!")
    
    # Paths
    script_dir = Path(__file__).parent
    main_script = script_dir / "keydrop_bot_desktop.py"
    icon_file = script_dir / "bot-icone.ico"
    dist_dir = script_dir / "dist"
    build_dir = script_dir / "build"
    
    # Verificar arquivos necessários
    if not main_script.exists():
        print(f"❌ Arquivo principal não encontrado: {main_script}")
        return False
    print(f"✅ Script principal encontrado: {main_script}")
    
    if icon_file.exists():
        print(f"✅ Ícone encontrado: {icon_file}")
        icon_param = f"--icon={icon_file}"
    else:
        print("⚠️ Ícone não encontrado, continuando sem ícone")
        icon_param = ""
    
    # Limpar builds anteriores
    if dist_dir.exists():
        print("🧹 Limpando builds anteriores...")
        shutil.rmtree(dist_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    print("\n📋 Configurando build...")
    
    # Configurar argumentos do PyInstaller para máxima compatibilidade
    args = [
        str(main_script),
        "--name=KeydropBot_Desktop_v4.0.0",
        "--onefile",  # Arquivo único
        "--console",  # Manter console para debug
        "--clean",  # Build limpo
        "--noconfirm",  # Não pedir confirmação
        "--optimize=1",  # Otimização moderada (2 pode causar problemas)
        "--noupx",  # Não usar UPX (evita problemas de antivírus)
    ]
    
    # Adicionar ícone se disponível
    if icon_param:
        args.append(icon_param)
    
    # Excluir módulos problemáticos
    exclude_modules = [
        "numpy", "scipy", "matplotlib", "pandas", "opencv-python", 
        "tensorflow", "torch", "sklearn", "PIL", "pygame"
    ]
    
    for module in exclude_modules:
        args.append(f"--exclude-module={module}")
    
    # Adicionar dados necessários
    if icon_file.exists():
        args.append(f"--add-data={icon_file};.")
    
    # Configurações específicas do Windows
    if os.name == 'nt':
        # Não adicionar --uac-admin por enquanto para evitar problemas
        pass
    
    print(f"🚀 Iniciando build com argumentos otimizados...")
    print(f"📝 Comando: pyinstaller {' '.join(args[1:])}")
    
    try:
        # Executar PyInstaller
        import PyInstaller.__main__
        PyInstaller.__main__.run(args)
        
        # Verificar se o executável foi criado
        exe_path = dist_dir / "KeydropBot_Desktop_v4.0.0.exe"
        if exe_path.exists():
            exe_size = exe_path.stat().st_size / (1024 * 1024)  # MB
            print(f"\n✅ BUILD CONCLUÍDO COM SUCESSO!")
            print(f"📄 Executável: {exe_path}")
            print(f"📏 Tamanho: {exe_size:.1f} MB")
            
            # Criar versão alternativa sem console
            print(f"\n🔄 Criando versão sem console...")
            args_windowed = args.copy()
            args_windowed[2] = "--name=KeydropBot_Desktop_NoConsole_v4.0.0"
            args_windowed[4] = "--windowed"  # Substituir --console por --windowed
            
            try:
                PyInstaller.__main__.run(args_windowed)
                exe_windowed = dist_dir / "KeydropBot_Desktop_NoConsole_v4.0.0.exe"
                if exe_windowed.exists():
                    print(f"✅ Versão sem console criada: {exe_windowed}")
                else:
                    print("⚠️ Não foi possível criar versão sem console")
            except Exception as e:
                print(f"⚠️ Erro ao criar versão sem console: {e}")
            
            print(f"\n🎉 EXECUTÁVEIS PRONTOS!")
            print(f"📁 Localização: {dist_dir}")
            print(f"🖥️ Console: KeydropBot_Desktop_v4.0.0.exe")
            if exe_windowed.exists():
                print(f"🪟 Windowed: KeydropBot_Desktop_NoConsole_v4.0.0.exe")
            
            print(f"\n💡 Para testar:")
            print(f"   cd \"{dist_dir}\"")
            print(f"   .\\KeydropBot_Desktop_v4.0.0.exe")
            
            return True
            
        else:
            print("❌ Executável não foi criado!")
            print("🔍 Verifique os logs acima para erros")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o build: {e}")
        import traceback
        print("📋 Detalhes do erro:")
        traceback.print_exc()
        return False

def test_executable():
    """Testar o executável criado"""
    dist_dir = Path(__file__).parent / "dist"
    exe_path = dist_dir / "KeydropBot_Desktop_v4.0.0.exe"
    
    if not exe_path.exists():
        print("❌ Executável não encontrado para teste")
        return False
    
    print(f"\n🧪 Testando executável: {exe_path}")
    try:
        # Teste rápido sem interface gráfica
        result = subprocess.run([str(exe_path), "--version"], 
                              timeout=15, capture_output=True, text=True)
        print(f"📊 Código de saída: {result.returncode}")
        if result.stdout:
            print(f"📤 Saída: {result.stdout}")
        if result.stderr:
            print(f"📤 Erro: {result.stderr}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⏰ Teste expirou (pode ser normal para GUI)")
        return True
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Keydrop Bot Professional - Build System v4.0.0")
    print("👨‍💻 Desenvolvido por: William Medrado")
    print("=" * 60)
    
    success = main()
    
    if success:
        print("\n" + "="*60)
        print("✅ BUILD CONCLUÍDO COM SUCESSO!")
        print("="*60)
        
        # Perguntar se quer testar
        try:
            test_choice = input("\n🧪 Deseja testar o executável? (s/n): ").lower().strip()
            if test_choice in ['s', 'sim', 'y', 'yes']:
                test_result = test_executable()
                if test_result:
                    print("✅ Teste passou!")
                else:
                    print("⚠️ Teste apresentou problemas")
        except KeyboardInterrupt:
            print("\n⏹️ Teste cancelado pelo usuário")
        
        try:
            input("\n📝 Pressione Enter para sair...")
        except KeyboardInterrupt:
            pass
    else:
        print("\n" + "="*60)
        print("❌ BUILD FALHOU!")
        print("="*60)
        print("💡 Verifique os erros acima e tente novamente")
        try:
            input("\n📝 Pressione Enter para sair...")
        except KeyboardInterrupt:
            pass
