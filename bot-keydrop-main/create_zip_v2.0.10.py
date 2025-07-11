#!/usr/bin/env python3
"""
Script simples para criar o arquivo ZIP da versão 2.0.10
"""
import os
import zipfile
import json
from datetime import datetime

def create_release_zip():
    """Cria o arquivo ZIP da release v2.0.10"""
    print("📦 Criando KeyDrop Bot Professional Edition v2.0.10...")
    
    # Verificar versão
    try:
        with open('version.json', 'r') as f:
            version_info = json.load(f)
            version = version_info['version']
            print(f"Versão: {version}")
    except:
        version = "2.0.10"
    
    # Arquivo ZIP
    zip_filename = f"KeyDrop_Bot_Professional_v{version}.zip"
    
    # Arquivos essenciais
    files_to_include = [
        'modern_gui_v2.py',
        'keydrop_bot.py',
        'launcher.py',
        'bot_gui.py',
        'gui_keydrop.py',
        'modern_gui.py',
        'discord_notify.py',
        'version.json',
        'requirements.txt',
        'bot_config.json',
        'bot_config_backup.json',
        'release_info.json',
        'github_token.txt',
        'bot-icone.ico',
        'bot-icone.png',
        'README.md',
        'CHANGELOG.md',
        'TROUBLESHOOTING.md',
        'RELEASE_NOTES_v2.0.10.md',
        'KeyDrop_Bot_Classico.exe',
        'KeyDrop_Bot_Moderno.exe',
        'KeyDrop_Bot_Classico.spec',
        'KeyDrop_Bot_Moderno.spec',
        'test_new_features.py',
        'demo_new_features.py',
        'test_update_system.py'
    ]
    
    # Diretórios essenciais
    dirs_to_include = [
        'src',
        'profiles',
        'docs',
        'startup',
        'dev'
    ]
    
    print(f"📁 Criando arquivo: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Adicionar arquivos
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file)
                print(f"✅ Adicionado: {file}")
            else:
                print(f"⚠️ Não encontrado: {file}")
        
        # Adicionar diretórios
        for dir_name in dirs_to_include:
            if os.path.exists(dir_name):
                for root, dirs, files in os.walk(dir_name):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path)
                print(f"✅ Adicionado diretório: {dir_name}")
            else:
                print(f"⚠️ Diretório não encontrado: {dir_name}")
    
    # Verificar tamanho
    if os.path.exists(zip_filename):
        size = os.path.getsize(zip_filename) / (1024 * 1024)  # MB
        print(f"📊 Arquivo criado: {zip_filename} ({size:.2f} MB)")
        print("🎉 Release v2.0.10 criada com sucesso!")
        return True
    else:
        print("❌ Falha ao criar arquivo ZIP")
        return False

if __name__ == "__main__":
    success = create_release_zip()
    if success:
        print("\n🚀 KeyDrop Bot Professional Edition v2.0.10 pronto para distribuição!")
    else:
        print("\n❌ Erro ao criar release")
