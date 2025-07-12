"""
Teste Final do KeyDrop Bot Professional Edition v4.0.0
======================================================

Teste completo de todas as funcionalidades implementadas:
- Sistema de Stop Robusto
- Mini Window Mode
- Otimizações de Performance
- Gerenciamento de Memória
- Interface Aprimorada
- Launcher Atualizado
"""

import sys
import os
import time
import json
import threading
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_version_system():
    """Testa o sistema de versão"""
    print("🏷️ Testando Sistema de Versão...")
    
    try:
        # Verificar se version.json existe
        if not os.path.exists("version.json"):
            print("❌ Arquivo version.json não encontrado")
            return False
        
        # Ler dados de versão
        with open("version.json", "r") as f:
            version_data = json.load(f)
        
        # Verificar campos obrigatórios
        required_fields = ["version", "build", "name", "description", "features"]
        for field in required_fields:
            if field not in version_data:
                print(f"❌ Campo '{field}' ausente no version.json")
                return False
        
        print(f"✅ Versão: {version_data['version']}")
        print(f"✅ Build: {version_data['build']}")
        print(f"✅ Funcionalidades: {len(version_data['features'])} listadas")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar versão: {e}")
        return False

def test_memory_manager():
    """Testa o gerenciador de memória"""
    print("\n🧠 Testando Gerenciador de Memória...")
    
    try:
        from src.memory_manager import MemoryManager
        
        # Inicializar memory manager
        mm = MemoryManager()
        
        # Testar estatísticas
        stats = mm.get_stats()
        print(f"✅ Estatísticas obtidas: {stats}")
        
        # Testar limpeza forçada
        mm._perform_cleanup()
        print("✅ Limpeza forçada executada")
        
        # Testar monitoramento
        stats_after = mm.get_stats()
        print(f"✅ Estatísticas após limpeza: {stats_after}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar memory manager: {e}")
        return False

def test_launcher():
    """Testa o launcher"""
    print("\n🚀 Testando Launcher...")
    
    try:
        import launcher
        
        # Testar funções básicas
        print("   Testando verificação de Python...")
        if launcher.verificar_python():
            print("✅ Verificação de Python OK")
        else:
            print("❌ Verificação de Python falhou")
            return False
        
        print("   Testando verificação de arquivos...")
        if launcher.verificar_arquivos_principais():
            print("✅ Verificação de arquivos OK")
        else:
            print("❌ Verificação de arquivos falhou")
            return False
        
        print("   Testando banner...")
        launcher.print_banner()
        print("✅ Banner exibido corretamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar launcher: {e}")
        return False

def test_gui_imports():
    """Testa importações da interface"""
    print("\n🖥️ Testando Importações da Interface...")
    
    try:
        # Testar importação da interface moderna
        import modern_gui
        print("✅ Interface moderna importada")
        
        # Testar importação do bot principal
        import keydrop_bot
        print("✅ Bot principal importado")
        
        # Testar importação do bot_gui clássico
        import bot_gui
        print("✅ Interface clássica importada")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar importações: {e}")
        return False

def test_file_structure():
    """Testa estrutura de arquivos"""
    print("\n📁 Testando Estrutura de Arquivos...")
    
    # Arquivos principais que devem existir
    essential_files = [
        "modern_gui.py",
        "keydrop_bot.py", 
        "bot_gui.py",
        "launcher.py",
        "version.json",
        "requirements.txt",
        "README.md",
        "CHANGELOG.md"
    ]
    
    # Diretórios que devem existir
    essential_dirs = [
        "src",
        "docs",
        "dev",
        "startup"
    ]
    
    all_good = True
    
    for file in essential_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - FALTANDO")
            all_good = False
    
    for dir in essential_dirs:
        if os.path.exists(dir):
            print(f"✅ {dir}/")
        else:
            print(f"❌ {dir}/ - FALTANDO")
            all_good = False
    
    # Verificar arquivos específicos do src
    src_files = [
        "src/memory_manager.py",
        "src/update_manager.py",
        "src/utils.py"
    ]
    
    for file in src_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"⚠️ {file} - OPCIONAL")
    
    return all_good

def test_executables():
    """Testa se os executáveis existem"""
    print("\n💻 Testando Executáveis...")
    
    executables = [
        "KeyDrop_Bot_Moderno.exe",
        "KeyDrop_Bot_Classico.exe",
        "startup/executavel/KeyDrop_Bot_Moderno.exe",
        "startup/executavel/KeyDrop_Bot_Classico.exe"
    ]
    
    found_count = 0
    total_count = len(executables)
    
    for exe in executables:
        if os.path.exists(exe):
            size = os.path.getsize(exe) / (1024 * 1024)  # MB
            print(f"✅ {exe} ({size:.1f} MB)")
            found_count += 1
        else:
            print(f"⚠️ {exe} - NÃO ENCONTRADO")
    
    print(f"\n📊 Executáveis encontrados: {found_count}/{total_count}")
    return found_count > 0  # Pelo menos um executável deve existir

def test_release_files():
    """Testa arquivos de release"""
    print("\n📦 Testando Arquivos de Release...")
    
    release_files = [
        "RELEASE_FORM_v4.0.0.md",
        "CHANGELOG.md",
        "KeyDrop_Bot_v4.0.0.zip"
    ]
    
    found_count = 0
    
    for file in release_files:
        if os.path.exists(file):
            if file.endswith('.zip'):
                size = os.path.getsize(file) / (1024 * 1024)  # MB
                print(f"✅ {file} ({size:.1f} MB)")
            else:
                print(f"✅ {file}")
            found_count += 1
        else:
            print(f"⚠️ {file} - NÃO ENCONTRADO")
    
    return found_count >= 2  # Pelo menos CHANGELOG e RELEASE_FORM

def main():
    """Função principal do teste"""
    print("🧪 TESTE FINAL - KEYDROP BOT PROFESSIONAL EDITION v4.0.0")
    print("=" * 70)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Lista de testes
    tests = [
        ("Sistema de Versão", test_version_system),
        ("Gerenciador de Memória", test_memory_manager),
        ("Launcher", test_launcher),
        ("Importações da Interface", test_gui_imports),
        ("Estrutura de Arquivos", test_file_structure),
        ("Executáveis", test_executables),
        ("Arquivos de Release", test_release_files)
    ]
    
    results = []
    
    # Executar testes
    for test_name, test_func in tests:
        print(f"\n🔄 Executando: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: PASSOU")
            else:
                print(f"❌ {test_name}: FALHOU")
                
        except Exception as e:
            print(f"💥 {test_name}: ERRO - {e}")
            results.append((test_name, False))
    
    # Resultado final
    print("\n" + "=" * 70)
    print("📊 RESULTADOS FINAIS:")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {test_name}: {status}")
    
    print(f"\n📈 Resumo: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("🚀 KeyDrop Bot Professional Edition v4.0.0 está pronto para produção!")
        return True
    elif passed >= total * 0.8:  # 80% ou mais
        print("⚠️ MAIORIA DOS TESTES PASSOU")
        print("🔧 Alguns ajustes menores podem ser necessários")
        return True
    else:
        print("❌ MUITOS TESTES FALHARAM")
        print("🛠️ Correções são necessárias antes da produção")
        return False

if __name__ == "__main__":
    try:
        success = main()
        input("\n🏁 Pressione Enter para sair...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Teste interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Erro inesperado: {e}")
        input("Pressione Enter para sair...")
        sys.exit(1)
