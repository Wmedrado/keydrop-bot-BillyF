#!/usr/bin/env python3
"""
Script simplificado para upload correto do arquivo v2.0.7
"""

import requests
import json
import os

def upload_correct_file():
    """Faz upload do arquivo correto"""
    
    # Ler token
    with open('github_token.txt', 'r') as f:
        token = f.read().strip()
    
    # Ler informações da release
    with open('release_info.json', 'r') as f:
        release_info = json.load(f)
    
    # Headers
    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/zip'
    }
    
    # URL de upload
    upload_url = release_info['upload_url'].replace('{?name,label}', '')
    
    # Arquivo
    filename = 'KeyDrop_Bot_v2.0.7.zip'
    
    if not os.path.exists(filename):
        print(f"❌ Arquivo {filename} não encontrado!")
        return False
    
    print(f"📤 Fazendo upload de {filename}...")
    
    with open(filename, 'rb') as f:
        response = requests.post(
            f"{upload_url}?name={filename}",
            headers=headers,
            data=f.read()
        )
    
    if response.status_code == 201:
        asset_info = response.json()
        print("✅ Upload concluído com sucesso!")
        print(f"📦 Nome: {asset_info['name']}")
        print(f"🔗 URL: {asset_info['browser_download_url']}")
        return True
    else:
        print(f"❌ Erro no upload: {response.status_code}")
        print(f"📝 Resposta: {response.text}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("📤 UPLOAD DO ARQUIVO v2.0.7")
    print("=" * 60)
    
    success = upload_correct_file()
    
    if success:
        print("🎉 Upload concluído com sucesso!")
    else:
        print("❌ Falha no upload.")
    
    print("=" * 60)
