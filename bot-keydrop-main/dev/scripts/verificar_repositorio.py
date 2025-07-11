#!/usr/bin/env python3
"""
Script para verificar qual repositório existe
"""

import requests
import os
from pathlib import Path

# Obter token
project_root = Path(__file__).parent.parent.parent
token_file = project_root / 'github_token.txt'
token = token_file.read_text(encoding='utf-8').strip()

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

def testar_repositorio(owner, repo):
    """Testa se um repositório existe e tem permissão"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    print(f"🔍 Testando: {owner}/{repo}")
    print(f"📡 URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Repositório encontrado!")
            print(f"📂 Nome: {data['name']}")
            print(f"🔒 Privado: {data['private']}")
            print(f"👤 Proprietário: {data['owner']['login']}")
            print(f"🌐 URL: {data['html_url']}")
            return True
        elif response.status_code == 404:
            print(f"❌ Repositório não encontrado")
            return False
        elif response.status_code == 403:
            print(f"❌ Sem permissão para acessar")
            return False
        else:
            print(f"❓ Status desconhecido: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return False

def listar_repositorios(owner):
    """Lista todos os repositórios do usuário"""
    url = f"https://api.github.com/users/{owner}/repos"
    print(f"\n📋 Listando repositórios de: {owner}")
    print(f"📡 URL: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            repos = response.json()
            print(f"✅ {len(repos)} repositórios encontrados:")
            for repo in repos:
                print(f"  📂 {repo['name']} {'(privado)' if repo['private'] else '(público)'}")
            return repos
        else:
            print(f"❌ Erro ao listar repositórios: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return []

if __name__ == "__main__":
    print("🔍 Verificando repositórios do GitHub...")
    print("=" * 60)
    
    # Testar possíveis nomes
    repositorios_teste = [
        ("wmedrado", "bot-keydrop"),
        ("wmedrado", "BOT-KEYDROP-BY-WILL"),
        ("wmedrado", "keydrop-bot"),
        ("wmedrado", "KeyDrop-Bot"),
        ("wmedrdao", "bot-keydrop"),
        ("wmedrdao", "BOT-KEYDROP-BY-WILL"),
    ]
    
    for owner, repo in repositorios_teste:
        testar_repositorio(owner, repo)
        print("-" * 40)
    
    # Listar todos os repositórios
    listar_repositorios("wmedrado")
    print("-" * 40)
    listar_repositorios("wmedrdao")
