#!/usr/bin/env python3
"""
Debug extremo - Isolar problema
"""

print("DEBUG: Passo 1 - Script iniciado")

try:
    print("DEBUG: Passo 2 - Testando imports básicos")
    import sys
    import os
    print("DEBUG: Passo 3 - sys e os importados")
    
    from pathlib import Path
    print("DEBUG: Passo 4 - pathlib importado")
    
    import tkinter as tk
    print("DEBUG: Passo 5 - tkinter importado")
    
    print("DEBUG: Passo 6 - Testando psutil...")
    import psutil
    print("DEBUG: Passo 7 - psutil importado")
    
    print("DEBUG: Passo 8 - Testando requests...")
    import requests
    print("DEBUG: Passo 9 - requests importado")
    
    print("DEBUG: Passo 10 - Criando janela básica...")
    root = tk.Tk()
    root.title("DEBUG - Todos os imports OK")
    root.geometry("300x200")
    
    tk.Label(root, text="✅ Todos os imports funcionaram!\n\nO problema deve estar no código\ndo keydrop_bot_desktop.py", 
             justify=tk.CENTER, pady=20).pack(expand=True)
    
    tk.Button(root, text="Fechar", command=root.destroy).pack(pady=10)
    
    print("DEBUG: Passo 11 - Iniciando mainloop...")
    root.mainloop()
    print("DEBUG: Passo 12 - Mainloop concluído")
    
except Exception as e:
    print(f"DEBUG: ERRO no passo: {e}")
    import traceback
    traceback.print_exc()
    input("Pressione Enter para sair...")

print("DEBUG: Script finalizado")
