#!/usr/bin/env python3
"""
Criação direta do arquivo ZIP para release v2.0.10
"""
import os
import zipfile
import sys

def create_zip_directly():
    """Cria o arquivo ZIP diretamente"""
    print("Criando KeyDrop_Bot_Professional_v2.0.10.zip...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('modern_gui_v2.py'):
        print("ERRO: Arquivo modern_gui_v2.py não encontrado")
        return False
    
    zip_filename = "KeyDrop_Bot_Professional_v2.0.10.zip"
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
            # Arquivos principais
            main_files = [
                'modern_gui_v2.py',
                'keydrop_bot.py',
                'launcher.py',
                'bot_gui.py',
                'gui_keydrop.py',
                'modern_gui.py',
                'discord_notify.py'
            ]
            
            for file in main_files:
                if os.path.exists(file):
                    zipf.write(file)
                    print(f"Adicionado: {file}")
            
            # Arquivos de configuração
            config_files = [
                'version.json',
                'requirements.txt',
                'bot_config.json',
                'bot_config_backup.json',
                'release_info.json',
                'github_token.txt'
            ]
            
            for file in config_files:
                if os.path.exists(file):
                    zipf.write(file)
                    print(f"Adicionado: {file}")
            
            # Arquivos de documentação
            doc_files = [
                'README.md',
                'CHANGELOG.md',
                'TROUBLESHOOTING.md',
                'RELEASE_NOTES_v2.0.10.md'
            ]
            
            for file in doc_files:
                if os.path.exists(file):
                    zipf.write(file)
                    print(f"Adicionado: {file}")
            
            # Ícones
            icon_files = [
                'bot-icone.ico',
                'bot-icone.png'
            ]
            
            for file in icon_files:
                if os.path.exists(file):
                    zipf.write(file)
                    print(f"Adicionado: {file}")
            
            # Executáveis
            exe_files = [
                'KeyDrop_Bot_Classico.exe',
                'KeyDrop_Bot_Moderno.exe',
                'KeyDrop_Bot_Classico.spec',
                'KeyDrop_Bot_Moderno.spec'
            ]
            
            for file in exe_files:
                if os.path.exists(file):
                    zipf.write(file)
                    print(f"Adicionado: {file}")
            
            # Diretório src
            if os.path.exists('src'):
                for root, dirs, files in os.walk('src'):
                    for file in files:
                        if file.endswith('.py'):
                            file_path = os.path.join(root, file)
                            zipf.write(file_path)
                            print(f"Adicionado: {file_path}")
            
            # Diretório docs
            if os.path.exists('docs'):
                for root, dirs, files in os.walk('docs'):
                    for file in files:
                        if file.endswith('.md'):
                            file_path = os.path.join(root, file)
                            zipf.write(file_path)
                            print(f"Adicionado: {file_path}")
            
            # Diretório startup
            if os.path.exists('startup'):
                for root, dirs, files in os.walk('startup'):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path)
                        print(f"Adicionado: {file_path}")
        
        # Verificar se foi criado
        if os.path.exists(zip_filename):
            size = os.path.getsize(zip_filename) / (1024 * 1024)
            print(f"SUCESSO: {zip_filename} criado ({size:.2f} MB)")
            return True
        else:
            print("ERRO: Arquivo ZIP não foi criado")
            return False
            
    except Exception as e:
        print(f"ERRO: {e}")
        return False

if __name__ == "__main__":
    success = create_zip_directly()
    if success:
        print("KeyDrop Bot Professional Edition v2.0.10 pronto!")
    else:
        print("Falha na criação do arquivo ZIP")
        sys.exit(1)
