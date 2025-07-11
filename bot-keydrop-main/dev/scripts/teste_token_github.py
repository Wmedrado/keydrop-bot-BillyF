#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a configuração do token do GitHub
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def testar_token_github():
    """Testa se o token do GitHub está configurado corretamente"""
    
    print("=" * 60)
    print("TESTE DE CONFIGURAÇÃO DO TOKEN GITHUB")
    print("=" * 60)
    
    # Importar PrivateUpdateManager
    sys.path.append('..')
    from src.private_update_manager import PrivateUpdateManager
    
    # Criar instância
    update_manager = PrivateUpdateManager()
    
    print(f"Repositório: {update_manager.repo_owner}/{update_manager.repo_name}")
    print(f"Versão atual: {update_manager.current_version}")
    print(f"Token configurado: {'✅ Sim' if update_manager.github_token else '❌ Não'}")
    
    if update_manager.github_token:
        # Mascarar o token para segurança
        token_masked = update_manager.github_token[:8] + "*" * (len(update_manager.github_token) - 12) + update_manager.github_token[-4:]
        print(f"Token (mascarado): {token_masked}")
        
        # Testar verificação de atualizações
        print("\n🔍 Testando verificação de atualizações...")
        try:
            result = update_manager.check_for_updates()
            print(f"Resultado: {result}")
            
            if result.get('error'):
                print(f"❌ Erro: {result['error']}")
            elif result.get('available'):
                print(f"✅ Atualização disponível: v{result['version']}")
            else:
                print("✅ Nenhuma atualização disponível")
                
        except Exception as e:
            print(f"❌ Erro durante verificação: {e}")
    
    else:
        print("\n❌ Token não encontrado!")
        print("📝 Soluções:")
        print("1. Criar arquivo 'github_token.txt' na raiz do projeto")
        print("2. Definir variável de ambiente GITHUB_TOKEN")
        print("3. Adicionar 'github_token' no bot_config.json")
    
    return True

def verificar_arquivos():
    """Verifica se os arquivos necessários existem"""
    
    print("\n" + "=" * 60)
    print("VERIFICAÇÃO DE ARQUIVOS")
    print("=" * 60)
    
    # Obter diretório raiz do projeto
    project_root = Path(__file__).parent.parent
    
    arquivos_importantes = [
        ('github_token.txt', project_root / 'github_token.txt'),
        ('bot_config.json', project_root / 'bot_config.json'),
        ('src/private_update_manager.py', project_root / 'src' / 'private_update_manager.py')
    ]
    
    for nome, caminho in arquivos_importantes:
        existe = caminho.exists()
        print(f"{nome}: {'✅' if existe else '❌'} {caminho}")
        
        if existe and nome == 'github_token.txt':
            try:
                conteudo = caminho.read_text(encoding='utf-8').strip()
                if conteudo:
                    print(f"  Token encontrado (length: {len(conteudo)})")
                else:
                    print("  ❌ Arquivo vazio!")
            except Exception as e:
                print(f"  ❌ Erro ao ler: {e}")

def verificar_variaveis_ambiente():
    """Verifica variáveis de ambiente relacionadas"""
    
    print("\n" + "=" * 60)
    print("VERIFICAÇÃO DE VARIÁVEIS DE AMBIENTE")
    print("=" * 60)
    
    vars_importantes = ['GITHUB_TOKEN', 'PATH', 'HOME', 'USERPROFILE']
    
    for var in vars_importantes:
        valor = os.getenv(var)
        if var == 'GITHUB_TOKEN':
            if valor:
                masked = valor[:8] + "*" * (len(valor) - 12) + valor[-4:] if len(valor) > 12 else "***"
                print(f"{var}: ✅ {masked}")
            else:
                print(f"{var}: ❌ Não definida")
        else:
            print(f"{var}: {'✅' if valor else '❌'}")

if __name__ == "__main__":
    print(f"Iniciando testes: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        verificar_arquivos()
        verificar_variaveis_ambiente()
        testar_token_github()
        
        print("\n✅ TESTE CONCLUÍDO!")
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE TESTE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
