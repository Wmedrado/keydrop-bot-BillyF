#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Diagnóstico completo do sistema de atualização
👨‍💻 Desenvolvido por: Billy Franck (wmedrado)
📞 Discord: wmedrado
"""

import requests
import json
import os
from pathlib import Path

def diagnosticar_token():
    """Diagnostica o token do GitHub"""
    print("🔑 DIAGNÓSTICO DO TOKEN")
    print("=" * 40)
    
    try:
        # Verificar arquivo de token
        token_file = Path("github_token.txt")
        if not token_file.exists():
            print("❌ Arquivo github_token.txt não encontrado!")
            return False
        
        token = token_file.read_text().strip()
        if not token:
            print("❌ Token está vazio!")
            return False
        
        print(f"✅ Token encontrado: {token[:10]}...")
        
        # Testar autenticação
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Testar acesso básico à API
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ Token válido! Usuário: {user_info.get('login')}")
            return True
        else:
            print(f"❌ Token inválido! Status: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar token: {e}")
        return False

def diagnosticar_repositorio():
    """Diagnostica o acesso ao repositório"""
    print("\n📁 DIAGNÓSTICO DO REPOSITÓRIO")
    print("=" * 40)
    
    try:
        token_file = Path("github_token.txt")
        token = token_file.read_text().strip()
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Testar acesso ao repositório específico
        repo_url = 'https://api.github.com/repos/Wmedrado/bot-keydrop'
        response = requests.get(repo_url, headers=headers)
        
        print(f"🔍 Testando: {repo_url}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            repo_info = response.json()
            print(f"✅ Repositório encontrado!")
            print(f"   Nome: {repo_info.get('name')}")
            print(f"   Privado: {repo_info.get('private')}")
            print(f"   Owner: {repo_info.get('owner', {}).get('login')}")
            return True
            
        elif response.status_code == 404:
            print("❌ Repositório não encontrado!")
            print("💡 Possíveis causas:")
            print("   1. Nome do repositório incorreto")
            print("   2. Repositório não existe")
            print("   3. Token sem permissão de acesso")
            return False
            
        elif response.status_code == 403:
            print("❌ Acesso negado!")
            print("💡 Possíveis causas:")
            print("   1. Token sem permissão 'repo'")
            print("   2. Repositório privado sem acesso")
            return False
            
        else:
            print(f"❌ Erro inesperado: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar repositório: {e}")
        return False

def listar_repositorios_usuario():
    """Lista todos os repositórios do usuário"""
    print("\n📋 REPOSITÓRIOS DO USUÁRIO")
    print("=" * 40)
    
    try:
        token_file = Path("github_token.txt")
        token = token_file.read_text().strip()
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Listar repositórios (incluindo privados)
        response = requests.get('https://api.github.com/user/repos?per_page=100', headers=headers)
        
        if response.status_code == 200:
            repos = response.json()
            
            print(f"📁 Total de repositórios: {len(repos)}")
            print("\n🔍 Procurando repositórios relacionados ao bot:")
            
            bot_repos = []
            for repo in repos:
                repo_name = repo.get('name', '').lower()
                if any(term in repo_name for term in ['bot', 'keydrop', 'key-drop']):
                    bot_repos.append(repo)
                    visibility = "🔒 Privado" if repo.get('private') else "🌐 Público"
                    print(f"   • {repo.get('full_name')} {visibility}")
            
            if not bot_repos:
                print("⚠️ Nenhum repositório relacionado ao bot encontrado!")
                print("\n📋 Todos os repositórios:")
                for repo in repos[:10]:  # Mostrar apenas os primeiros 10
                    visibility = "🔒 Privado" if repo.get('private') else "🌐 Público"
                    print(f"   • {repo.get('full_name')} {visibility}")
                
                if len(repos) > 10:
                    print(f"   ... e mais {len(repos) - 10} repositórios")
            
            return bot_repos
            
        else:
            print(f"❌ Erro ao listar repositórios: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Erro ao listar repositórios: {e}")
        return []

def verificar_releases():
    """Verifica as releases do repositório"""
    print("\n🚀 VERIFICANDO RELEASES")
    print("=" * 40)
    
    try:
        token_file = Path("github_token.txt")
        token = token_file.read_text().strip()
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Verificar releases
        releases_url = 'https://api.github.com/repos/Wmedrado/bot-keydrop/releases'
        response = requests.get(releases_url, headers=headers)
        
        print(f"🔍 Testando: {releases_url}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            releases = response.json()
            print(f"✅ {len(releases)} releases encontradas")
            
            if releases:
                print("\n📋 Releases disponíveis:")
                for release in releases[:5]:  # Mostrar apenas as 5 mais recentes
                    print(f"   • {release.get('tag_name')} - {release.get('name')}")
                    print(f"     Criado: {release.get('created_at')}")
                    print(f"     Draft: {release.get('draft')}")
                    print(f"     Prerelease: {release.get('prerelease')}")
                    print()
            else:
                print("⚠️ Nenhuma release encontrada")
                print("💡 Para o sistema de atualização funcionar, você precisa:")
                print("   1. Criar pelo menos uma release no GitHub")
                print("   2. Definir uma tag de versão (ex: v2.0.1)")
                print("   3. Publicar a release")
            
            return len(releases) > 0
            
        else:
            print(f"❌ Erro ao verificar releases: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar releases: {e}")
        return False

def verificar_permissoes_token():
    """Verifica as permissões do token"""
    print("\n🔐 VERIFICANDO PERMISSÕES DO TOKEN")
    print("=" * 40)
    
    try:
        token_file = Path("github_token.txt")
        token = token_file.read_text().strip()
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Fazer uma requisição para ver os headers de resposta
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            # As permissões estão no header X-OAuth-Scopes
            scopes = response.headers.get('X-OAuth-Scopes', '')
            print(f"🔍 Scopes do token: {scopes}")
            
            required_scopes = ['repo']
            missing_scopes = []
            
            for scope in required_scopes:
                if scope not in scopes:
                    missing_scopes.append(scope)
            
            if missing_scopes:
                print(f"❌ Permissões faltando: {', '.join(missing_scopes)}")
                print("💡 Para corrigir:")
                print("   1. Acesse: https://github.com/settings/tokens")
                print("   2. Edite seu token")
                print("   3. Marque a permissão 'repo'")
                print("   4. Atualize o token")
                return False
            else:
                print("✅ Token tem todas as permissões necessárias!")
                return True
                
        else:
            print(f"❌ Erro ao verificar permissões: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar permissões: {e}")
        return False

def main():
    """Função principal de diagnóstico"""
    print("🔧 DIAGNÓSTICO COMPLETO DO SISTEMA DE ATUALIZAÇÃO")
    print("=" * 60)
    
    resultados = {
        'token': False,
        'repositorio': False,
        'releases': False,
        'permissoes': False
    }
    
    # Executar todos os diagnósticos
    resultados['token'] = diagnosticar_token()
    
    if resultados['token']:
        resultados['permissoes'] = verificar_permissoes_token()
        resultados['repositorio'] = diagnosticar_repositorio()
        
        if not resultados['repositorio']:
            # Se o repositório não foi encontrado, listar todos
            listar_repositorios_usuario()
        else:
            resultados['releases'] = verificar_releases()
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO DO DIAGNÓSTICO")
    print("=" * 60)
    
    status_emoji = {True: "✅", False: "❌"}
    
    print(f"{status_emoji[resultados['token']]} Token do GitHub")
    print(f"{status_emoji[resultados['permissoes']]} Permissões do token")
    print(f"{status_emoji[resultados['repositorio']]} Acesso ao repositório")
    print(f"{status_emoji[resultados['releases']]} Releases disponíveis")
    
    if all(resultados.values()):
        print("\n🎉 SISTEMA DE ATUALIZAÇÃO FUNCIONANDO!")
        print("✅ Todos os componentes estão corretos")
    else:
        print("\n⚠️ PROBLEMAS ENCONTRADOS:")
        
        if not resultados['token']:
            print("   🔑 Configure um token válido")
        elif not resultados['permissoes']:
            print("   🔐 Adicione permissão 'repo' ao token")
        elif not resultados['repositorio']:
            print("   📁 Verifique o nome do repositório")
        elif not resultados['releases']:
            print("   🚀 Crie pelo menos uma release")
    
    print("\n" + "=" * 60)
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    # Mudar para o diretório do projeto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..', '..')
    os.chdir(project_root)
    
    main()
