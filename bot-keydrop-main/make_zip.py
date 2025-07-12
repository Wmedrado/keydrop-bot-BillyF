import zipfile
import os

# Criar arquivo ZIP da versão 4.0.0
zip_name = "KeyDrop_Bot_Professional_v4.0.0.zip"

print(f"Criando {zip_name}...")

with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Arquivos principais
    files = [
        'modern_gui_v2.py',
        'keydrop_bot.py',
        'launcher.py',
        'bot_gui.py',
        'discord_notify.py',
        'version.json',
        'requirements.txt',
        'bot_config.json',
        'github_token.txt',
        'README.md',
        'TROUBLESHOOTING.md',
        'RELEASE_NOTES_v4.0.0.md',
        'bot-icone.ico',
        'bot-icone.png',
        'KeyDrop_Bot_Classico.exe',
        'KeyDrop_Bot_Moderno.exe'
    ]
    
    for f in files:
        if os.path.exists(f):
            zf.write(f)
            print(f"+ {f}")
    
    # Diretório src
    for root, dirs, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                fp = os.path.join(root, file)
                zf.write(fp)
                print(f"+ {fp}")
    
    # Diretório docs essencial
    if os.path.exists('docs/INSTALACAO.md'):
        zf.write('docs/INSTALACAO.md')
        print("+ docs/INSTALACAO.md")

print(f"Arquivo {zip_name} criado!")
size = os.path.getsize(zip_name) / (1024*1024)
print(f"Tamanho: {size:.1f} MB")
