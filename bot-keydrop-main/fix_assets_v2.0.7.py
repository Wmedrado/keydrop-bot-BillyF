#!/usr/bin/env python3
"""
Script para verificar e corrigir assets da release v2.0.7
"""

import requests
import json
import os

def check_and_fix_assets():
    """Verifica e corrige assets da release v2.0.7"""
    
    # Ler token
    with open('github_token.txt', 'r') as f:
        token = f.read().strip()
    
    # Headers
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'KeyDrop-Bot-Updater'
    }
    
    # Buscar release v2.0.7
    url = 'https://api.github.com/repos/wmedrado/bot-keydrop/releases/tags/v2.0.7'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        release_data = response.json()
        print(f"✅ Release v2.0.7 encontrada!")
        print(f"📦 ID: {release_data['id']}")
        
        # Listar assets
        assets = release_data.get('assets', [])
        print(f"📋 Assets encontrados: {len(assets)}")
        
        for asset in assets:
            print(f"  - {asset['name']} (ID: {asset['id']})")
            
            # Se encontrar o arquivo com nome errado, deletar
            if asset['name'] == 'KeyDrop_Bot_v2.0.6.zip':
                print(f"❌ Deletando asset com nome incorreto: {asset['name']}")
                delete_url = f"https://api.github.com/repos/wmedrado/bot-keydrop/releases/assets/{asset['id']}"
                delete_response = requests.delete(delete_url, headers=headers)
                
                if delete_response.status_code == 204:
                    print("✅ Asset deletado com sucesso!")
                else:
                    print(f"❌ Erro ao deletar asset: {delete_response.status_code}")
        
        # Fazer upload do arquivo correto
        if os.path.exists('KeyDrop_Bot_v2.0.7.zip'):
            print("\n📤 Fazendo upload do arquivo correto...")
            upload_url = release_data['upload_url'].replace('{?name,label}', '')
            
            with open('KeyDrop_Bot_v2.0.7.zip', 'rb') as f:
                files = {'file': f}
                upload_response = requests.post(
                    f"{upload_url}?name=KeyDrop_Bot_v2.0.7.zip",
                    headers={
                        'Authorization': f'token {token}',
                        'Content-Type': 'application/zip'
                    },
                    data=f.read()
                )
                
                if upload_response.status_code == 201:
                    print("✅ Upload concluído com sucesso!")
                    asset_info = upload_response.json()
                    print(f"📦 Nome: {asset_info['name']}")
                    print(f"🔗 URL: {asset_info['browser_download_url']}")
                else:
                    print(f"❌ Erro no upload: {upload_response.status_code}")
                    print(f"📝 Resposta: {upload_response.text}")
        else:
            print("❌ Arquivo KeyDrop_Bot_v2.0.7.zip não encontrado!")
            
    else:
        print(f"❌ Erro ao buscar release: {response.status_code}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 CORREÇÃO DE ASSETS DA RELEASE v2.0.7")
    print("=" * 60)
    
    check_and_fix_assets()
    
    print("=" * 60)
