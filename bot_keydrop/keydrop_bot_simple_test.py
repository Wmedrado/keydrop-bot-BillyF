#!/usr/bin/env python3
"""
Keydrop Bot Professional v3.0.0 - Teste Simples
Versão simplificada para testar funcionalidade básica
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys
import os
import json
import time
from datetime import datetime

class KeydropBotSimple:
    def __init__(self):
        """Inicialização simples e robusta"""
        print("🎯 Iniciando Keydrop Bot Simple...")
        
        # Criar janela principal
        self.root = tk.Tk()
        self.root.title("Keydrop Bot Professional v3.0.0 - Teste")
        self.root.geometry("800x600")
        
        # Configurar tema simples
        self.setup_simple_theme()
        
        # Criar interface
        self.create_interface()
        
        # Mostrar janela
        self.root.lift()
        self.root.focus_force()
        
        print("✅ Interface criada com sucesso!")

    def setup_simple_theme(self):
        """Tema simples sem complicações"""
        self.root.configure(bg='#2d2d2d')

    def create_interface(self):
        """Criar interface simples"""
        # Header
        header = tk.Frame(self.root, bg='#2d2d2d')
        header.pack(fill='x', padx=10, pady=10)
        
        tk.Label(header, text="🤖 Keydrop Bot Professional v3.0.0", 
                font=('Arial', 16, 'bold'), bg='#2d2d2d', fg='#ffffff').pack()
        
        # Controles principais
        controls = tk.Frame(self.root, bg='#2d2d2d')
        controls.pack(fill='x', padx=10, pady=10)
        
        tk.Button(controls, text="🚀 TESTAR APLICAÇÃO", 
                 command=self.test_app, font=('Arial', 12, 'bold'),
                 bg='#4CAF50', fg='white', width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(controls, text="🌐 ABRIR KEYDROP", 
                 command=self.open_keydrop, font=('Arial', 12, 'bold'),
                 bg='#2196F3', fg='white', width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(controls, text="❌ FECHAR", 
                 command=self.root.destroy, font=('Arial', 12, 'bold'),
                 bg='#F44336', fg='white', width=15).pack(side=tk.RIGHT, padx=5)
        
        # Área de logs
        logs_frame = tk.Frame(self.root, bg='#2d2d2d')
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(logs_frame, text="📋 Log de Atividades", 
                font=('Arial', 12, 'bold'), bg='#2d2d2d', fg='#ffffff').pack(anchor='w')
        
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=20, 
                                                  font=('Consolas', 10), 
                                                  bg='#1e1e1e', fg='#ffffff')
        self.logs_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Log inicial
        self.log("🎉 Keydrop Bot Professional v3.0.0 carregado!")
        self.log("✅ Interface gráfica funcionando perfeitamente")
        self.log("🔧 Sistema pronto para testes")

    def log(self, message):
        """Adicionar mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
        print(f"LOG: {message}")

    def test_app(self):
        """Testar funcionalidades da aplicação"""
        self.log("🔄 Iniciando teste da aplicação...")
        
        # Teste 1: Verificar Python
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        self.log(f"🐍 Python {python_version} - OK")
        
        # Teste 2: Verificar Selenium
        try:
            import selenium
            self.log(f"🔧 Selenium {selenium.__version__} - OK")
        except ImportError:
            self.log("⚠️ Selenium não instalado - Instale com: pip install selenium")
        
        # Teste 3: Verificar psutil
        try:
            import psutil
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            self.log(f"💻 CPU: {cpu}% | RAM: {memory.percent}% - OK")
        except ImportError:
            self.log("⚠️ psutil não instalado - Instale com: pip install psutil")
        
        # Teste 4: Verificar requests
        try:
            import requests
            self.log(f"🌐 Requests - OK")
        except ImportError:
            self.log("⚠️ requests não instalado - Instale com: pip install requests")
        
        self.log("✅ Teste da aplicação concluído!")
        messagebox.showinfo("Teste Concluído", "Aplicação testada com sucesso!")

    def open_keydrop(self):
        """Abrir site do Keydrop"""
        self.log("🌐 Abrindo site do Keydrop...")
        try:
            import webbrowser
            webbrowser.open("https://key-drop.com/pt/giveaways/list")
            self.log("✅ Site aberto no navegador padrão")
        except Exception as e:
            self.log(f"❌ Erro ao abrir site: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir site:\n{e}")

    def run(self):
        """Executar aplicação"""
        self.log("🚀 Aplicação iniciada e funcionando!")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log("⏹️ Aplicação interrompida pelo usuário")
        except Exception as e:
            self.log(f"❌ Erro na aplicação: {e}")
            print(f"Erro crítico: {e}")

def main():
    """Função principal"""
    try:
        print("🎯 Iniciando teste simples do Keydrop Bot...")
        app = KeydropBotSimple()
        app.run()
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
