#!/usr/bin/env python3
"""
Debug Keydrop Bot - Testar criação da classe
"""

print("DEBUG: Iniciando teste da classe KeydropBotGUI...")

try:
    # Imports básicos (já testados e funcionam)
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    import threading
    import subprocess
    import sys
    import os
    import json
    import requests
    import time
    import logging
    import traceback
    from datetime import datetime
    from pathlib import Path
    import psutil
    
    print("DEBUG: Todos os imports OK")
    
    class KeydropBotGUI_Test:
        def __init__(self):
            print("DEBUG: Iniciando __init__ da classe...")
            
            # Teste 1: Criar root
            print("DEBUG: Criando tk.Tk()...")
            self.root = tk.Tk()
            print("DEBUG: tk.Tk() criado com sucesso")
            
            # Teste 2: Configurações básicas
            print("DEBUG: Aplicando configurações básicas...")
            self.root.title("Keydrop Bot Professional v2.1.0")
            self.root.geometry("900x700")
            self.root.resizable(True, True)
            print("DEBUG: Configurações básicas OK")
            
            # Teste 3: Forçar aparecer
            print("DEBUG: Forçando janela aparecer...")
            self.root.lift()
            self.root.attributes('-topmost', True)
            self.root.after(100, lambda: self.root.attributes('-topmost', False))
            print("DEBUG: Comandos de aparição OK")
            
            # Teste 4: Centralizar
            print("DEBUG: Centralizando...")
            try:
                self.root.eval('tk::PlaceWindow . center')
                print("DEBUG: Centralização OK")
            except:
                print("DEBUG: Erro na centralização (ignorado)")
            
            # Teste 5: Criar interface simples
            print("DEBUG: Criando interface simples...")
            label = tk.Label(self.root, text="🎯 TESTE DA CLASSE\n\nSe você vê esta tela,\na classe KeydropBotGUI\nestá funcionando!", 
                           font=('Arial', 12), justify=tk.CENTER, pady=20)
            label.pack(expand=True)
            
            tk.Button(self.root, text="Fechar", command=self.root.destroy, font=('Arial', 10)).pack(pady=10)
            print("DEBUG: Interface simples criada")
            
            print("DEBUG: __init__ concluído com sucesso!")
        
        def run(self):
            print("DEBUG: Iniciando mainloop...")
            self.root.mainloop()
            print("DEBUG: Mainloop finalizado")
    
    print("DEBUG: Criando instância da classe...")
    app = KeydropBotGUI_Test()
    
    print("DEBUG: Executando aplicação...")
    app.run()
    
    print("DEBUG: Teste concluído com sucesso!")
    
except Exception as e:
    print(f"DEBUG: ERRO detectado: {e}")
    traceback.print_exc()
    input("Pressione Enter para sair...")

print("DEBUG: Script finalizado")
