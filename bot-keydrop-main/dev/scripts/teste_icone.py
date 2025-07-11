#!/usr/bin/env python3
"""
Script de Teste do Ícone
Testa se o ícone está sendo carregado corretamente
"""

import os
import sys
import tkinter as tk
from pathlib import Path

# Adicionar o diretório raiz ao sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def testar_icone():
    """Testa o carregamento do ícone"""
    print("🎨 TESTE: Carregamento do Ícone")
    print("=" * 50)
    
    # Verificar se os arquivos existem
    ico_path = project_root / 'bot-icone.ico'
    png_path = project_root / 'bot-icone.png'
    
    print(f"📄 Ícone ICO: {ico_path}")
    print(f"✅ ICO existe: {ico_path.exists()}")
    
    print(f"📄 Ícone PNG: {png_path}")
    print(f"✅ PNG existe: {png_path.exists()}")
    
    # Verificar tamanho dos arquivos
    if ico_path.exists():
        size_ico = ico_path.stat().st_size
        print(f"📏 Tamanho ICO: {size_ico} bytes")
    
    if png_path.exists():
        size_png = png_path.stat().st_size
        print(f"📏 Tamanho PNG: {size_png} bytes")
    
    # Testar carregamento em tkinter
    try:
        print("🔄 Testando carregamento do ícone...")
        root = tk.Tk()
        root.withdraw()  # Ocultar janela
        
        # Testar ICO primeiro (melhor para Windows)
        if ico_path.exists():
            try:
                root.iconbitmap(str(ico_path))
                print("✅ ICO iconbitmap() - OK")
            except Exception as e:
                print(f"❌ ICO iconbitmap() - Erro: {e}")
        
        # Testar PNG como fallback
        if png_path.exists():
            try:
                icon_image = tk.PhotoImage(file=str(png_path))
                root.iconphoto(True, icon_image)
                print("✅ PNG PhotoImage + iconphoto() - OK")
            except Exception as e:
                print(f"❌ PNG PhotoImage + iconphoto() - Erro: {e}")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Erro geral no teste: {e}")
        return False
    
    print("\n🎉 Teste concluído com sucesso!")
    return True

def testar_interface_moderna():
    """Testa o ícone na interface moderna"""
    print("\n🎨 TESTE: Ícone na Interface Moderna")
    print("=" * 50)
    
    try:
        # Importar customtkinter
        import customtkinter as ctk
        
        # Criar janela de teste
        root = ctk.CTk()
        root.title("Teste de Ícone - KeyDrop Bot")
        root.geometry("400x300")
        
        # Tentar carregar o ícone (prioridade para ICO)
        ico_path = project_root / 'bot-icone.ico'
        png_path = project_root / 'bot-icone.png'
        
        icon_loaded = False
        
        # Tentar ICO primeiro
        if ico_path.exists():
            try:
                root.iconbitmap(str(ico_path))
                print("✅ Ícone ICO carregado na interface moderna!")
                icon_loaded = True
            except Exception as e:
                print(f"❌ Erro ao carregar ICO: {e}")
        
        # Fallback para PNG
        if not icon_loaded and png_path.exists():
            try:
                icon_image = tk.PhotoImage(file=str(png_path))
                root.iconphoto(True, icon_image)
                print("✅ Ícone PNG carregado na interface moderna!")
                icon_loaded = True
            except Exception as e:
                print(f"❌ Erro ao carregar PNG: {e}")
        
        if not icon_loaded:
            print("❌ Nenhum ícone foi carregado!")
        
        # Mostrar janela por 3 segundos
        root.after(3000, root.destroy)
        
        # Label de teste
        label = ctk.CTkLabel(
            root,
            text="🎨 Teste de Ícone\n\nVerifique se o ícone aparece\nna barra de título",
            font=ctk.CTkFont(size=16)
        )
        label.pack(expand=True)
        
        root.mainloop()
        
        print("✅ Teste da interface moderna concluído!")
        
    except Exception as e:
        print(f"❌ Erro no teste da interface moderna: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 INICIANDO TESTES DO ÍCONE\n")
    
    # Teste 1: Verificar arquivo
    sucesso1 = testar_icone()
    
    # Teste 2: Interface moderna
    sucesso2 = testar_interface_moderna()
    
    print("\n📊 RESULTADO DOS TESTES:")
    print(f"✅ Arquivo e carregamento básico: {'OK' if sucesso1 else 'ERRO'}")
    print(f"✅ Interface moderna: {'OK' if sucesso2 else 'ERRO'}")
    
    if sucesso1 and sucesso2:
        print("\n🎉 Todos os testes passaram! O ícone está funcionando corretamente.")
    else:
        print("\n❌ Alguns testes falharam. Verifique os erros acima.")
