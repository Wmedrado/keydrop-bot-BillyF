#!/usr/bin/env python3
"""
Teste Simples - Verificar se executável funciona
"""

import tkinter as tk
import sys
import os
from pathlib import Path

def main():
    """Teste simples de executável"""
    try:
        print("TESTE: Iniciando...")
        
        # Criar janela simples
        root = tk.Tk()
        root.title("TESTE - Executável Funcionando")
        root.geometry("400x200")
        
        # Forçar aparecer
        root.lift()
        root.attributes('-topmost', True)
        root.after(100, lambda: root.attributes('-topmost', False))
        
        # Conteúdo
        label = tk.Label(root, text="✅ EXECUTÁVEL FUNCIONANDO!\n\nSe você vê esta janela,\no PyInstaller está OK.", 
                        font=('Arial', 12), justify=tk.CENTER, pady=20)
        label.pack(expand=True)
        
        # Informações de debug
        info_text = f"Executável: {hasattr(sys, '_MEIPASS')}\nDiretório: {os.getcwd()}"
        info_label = tk.Label(root, text=info_text, font=('Arial', 9), fg='gray')
        info_label.pack()
        
        # Botão fechar
        tk.Button(root, text="Fechar", command=root.destroy, font=('Arial', 10)).pack(pady=10)
        
        print("TESTE: Janela criada, iniciando mainloop...")
        root.mainloop()
        print("TESTE: Mainloop encerrado")
        
    except Exception as e:
        print(f"ERRO no teste: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
