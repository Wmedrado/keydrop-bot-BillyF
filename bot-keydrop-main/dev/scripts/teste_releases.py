#!/usr/bin/env python3
"""
Script para testar acesso às releases do repositório
"""

import os
import sys
import requests
from pathlib import Path

# Adicionar o diretório raiz ao sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_github_access():
    """Testa diferentes endpoints do GitHub"""
    print("🔍 TESTE: Acesso ao GitHub")
    print("=" * 60)
    
    # Carregar token
    token_file = project_root / 'github_token.txt'
    if not token_file.exists():
        print("❌ Arquivo github_token.txt não encontrado!")
        return
    
    token = token_file.read_text(encoding='utf-8').strip()
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    repo_owner = "wmedrado"
    repo_name = "bot-keydrop"
    
    print(f"🏪 Repositório: {repo_owner}/{repo_name}")
    print(f"🔑 Token: {token[:10]}...{token[-10:]}")
    print()
    
    # Teste 1: Verificar se o usuário existe
    print("🔍 Teste 1: Verificando usuário...")
    try:
        response = requests.get(f"https://api.github.com/users/{repo_owner}", headers=headers)
        print(f"📡 Status: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"👤 Usuário: {user_data.get('login', 'N/A')}")
            print(f"📝 Nome: {user_data.get('name', 'N/A')}")
            print(f"🏪 Repositórios públicos: {user_data.get('public_repos', 0)}")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    print()
    
    # Teste 2: Verificar se o repositório existe
    print("🔍 Teste 2: Verificando repositório...")
    try:
        response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}", headers=headers)
        print(f"📡 Status: {response.status_code}")
        if response.status_code == 200:
            repo_data = response.json()
            print(f"📁 Repositório: {repo_data.get('full_name', 'N/A')}")
            print(f"🔒 Privado: {repo_data.get('private', False)}")
            print(f"📝 Descrição: {repo_data.get('description', 'N/A')}")
            print(f"🌟 Estrelas: {repo_data.get('stargazers_count', 0)}")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    print()
    
    # Teste 3: Verificar releases
    print("🔍 Teste 3: Verificando releases...")
    try:
        response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases", headers=headers)
        print(f"📡 Status: {response.status_code}")
        if response.status_code == 200:
            releases = response.json()
            print(f"📦 Total de releases: {len(releases)}")
            
            if releases:
                latest = releases[0]
                print(f"🏷️ Última release: {latest.get('tag_name', 'N/A')}")
                print(f"📝 Nome: {latest.get('name', 'N/A')}")
                print(f"📅 Data: {latest.get('published_at', 'N/A')}")
                print(f"🔄 Pré-release: {latest.get('prerelease', False)}")
                print(f"📎 Assets: {len(latest.get('assets', []))}")
            else:
                print("📦 Nenhuma release encontrada")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    print()
    
    # Teste 4: Verificar latest release
    print("🔍 Teste 4: Verificando latest release...")
    try:
        response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest", headers=headers)
        print(f"📡 Status: {response.status_code}")
        if response.status_code == 200:
            latest = response.json()
            print(f"🏷️ Tag: {latest.get('tag_name', 'N/A')}")
            print(f"📝 Nome: {latest.get('name', 'N/A')}")
            print(f"📅 Data: {latest.get('published_at', 'N/A')}")
            print(f"🔄 Pré-release: {latest.get('prerelease', False)}")
            print(f"📎 Assets: {len(latest.get('assets', []))}")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    print()
    
    # Teste 5: Verificar permissões
    print("🔍 Teste 5: Verificando permissões...")
    try:
        response = requests.get(f"https://api.github.com/user", headers=headers)
        print(f"📡 Status: {response.status_code}")
        if response.status_code == 200:
            user = response.json()
            print(f"👤 Usuário autenticado: {user.get('login', 'N/A')}")
            print(f"📧 Email: {user.get('email', 'N/A')}")
            print(f"🏪 Repositórios totais: {user.get('total_private_repos', 0)} privados + {user.get('public_repos', 0)} públicos")
        else:
            print(f"❌ Erro: {response.text}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    test_github_access()
