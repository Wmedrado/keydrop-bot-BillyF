#!/usr/bin/env python3
"""
Script para limpar arquivos antigos de release
"""
import os
import glob
from pathlib import Path

def cleanup_old_releases():
    """Remove arquivos antigos de release"""
    print("🧹 Limpando arquivos antigos de release...")
    
    # Arquivos ZIP antigos
    old_zips = [
        "KeyDrop_Bot_v2.0.1.zip",
        "KeyDrop_Bot_v2.0.2.zip", 
        "KeyDrop_Bot_v2.0.3.zip",
        "KeyDrop_Bot_v2.0.3_Fixed.zip",
        "KeyDrop_Bot_v2.0.4.zip",
        "KeyDrop_Bot_v2.0.5.zip",
        "KeyDrop_Bot_v2.0.6.zip",
        "KeyDrop_Bot_v2.0.7.zip"
    ]
    
    removed_count = 0
    for zip_file in old_zips:
        if os.path.exists(zip_file):
            try:
                os.remove(zip_file)
                print(f"✅ Removido: {zip_file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Erro ao remover {zip_file}: {e}")
    
    # Arquivos de documentação antigos
    old_docs = [
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
        "VALIDACAO_FINAL_v2.0.7.md"
    ]
    
    for doc_file in old_docs:
        if os.path.exists(doc_file):
            try:
                os.remove(doc_file)
                print(f"✅ Removido: {doc_file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Erro ao remover {doc_file}: {e}")
    
    # Scripts de criação de release antigos
    old_scripts = [
        "create_release.py",
        "create_release_v2.0.7.py",
        "fix_assets_v2.0.7.py",
        "upload_asset.py",
        "upload_correct_v2.0.7.py"
    ]
    
    for script_file in old_scripts:
        if os.path.exists(script_file):
            try:
                os.remove(script_file)
                print(f"✅ Removido: {script_file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Erro ao remover {script_file}: {e}")
    
    print(f"\n🎉 Limpeza concluída! {removed_count} arquivos removidos.")

if __name__ == "__main__":
    cleanup_old_releases()
