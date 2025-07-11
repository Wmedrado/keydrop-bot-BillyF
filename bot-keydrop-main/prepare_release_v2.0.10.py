#!/usr/bin/env python3
"""
Script para preparar distribuição da versão 2.0.10 - KeyDrop Bot Professional Edition
"""
import os
import shutil
import zipfile
import json
from datetime import datetime
from pathlib import Path

def prepare_release():
    """Prepara a release v2.0.10 para distribuição"""
    print("🚀 Preparando KeyDrop Bot Professional Edition v2.0.10...")
    print("=" * 60)
    
    # Verificar versão atual
    try:
        with open('version.json', 'r') as f:
            version_info = json.load(f)
            version = version_info['version']
            print(f"📦 Versão: {version}")
    except Exception as e:
        print(f"❌ Erro ao ler versão: {e}")
        return False
    
    # Limpar arquivos antigos primeiro
    cleanup_old_files()
    
    # Arquivos essenciais para a distribuição
    essential_files = [
        # Arquivos principais
        'modern_gui_v2.py',
        'keydrop_bot.py',
        'launcher.py',
        'bot_gui.py',
        'gui_keydrop.py',
        'modern_gui.py',
        'discord_notify.py',
        
        # Configurações
        'version.json',
        'requirements.txt',
        'bot_config.json',
        'bot_config_backup.json',
        'release_info.json',
        'github_token.txt',
        
        # Ícones
        'bot-icone.ico',
        'bot-icone.png',
        
        # Documentação
        'README.md',
        'CHANGELOG.md',
        'TROUBLESHOOTING.md',
        
        # Executáveis
        'KeyDrop_Bot_Classico.exe',
        'KeyDrop_Bot_Moderno.exe',
        'KeyDrop_Bot_Classico.spec',
        'KeyDrop_Bot_Moderno.spec'
    ]
    
    # Diretórios essenciais
    essential_dirs = [
        'src',
        'profiles',
        'docs',
        'startup',
        'dev'
    ]
    
    # Criar diretório temporário para a release
    release_dir = f"KeyDrop_Bot_Professional_v{version}"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    print(f"📁 Criando diretório de release: {release_dir}")
    
    # Copiar arquivos essenciais
    copied_files = 0
    for file in essential_files:
        if os.path.exists(file):
            try:
                shutil.copy2(file, release_dir)
                print(f"✅ Copiado: {file}")
                copied_files += 1
            except Exception as e:
                print(f"❌ Erro ao copiar {file}: {e}")
        else:
            print(f"⚠️ Arquivo não encontrado: {file}")
    
    # Copiar diretórios essenciais
    copied_dirs = 0
    for dir_name in essential_dirs:
        if os.path.exists(dir_name):
            try:
                shutil.copytree(dir_name, os.path.join(release_dir, dir_name))
                print(f"✅ Copiado diretório: {dir_name}")
                copied_dirs += 1
            except Exception as e:
                print(f"❌ Erro ao copiar {dir_name}: {e}")
        else:
            print(f"⚠️ Diretório não encontrado: {dir_name}")
    
    # Criar arquivo de informações da release
    release_info = {
        "version": version,
        "build_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "files_count": copied_files,
        "dirs_count": copied_dirs,
        "release_type": "production",
        "features": [
            "Interface moderna com CustomTkinter",
            "Suporte a múltiplos bots simultâneos",
            "Sistema de relatórios personalizável",
            "Integração completa com Telegram",
            "Controle remoto via Telegram",
            "Sistema de atualização automática",
            "Monitoramento de performance",
            "Banco de dados SQLite para estatísticas"
        ]
    }
    
    with open(os.path.join(release_dir, 'RELEASE_INFO.json'), 'w', encoding='utf-8') as f:
        json.dump(release_info, f, indent=2, ensure_ascii=False)
    
    # Criar arquivo ZIP para distribuição
    zip_filename = f"KeyDrop_Bot_Professional_v{version}.zip"
    
    print(f"\n📦 Criando arquivo ZIP: {zip_filename}")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arcname)
                
    # Verificar tamanho do arquivo
    zip_size = os.path.getsize(zip_filename) / (1024 * 1024)  # MB
    print(f"📊 Tamanho do arquivo: {zip_size:.2f} MB")
    
    # Limpar diretório temporário
    shutil.rmtree(release_dir)
    
    print("\n" + "=" * 60)
    print("🎉 RELEASE v2.0.10 PREPARADA COM SUCESSO!")
    print(f"📦 Arquivo: {zip_filename}")
    print(f"📊 Tamanho: {zip_size:.2f} MB")
    print(f"📁 Arquivos incluídos: {copied_files}")
    print(f"📂 Diretórios incluídos: {copied_dirs}")
    print("🚀 Pronto para distribuição!")
    
    return True

def cleanup_old_files():
    """Remove arquivos antigos desnecessários"""
    print("🧹 Limpando arquivos antigos...")
    
    # Arquivos ZIP antigos
    old_files = [
        "KeyDrop_Bot_v2.0.1.zip",
        "KeyDrop_Bot_v2.0.2.zip",
        "KeyDrop_Bot_v2.0.3.zip",
        "KeyDrop_Bot_v2.0.3_Fixed.zip",
        "KeyDrop_Bot_v2.0.4.zip",
        "KeyDrop_Bot_v2.0.5.zip",
        "KeyDrop_Bot_v2.0.6.zip",
        "KeyDrop_Bot_v2.0.7.zip",
        
        # Documentos antigos
        "FINALIZAÇÃO_v2.0.5.md",
        "IMPLEMENTACAO_COMPLETA_v2.0.9.md",
        "IMPLEMENTACAO_CONCLUIDA_v2.0.9.md",
        "INSTRUCOES_PUBLICACAO_v2.0.1.md",
        "INSTRUCOES_PUBLICACAO_v2.0.3.md",
        "INSTRUCOES_PUBLICACAO_v2.0.4.md",
        "INSTRUCOES_RELEASE_v2.0.2.md",
        "MELHORIAS_v2.0.5.md",
        "RELEASE_FORM_v2.0.2.md",
        "RELEASE_FORM_v2.0.3_FIXED.md",
        "RELEASE_FORM_v2.0.3.md",
        "RELEASE_FORM_v2.0.4.md",
        "RELEASE_FORM_v2.0.5.md",
        "RELEASE_FORM_v2.0.6.md",
        "RELEASE_FORM_v2.0.7.md",
        "RELEASE_NOTES_v2.0.9.md",
        "RELEASE_PUBLICADO_v2.0.1.md",
        "RESUMO_TÉCNICO_v2.0.5.md",
        "VALIDACAO_FINAL_v2.0.7.md",
        
        # Scripts antigos
        "create_release.py",
        "create_release_v2.0.7.py",
        "fix_assets_v2.0.7.py",
        "upload_asset.py",
        "upload_correct_v2.0.7.py"
    ]
    
    removed_count = 0
    for file in old_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🗑️ Removido: {file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Erro ao remover {file}: {e}")
    
    print(f"✅ {removed_count} arquivos antigos removidos")

if __name__ == "__main__":
    prepare_release()
