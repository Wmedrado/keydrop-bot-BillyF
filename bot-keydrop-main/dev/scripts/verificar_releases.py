#!/usr/bin/env python3
"""
Script para verificar releases no repositório
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

def verificar_releases(owner, repo):
    """Verifica releases no repositório"""
    print(f"🔍 Verificando releases: {owner}/{repo}")
    
    # Testar latest release
    url_latest = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    print(f"📡 URL (latest): {url_latest}")
    
    try:
        response = requests.get(url_latest, headers=headers, timeout=10)
        print(f"📊 Status (latest): {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Latest release encontrado!")
            print(f"🏷️  Tag: {data['tag_name']}")
            print(f"📝 Nome: {data['name']}")
            print(f"📅 Data: {data['published_at']}")
            print(f"📋 Descrição: {data['body'][:100]}...")
            print(f"🔗 URL: {data['html_url']}")
            return True
        elif response.status_code == 404:
            print(f"❌ Nenhum release encontrado")
        else:
            print(f"❓ Status desconhecido: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Testar todos os releases
    url_all = f"https://api.github.com/repos/{owner}/{repo}/releases"
    print(f"\n📡 URL (all): {url_all}")
    
    try:
        response = requests.get(url_all, headers=headers, timeout=10)
        print(f"📊 Status (all): {response.status_code}")
        
        if response.status_code == 200:
            releases = response.json()
            print(f"✅ {len(releases)} releases encontrados:")
            for release in releases:
                print(f"  🏷️  {release['tag_name']} - {release['name']} ({release['published_at'][:10]})")
            return len(releases) > 0
        else:
            print(f"❌ Erro ao listar releases: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    return False

def criar_release_teste(owner, repo):
    """Cria um release de teste"""
    print(f"\n🔧 Criando release de teste: {owner}/{repo}")
    
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    print(f"📡 URL: {url}")
    
    release_data = {
        "tag_name": "v2.0.1",
        "name": "KeyDrop Bot v2.0.1",
        "body": "Release de teste para sistema de atualização automática\n\n### Melhorias:\n- Correção do sistema de atualização\n- Melhorias na interface\n- Otimizações de performance",
        "draft": False,
        "prerelease": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=release_data, timeout=10)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Release criado com sucesso!")
            print(f"🏷️  Tag: {data['tag_name']}")
            print(f"📝 Nome: {data['name']}")
            print(f"🔗 URL: {data['html_url']}")
            return True
        else:
            print(f"❌ Erro ao criar release: {response.status_code}")
            print(f"📋 Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    return False

if __name__ == "__main__":
    print("🔍 Verificando releases no repositório...")
    print("=" * 60)
    
    owner = "wmedrado"
    repo = "bot-keydrop"
    
    # Verificar releases existentes
    has_releases = verificar_releases(owner, repo)
    
    if not has_releases:
        print("\n⚠️  Nenhum release encontrado!")
        print("💡 O sistema de atualização precisa de pelo menos um release para funcionar.")
        
        resposta = input("\n🤔 Deseja criar um release de teste? (s/n): ")
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            criar_release_teste(owner, repo)
            print("\n🔄 Verificando novamente...")
            verificar_releases(owner, repo)
