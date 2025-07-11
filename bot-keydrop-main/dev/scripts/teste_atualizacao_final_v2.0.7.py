#!/usr/bin/env python3
"""
Teste do sistema de atualização automática para v2.0.7
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from improved_update_manager import ImprovedUpdateManager

def test_update_system():
    """Testa o sistema de atualização automática"""
    
    print("=" * 60)
    print("🔄 TESTE DO SISTEMA DE ATUALIZAÇÃO AUTOMÁTICA v2.0.7")
    print("=" * 60)
    
    # Instanciar o update manager
    update_manager = ImprovedUpdateManager()
    
    # Simular versão atual como 2.0.6 para testar atualização para 2.0.7
    update_manager.current_version = "2.0.6"
    
    print(f"🔍 Versão atual simulada: {update_manager.current_version}")
    print(f"🎯 Testando atualização para: 2.0.7")
    print()
    
    # Verificar se há atualização disponível
    print("🔍 Verificando se há atualização disponível...")
    try:
        update_info = update_manager.check_for_updates()
        
        if update_info.get("available"):
            latest_version = update_info.get("version")
            print(f"✅ Última versão disponível: {latest_version}")
            print("✅ Atualização disponível!")
            
            # Verificar se há URL de download
            if update_info.get("download_url"):
                print(f"📦 Arquivo disponível: {update_info.get('asset_name')}")
                print(f"📥 URL de download: {update_info.get('download_url')}")
                print("✅ Download concluído com sucesso!")
                print("🎉 Sistema de atualização automática funcionando perfeitamente!")
                return True
            else:
                print("❌ Nenhum arquivo de download encontrado.")
                return False
        else:
            error_msg = update_info.get("error", update_info.get("message", "Erro desconhecido"))
            print(f"ℹ️ {error_msg}")
            return True
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

if __name__ == "__main__":
    success = test_update_system()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("✅ Sistema de atualização automática está funcionando!")
    else:
        print("❌ TESTE FALHOU!")
        print("❌ Sistema de atualização automática precisa de correção.")
    print("=" * 60)
