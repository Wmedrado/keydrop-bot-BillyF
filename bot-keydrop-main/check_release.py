import requests
import json

# Ler token
with open('github_token.txt', 'r') as f:
    token = f.read().strip()

# Headers
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'KeyDrop-Bot-Updater'
}

# Verificar se release já existe
url = 'https://api.github.com/repos/wmedrado/bot-keydrop/releases/tags/v2.0.7'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print('✅ Release v2.0.7 já existe!')
    release_info = response.json()
    print(f'📋 ID da release: {release_info["id"]}')
    print(f'🌐 URL da release: {release_info["html_url"]}')
    print(f'📦 Arquivos: {len(release_info["assets"])} assets')
    
    # Salvar informações para upload
    with open('release_info.json', 'w') as f:
        json.dump(release_info, f, indent=2)
else:
    print(f'❌ Release não encontrada: {response.status_code}')
    print(f'📝 Resposta: {response.text}')
