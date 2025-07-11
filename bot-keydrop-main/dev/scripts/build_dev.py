#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de build para desenvolvimento
👨‍💻 Desenvolvido por: Billy Franck (wmedrado)
📞 Discord: wmedrado
"""

import os
import shutil
import zipfile
import json
from datetime import datetime

def limpar_projeto():
    """Remove arquivos temporários e cache"""
    print("🧹 Limpando arquivos temporários...")
    
    # Pastas para limpar
    pastas_limpar = [
        '__pycache__',
        'src/__pycache__',
        'dev/temp',
        'dev/logs'
    ]
    
    # Arquivos para limpar
    arquivos_limpar = [
        '*.pyc',
        '*.pyo',
        '*.log',
        '*.tmp'
    ]
    
    projeto_root = os.path.join(os.path.dirname(__file__), '..', '..')
    
    for pasta in pastas_limpar:
        pasta_path = os.path.join(projeto_root, pasta)
        if os.path.exists(pasta_path):
            shutil.rmtree(pasta_path)
            print(f"   ✅ Removido: {pasta}")
    
    print("✅ Limpeza concluída!")

def criar_backup():
    """Cria backup do projeto"""
    print("💾 Criando backup do projeto...")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"backup_projeto_{timestamp}.zip"
    
    projeto_root = os.path.join(os.path.dirname(__file__), '..', '..')
    backup_path = os.path.join(os.path.dirname(__file__), '..', 'backup', backup_name)
    
    # Arquivos principais para backup
    arquivos_backup = [
        'modern_gui.py',
        'keydrop_bot.py',
        'bot_config.json',
        'version.json',
        'requirements.txt',
        'src/',
        'docs/',
        'github_token.txt'
    ]
    
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in arquivos_backup:
            item_path = os.path.join(projeto_root, item)
            if os.path.exists(item_path):
                if os.path.isdir(item_path):
                    # Adicionar diretório
                    for root, dirs, files in os.walk(item_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, projeto_root)
                            zipf.write(file_path, arcname)
                else:
                    # Adicionar arquivo
                    zipf.write(item_path, item)
    
    print(f"✅ Backup criado: {backup_name}")
    return backup_path

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("📦 Verificando dependências...")
    
    try:
        import customtkinter
        print("   ✅ customtkinter")
    except ImportError:
        print("   ❌ customtkinter - Execute: pip install customtkinter")
    
    try:
        import selenium
        print("   ✅ selenium")
    except ImportError:
        print("   ❌ selenium - Execute: pip install selenium")
    
    try:
        import requests
        print("   ✅ requests")
    except ImportError:
        print("   ❌ requests - Execute: pip install requests")
    
    try:
        import PIL
        print("   ✅ Pillow")
    except ImportError:
        print("   ❌ Pillow - Execute: pip install Pillow")
    
    print("✅ Verificação de dependências concluída!")

def atualizar_versao():
    """Atualiza a versão do projeto"""
    print("🔄 Atualizando versão...")
    
    version_path = os.path.join(os.path.dirname(__file__), '..', '..', 'version.json')
    
    try:
        with open(version_path, 'r', encoding='utf-8') as f:
            version_data = json.load(f)
        
        # Incrementar versão patch
        version_parts = version_data['version'].split('.')
        version_parts[2] = str(int(version_parts[2]) + 1)
        new_version = '.'.join(version_parts)
        
        version_data['version'] = new_version
        version_data['last_updated'] = datetime.now().isoformat()
        
        with open(version_path, 'w', encoding='utf-8') as f:
            json.dump(version_data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Versão atualizada para: {new_version}")
        return new_version
    except Exception as e:
        print(f"❌ Erro ao atualizar versão: {e}")
        return None

def main():
    """Função principal de build"""
    print("🚀 SCRIPT DE BUILD PARA DESENVOLVIMENTO")
    print("=" * 50)
    
    opcoes = [
        ("1", "Limpar projeto", limpar_projeto),
        ("2", "Criar backup", criar_backup),
        ("3", "Verificar dependências", verificar_dependencias),
        ("4", "Atualizar versão", atualizar_versao),
        ("5", "Build completo", lambda: [limpar_projeto(), verificar_dependencias(), criar_backup(), atualizar_versao()]),
    ]
    
    print("📋 Opções disponíveis:")
    for codigo, nome, _ in opcoes:
        print(f"   {codigo}. {nome}")
    
    escolha = input("\n🤔 Escolha uma opção (1-5): ").strip()
    
    for codigo, nome, funcao in opcoes:
        if escolha == codigo:
            print(f"\n🔄 Executando: {nome}")
            print("-" * 30)
            
            if codigo == "5":  # Build completo
                for step in funcao():
                    pass
            else:
                funcao()
            
            print("-" * 30)
            print("✅ Concluído!")
            break
    else:
        print("❌ Opção inválida!")
    
    print("=" * 50)
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
