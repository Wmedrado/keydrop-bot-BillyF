"""
Teste do Sistema de Atualização v2.0.6
======================================

Testa se o sistema de atualização está funcionando corretamente.
"""

import sys
import os
import time
from datetime import datetime

# Adicionar o diretório raiz ao path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.improved_update_manager import ImprovedUpdateManager

def test_update_check():
    """Testa a verificação de atualizações"""
    print("🔍 Testando Sistema de Atualização...")
    print("=" * 50)
    
    # Simular versão mais antiga para testar
    update_manager = ImprovedUpdateManager(
        repo_owner="wmedrado",
        repo_name="bot-keydrop", 
        current_version="2.0.5"  # Versão anterior para testar
    )
    
    print(f"📋 Versão atual configurada: {update_manager.current_version}")
    print(f"🌐 Repositório: {update_manager.repo_owner}/{update_manager.repo_name}")
    print(f"🔑 Token configurado: {'✅ Sim' if update_manager.github_token else '❌ Não'}")
    
    try:
        # Verificar atualizações
        print("\n🔄 Verificando atualizações...")
        update_info = update_manager.check_for_updates()
        
        print(f"📊 Resultado da verificação:")
        print(f"   - Disponível: {update_info.get('available', False)}")
        
        if update_info.get('available'):
            print(f"   - Nova versão: {update_info.get('version', 'N/A')}")
            print(f"   - URL de download: {update_info.get('download_url', 'N/A')}")
            print(f"   - Nome do arquivo: {update_info.get('asset_name', 'N/A')}")
            print(f"   - Tamanho: {update_info.get('asset_size', 0)} bytes")
            
            if update_info.get('download_url'):
                print("✅ Sistema de atualização funcionando corretamente!")
                return True
            else:
                print("❌ URL de download não encontrada!")
                return False
        else:
            if update_info.get('error'):
                print(f"❌ Erro: {update_info.get('error')}")
                return False
            else:
                print(f"ℹ️ Mensagem: {update_info.get('message', 'N/A')}")
                return True
                
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

def test_version_comparison():
    """Testa a comparação de versões"""
    print("\n🔢 Testando Comparação de Versões...")
    print("=" * 50)
    
    update_manager = ImprovedUpdateManager()
    
    # Casos de teste
    test_cases = [
        ("2.0.6", "2.0.5", True),   # Nova versão disponível
        ("2.0.5", "2.0.6", False),  # Versão atual é mais nova
        ("2.0.6", "2.0.6", False),  # Versões iguais
        ("2.1.0", "2.0.6", True),   # Versão minor nova
        ("3.0.0", "2.0.6", True),   # Versão major nova
    ]
    
    all_passed = True
    
    for latest, current, expected in test_cases:
        result = update_manager.is_newer_version(latest, current)
        status = "✅" if result == expected else "❌"
        print(f"   {status} {latest} > {current}: {result} (esperado: {expected})")
        
        if result != expected:
            all_passed = False
    
    return all_passed

def test_token_detection():
    """Testa a detecção do token do GitHub"""
    print("\n🔑 Testando Detecção de Token...")
    print("=" * 50)
    
    update_manager = ImprovedUpdateManager()
    
    if update_manager.github_token:
        print("✅ Token do GitHub detectado com sucesso!")
        print(f"🔐 Token (primeiros 10 caracteres): {update_manager.github_token[:10]}...")
        return True
    else:
        print("❌ Token do GitHub não detectado!")
        print("📝 Verifique se o arquivo 'github_token.txt' existe no diretório raiz")
        return False

def main():
    """Função principal do teste"""
    print("🧪 TESTE DO SISTEMA DE ATUALIZAÇÃO v2.0.6")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Lista de testes
    tests = [
        ("Detecção de Token", test_token_detection),
        ("Comparação de Versões", test_version_comparison),
        ("Verificação de Atualizações", test_update_check)
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
        print("🎉 SISTEMA DE ATUALIZAÇÃO FUNCIONANDO PERFEITAMENTE!")
        print("🚀 Usuários podem atualizar automaticamente para v2.0.6!")
        return True
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("🔧 Correções necessárias no sistema de atualização")
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
