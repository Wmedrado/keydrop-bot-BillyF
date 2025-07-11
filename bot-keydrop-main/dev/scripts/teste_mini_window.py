"""
Teste do sistema de Mini Window
===============================

Testa se a funcionalidade de janelas pequenas (200x300) está funcionando corretamente.
"""

import sys
import os
import time
import threading
import json
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from keydrop_bot import KeyDropBot
from src.memory_manager import MemoryManager

def test_mini_window_mode():
    """Testa o modo mini window"""
    print("🧪 Testando Mini Window Mode...")
    print("=" * 50)
    
    # Configuração de teste
    profile_path = "profiles/test_mini_window"
    bot_id = "test_mini_1"
    
    try:
        # Criar diretório de perfil se não existir
        os.makedirs(profile_path, exist_ok=True)
        
        # Inicializar o bot
        bot = KeyDropBot(profile_path, bot_id, headless=False, mini_window=True)
        
        # Testar criação de driver com mini window
        print("\n1. Testando criação de driver com Mini Window...")
        driver = bot.criar_driver()
        
        if driver:
            print("✅ Driver criado com sucesso")
            
            # Verificar tamanho da janela
            size = driver.get_window_size()
            print(f"📏 Tamanho da janela: {size['width']}x{size['height']}")
            
            if size['width'] <= 250 and size['height'] <= 350:
                print("✅ Mini Window configurado corretamente")
            else:
                print("⚠️ Mini Window pode não estar funcionando corretamente")
            
            # Testar navegação
            print("\n2. Testando navegação...")
            driver.get("https://key-drop.com/pt/giveaways")
            time.sleep(3)
            
            current_url = driver.current_url
            print(f"🌐 URL atual: {current_url}")
            
            if "key-drop.com" in current_url:
                print("✅ Navegação funcionando")
            else:
                print("⚠️ Problema na navegação")
            
            # Fechar driver
            driver.quit()
            print("✅ Driver fechado com sucesso")
            
        else:
            print("❌ Falha ao criar driver")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False
    
    return True

def test_mini_window_vs_normal():
    """Compara Mini Window com modo normal"""
    print("\n🔍 Comparando Mini Window vs Normal...")
    print("=" * 50)
    
    # Configuração de teste
    profile_path = "profiles/test_comparison"
    
    try:
        # Criar diretório de perfil se não existir
        os.makedirs(profile_path, exist_ok=True)
        
        # Teste modo normal
        print("\n1. Testando modo normal...")
        bot_normal = KeyDropBot(profile_path, "test_normal", headless=False, mini_window=False)
        driver_normal = bot_normal.criar_driver()
        
        if driver_normal:
            size_normal = driver_normal.get_window_size()
            print(f"📏 Tamanho normal: {size_normal['width']}x{size_normal['height']}")
            driver_normal.quit()
        
        # Teste modo mini
        print("\n2. Testando modo mini...")
        bot_mini = KeyDropBot(profile_path, "test_mini", headless=False, mini_window=True)
        driver_mini = bot_mini.criar_driver()
        
        if driver_mini:
            size_mini = driver_mini.get_window_size()
            print(f"📏 Tamanho mini: {size_mini['width']}x{size_mini['height']}")
            driver_mini.quit()
        
        # Comparação
        if driver_normal and driver_mini:
            print("\n📊 Comparação:")
            print(f"   Normal: {size_normal['width']}x{size_normal['height']}")
            print(f"   Mini:   {size_mini['width']}x{size_mini['height']}")
            
            # Verificar se mini é realmente menor
            if (size_mini['width'] < size_normal['width'] and 
                size_mini['height'] < size_normal['height']):
                print("✅ Mini Window funcionando corretamente")
                return True
            else:
                print("⚠️ Mini Window pode não estar reduzindo o tamanho")
                return False
        
    except Exception as e:
        print(f"❌ Erro durante comparação: {e}")
        return False
    
    return True

def test_mini_window_performance():
    """Testa performance do Mini Window"""
    print("\n⚡ Testando Performance do Mini Window...")
    print("=" * 50)
    
    # Inicializar gerenciador de memória
    memory_manager = MemoryManager()
    
    # Configuração para teste de performance
    profile_path = "profiles/test_performance"
    bot_id = "test_perf_1"
    
    try:
        # Criar diretório de perfil se não existir
        os.makedirs(profile_path, exist_ok=True)
        
        # Monitorar memória inicial
        initial_stats = memory_manager.get_stats()
        initial_memory = initial_stats['current_memory']
        print(f"🧠 Memória inicial: {initial_memory:.2f} MB")
        
        # Criar bot
        bot = KeyDropBot(profile_path, bot_id, headless=False, mini_window=True)
        
        # Medir tempo de criação
        start_time = time.time()
        driver = bot.criar_driver()
        creation_time = time.time() - start_time
        
        print(f"⏱️ Tempo de criação: {creation_time:.2f}s")
        
        if driver:
            # Navegar para página
            start_nav = time.time()
            driver.get("https://key-drop.com/pt/giveaways")
            nav_time = time.time() - start_nav
            
            print(f"🌐 Tempo de navegação: {nav_time:.2f}s")
            
            # Monitorar memória após navegação
            current_stats = memory_manager.get_stats()
            current_memory = current_stats['current_memory']
            print(f"🧠 Memória após navegação: {current_memory:.2f} MB")
            print(f"📈 Incremento: {current_memory - initial_memory:.2f} MB")
            
            # Aguardar um pouco
            time.sleep(5)
            
            # Fechar driver
            driver.quit()
            
            # Verificar limpeza de memória
            time.sleep(2)
            final_stats = memory_manager.get_stats()
            final_memory = final_stats['current_memory']
            print(f"🧠 Memória final: {final_memory:.2f} MB")
            print(f"🧹 Limpeza: {current_memory - final_memory:.2f} MB")
            
            # Verificar se há otimização
            if creation_time < 5 and nav_time < 10:
                print("✅ Performance aceitável")
                return True
            else:
                print("⚠️ Performance pode ser melhorada")
                return False
        
    except Exception as e:
        print(f"❌ Erro durante teste de performance: {e}")
        return False
    
    return True

def main():
    """Função principal do teste"""
    print("🧪 TESTE DO SISTEMA MINI WINDOW")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Lista de testes
    tests = [
        ("Mini Window Mode", test_mini_window_mode),
        ("Mini vs Normal", test_mini_window_vs_normal),
        ("Performance", test_mini_window_performance)
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
    print("\n" + "=" * 60)
    print("📊 RESULTADOS FINAIS:")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {test_name}: {status}")
    
    print(f"\n📈 Resumo: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram!")
        return True
    else:
        print("⚠️ Alguns testes falharam")
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
