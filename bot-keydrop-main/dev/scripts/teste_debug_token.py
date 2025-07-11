#!/usr/bin/env python3
"""
Script de Debug para Token do GitHub
Testa diferentes cenários de carregamento do token
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def debug_token():
    """Debug detalhado do carregamento do token"""
    print("🔍 DEBUG: Carregamento do Token do GitHub")
    print("=" * 60)
    
    # Informações do ambiente
    print(f"📁 Diretório atual: {os.getcwd()}")
    print(f"📁 Diretório do script: {Path(__file__).parent}")
    print(f"📁 Diretório raiz do projeto: {project_root}")
    print(f"🐍 Python path: {sys.path[:3]}...")
    print()
    
    # Verificar arquivo github_token.txt
    token_file = project_root / 'github_token.txt'
    print(f"📄 Arquivo de token: {token_file}")
    print(f"✅ Arquivo existe: {token_file.exists()}")
    
    if token_file.exists():
        try:
            token_content = token_file.read_text(encoding='utf-8')
            print(f"📝 Conteúdo do arquivo: '{token_content[:20]}...' (total: {len(token_content)} chars)")
            token_clean = token_content.strip()
            print(f"🧹 Token limpo: '{token_clean[:20]}...' (total: {len(token_clean)} chars)")
            print(f"✅ Token não está vazio: {bool(token_clean)}")
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")
    print()
    
    # Testar importação
    try:
        from src.private_update_manager import PrivateUpdateManager
        print("✅ Importação da PrivateUpdateManager: OK")
        
        # Testar instanciação
        mgr = PrivateUpdateManager()
        print(f"✅ Instanciação: OK")
        print(f"🔑 Token configurado: {bool(mgr.github_token)}")
        
        if mgr.github_token:
            print(f"🔑 Token (primeiros 10 chars): {mgr.github_token[:10]}...")
            print(f"🔑 Token (últimos 10 chars): ...{mgr.github_token[-10:]}")
            print(f"📏 Tamanho do token: {len(mgr.github_token)} chars")
            
            # Testar headers
            print(f"🌐 Headers configurados: {bool(mgr.headers)}")
            if mgr.headers:
                auth_header = mgr.headers.get('Authorization', '')
                print(f"🔐 Authorization header: {auth_header[:20]}...")
        else:
            print("❌ Token não foi carregado!")
            
    except Exception as e:
        print(f"❌ Erro na importação/instanciação: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("🔍 Testando verificação de atualizações...")
    try:
        from src.private_update_manager import PrivateUpdateManager
        mgr = PrivateUpdateManager()
        
        # Testar check_for_updates
        print("⏳ Executando check_for_updates()...")
        result = mgr.check_for_updates()
        
        print(f"📊 Resultado: {result}")
        
        if result.get("error"):
            print(f"❌ Erro encontrado: {result['error']}")
        else:
            print("✅ Verificação executada sem erros")
            
    except Exception as e:
        print(f"❌ Erro no teste de verificação: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_token()
