#!/usr/bin/env python3
"""
Script de Teste Completo
Testa todas as funcionalidades implementadas
"""

import os
import sys
from pathlib import Path
import threading
import time

# Adicionar o diretório raiz ao sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def testar_icone_rapido():
    """Teste rápido do ícone"""
    print("🎨 TESTE: Ícone")
    print("=" * 30)
    
    ico_path = project_root / 'bot-icone.ico'
    png_path = project_root / 'bot-icone.png'
    
    print(f"✅ ICO existe: {ico_path.exists()}")
    print(f"✅ PNG existe: {png_path.exists()}")
    
    if ico_path.exists():
        size_ico = ico_path.stat().st_size
        print(f"📏 Tamanho ICO: {size_ico} bytes")
    
    return ico_path.exists() and png_path.exists()

def testar_atualizacao_rapido():
    """Teste rápido da atualização"""
    print("\n🔄 TESTE: Sistema de Atualização")
    print("=" * 30)
    
    try:
        from src.private_update_manager import PrivateUpdateManager
        
        mgr = PrivateUpdateManager()
        print(f"✅ Token configurado: {bool(mgr.github_token)}")
        
        if mgr.github_token:
            result = mgr.check_for_updates()
            print(f"✅ Verificação: {result.get('message', 'OK')}")
            return True
        else:
            print("❌ Token não configurado")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def testar_interface_rapido():
    """Teste rápido da interface"""
    print("\n🎨 TESTE: Interface com Ícone")
    print("=" * 30)
    
    try:
        import customtkinter as ctk
        import tkinter as tk
        
        # Criar janela de teste
        root = ctk.CTk()
        root.title("Teste KeyDrop Bot")
        root.geometry("300x200")
        
        # Carregar ícone
        ico_path = project_root / 'bot-icone.ico'
        if ico_path.exists():
            root.iconbitmap(str(ico_path))
            print("✅ Ícone carregado!")
        else:
            print("❌ Ícone não encontrado")
        
        # Label
        label = ctk.CTkLabel(
            root,
            text="🎉 Teste OK!\n\nVerifique se o ícone\naparece na barra de título",
            font=ctk.CTkFont(size=14)
        )
        label.pack(expand=True)
        
        # Fechar automaticamente após 2 segundos
        def fechar():
            root.destroy()
        
        root.after(2000, fechar)
        root.mainloop()
        
        print("✅ Interface testada!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na interface: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 TESTE COMPLETO - KeyDrop Bot Professional Edition")
    print("=" * 60)
    
    # Testes
    teste1 = testar_icone_rapido()
    teste2 = testar_atualizacao_rapido()
    teste3 = testar_interface_rapido()
    
    print("\n📊 RESULTADOS:")
    print("=" * 30)
    print(f"🎨 Ícone: {'✅ OK' if teste1 else '❌ ERRO'}")
    print(f"🔄 Atualização: {'✅ OK' if teste2 else '❌ ERRO'}")
    print(f"🖥️ Interface: {'✅ OK' if teste3 else '❌ ERRO'}")
    
    if teste1 and teste2 and teste3:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Projeto pronto para produção!")
    else:
        print("\n❌ Alguns testes falharam.")
        print("🔧 Verifique os erros acima.")
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Fazer commit das alterações")
    print("2. Atualizar a release no GitHub")
    print("3. Testar em ambiente de produção")
    print("\n👨‍💻 Desenvolvido por: William Medrado (wmedrado)")
    print("📞 Discord: wmedrado")

if __name__ == "__main__":
    main()
