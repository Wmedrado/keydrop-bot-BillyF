#!/usr/bin/env python3
"""
Utilitário para Configuração de Ícones
Facilita a configuração de ícones nas interfaces
"""

import os
import sys
import tkinter as tk
from pathlib import Path

def configurar_icone(window, arquivo_icone=None):
    """
    Configura ícone para uma janela Tkinter/CustomTkinter
    
    Args:
        window: Janela Tkinter/CustomTkinter
        arquivo_icone: Caminho para o arquivo de ícone (opcional)
    """
    try:
        # Determinar caminho do ícone
        if arquivo_icone:
            icon_path = arquivo_icone
        else:
            # Procurar por arquivos de ícone na raiz do projeto
            project_root = Path(__file__).parent.parent
            
            # Prioridade: .ico primeiro, depois .png
            possible_icons = [
                project_root / 'bot-icone.ico',
                project_root / 'keydrop-icon.ico',
                project_root / 'icon.ico',
                project_root / 'bot-icone.png',
                project_root / 'keydrop-icon.png',
                project_root / 'icon.png'
            ]
            
            icon_path = None
            for path in possible_icons:
                if path.exists():
                    icon_path = str(path)
                    break
        
        if not icon_path or not os.path.exists(icon_path):
            print(f"⚠️ Ícone não encontrado: {icon_path}")
            return False
        
        # Configurar ícone baseado no sistema operacional e tipo de arquivo
        if icon_path.lower().endswith('.ico'):
            # Arquivo .ico (melhor para Windows)
            window.iconbitmap(icon_path)
            print(f"✅ Ícone .ico configurado: {icon_path}")
            return True
            
        elif icon_path.lower().endswith('.png'):
            # Arquivo .png (multiplataforma)
            try:
                icon_image = tk.PhotoImage(file=icon_path)
                window.iconphoto(True, icon_image)
                print(f"✅ Ícone .png configurado: {icon_path}")
                return True
            except Exception as e:
                print(f"❌ Erro ao configurar ícone .png: {e}")
                return False
        
        else:
            print(f"❌ Formato de ícone não suportado: {icon_path}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao configurar ícone: {e}")
        return False

def testar_icone():
    """Testa a configuração de ícone"""
    print("🎨 TESTE: Configuração de Ícone")
    print("=" * 50)
    
    # Criar janela de teste
    root = tk.Tk()
    root.title("Teste de Ícone - KeyDrop Bot")
    root.geometry("400x300")
    
    # Configurar ícone
    sucesso = configurar_icone(root)
    
    if sucesso:
        print("🎉 Ícone configurado com sucesso!")
        
        # Mostrar janela por 3 segundos
        label = tk.Label(
            root,
            text="🎨 Teste de Ícone\n\nVerifique se o ícone aparece\nna barra de título",
            font=("Arial", 12),
            justify="center"
        )
        label.pack(expand=True)
        
        root.after(3000, root.destroy)
        root.mainloop()
        
    else:
        print("❌ Falha ao configurar ícone")
        root.destroy()
    
    return sucesso

if __name__ == "__main__":
    testar_icone()
