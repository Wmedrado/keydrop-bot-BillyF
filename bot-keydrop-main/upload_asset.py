import requests
import json
import os

# Ler token
with open('github_token.txt', 'r') as f:
    token = f.read().strip()

# Ler informações da release
with open('release_info.json', 'r') as f:
    release_info = json.load(f)

# Headers
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'KeyDrop-Bot-Updater'
}

# Informações da release
release_id = release_info['id']
upload_url = release_info['upload_url'].replace('{?name,label}', '')

# Arquivo para upload
zip_file = 'KeyDrop_Bot_v2.0.7.zip'

if not os.path.exists(zip_file):
    print(f'❌ Arquivo {zip_file} não encontrado!')
    exit(1)

# Fazer upload do arquivo
print(f'📤 Fazendo upload de {zip_file}...')

# Headers para upload
upload_headers = {
    'Authorization': f'token {token}',
    'Content-Type': 'application/zip',
    'User-Agent': 'KeyDrop-Bot-Updater'
}

# URL de upload
upload_url_with_name = f'{upload_url}?name={zip_file}'

# Fazer upload
with open(zip_file, 'rb') as f:
    file_data = f.read()

response = requests.post(
    upload_url_with_name,
    headers=upload_headers,
    data=file_data
)

if response.status_code == 201:
    print('✅ Upload realizado com sucesso!')
    asset_info = response.json()
    print(f'📋 Nome do arquivo: {asset_info["name"]}')
    print(f'📏 Tamanho: {asset_info["size"]} bytes')
    print(f'🌐 URL de download: {asset_info["browser_download_url"]}')
else:
    print(f'❌ Erro no upload: {response.status_code}')
    print(f'📝 Resposta: {response.text}')
