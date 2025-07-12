#!/usr/bin/env python3
"""
Keydrop Bot Professional v2.1.0 - Versão Simplificada Funcional
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
import json
import time
from pathlib import Path
from input_utils import safe_int, safe_float, sanitize_str

class KeydropBotSimples:
    def __init__(self):
        # Criar janela principal
        self.root = tk.Tk()
        self.root.title("Keydrop Bot Professional v2.1.0")
        self.root.geometry("800x600")
        
        # Forçar aparecer
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
        
        # Centralizar
        try:
            self.root.eval('tk::PlaceWindow . center')
        except:
            pass
        
        # Diretório base
        if hasattr(sys, '_MEIPASS'):
            self.base_path = Path(sys.executable).parent
        else:
            self.base_path = Path(__file__).parent
        
        # Variáveis
        self.config_file = self.base_path / "config" / "bot_config.json"
        
        # Criar interface
        self.criar_interface()
        
        # Log inicial
        self.log("🎉 Keydrop Bot Professional v2.1.0 iniciado!")
        self.log("📱 Versão Desktop Simplificada Funcional")
        self.log("👨‍💻 Desenvolvido por: William Medrado")

    def criar_interface(self):
        """Criar interface simplificada"""
        # Header
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header, text="🤖 Keydrop Bot Professional v2.1.0", 
                 font=('Arial', 16, 'bold')).pack()
        ttk.Label(header, text="Desenvolvido por: William Medrado (wmedrado)").pack()
        ttk.Label(header, text="📱 Aplicação Desktop Funcional", 
                 foreground='blue').pack()
        
        # Notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba Controle
        controle_frame = ttk.Frame(notebook)
        notebook.add(controle_frame, text="🎮 Controle")
        
        # Info
        info_frame = ttk.LabelFrame(controle_frame, text="Informações", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(info_frame, text="✅ Interface gráfica funcionando").pack(anchor=tk.W)
        ttk.Label(info_frame, text="✅ Executável desktop nativo").pack(anchor=tk.W)
        ttk.Label(info_frame, text="✅ Sistema de configurações").pack(anchor=tk.W)
        ttk.Label(info_frame, text="✅ Monitoramento básico").pack(anchor=tk.W)
        
        # Botões
        botoes_frame = ttk.LabelFrame(controle_frame, text="Ações", padding=10)
        botoes_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(botoes_frame, text="💾 Salvar Config", 
                  command=self.salvar_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text="🔄 Recarregar", 
                  command=self.carregar_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(botoes_frame, text="🧹 Limpar Logs", 
                  command=self.limpar_logs).pack(side=tk.LEFT, padx=5)
        
        # Aba Configurações
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="⚙️ Configurações")
        
        config_basic = ttk.LabelFrame(config_frame, text="Configurações Básicas", padding=10)
        config_basic.pack(fill=tk.X, padx=10, pady=5)
        
        # Número de guias
        ttk.Label(config_basic, text="Número de Guias:").grid(row=0, column=0, sticky=tk.W)
        self.num_tabs_var = tk.StringVar(value="5")
        ttk.Entry(config_basic, textvariable=self.num_tabs_var, width=10).grid(row=0, column=1, padx=5)
        
        # Velocidade
        ttk.Label(config_basic, text="Velocidade (seg):").grid(row=1, column=0, sticky=tk.W)
        self.speed_var = tk.StringVar(value="3.0")
        ttk.Entry(config_basic, textvariable=self.speed_var, width=10).grid(row=1, column=1, padx=5)
        
        # Checkboxes
        self.headless_var = tk.BooleanVar()
        ttk.Checkbutton(config_basic, text="Modo Headless", 
                       variable=self.headless_var).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.mini_var = tk.BooleanVar()
        ttk.Checkbutton(config_basic, text="Modo Mini", 
                       variable=self.mini_var).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Aba Logs
        logs_frame = ttk.Frame(notebook)
        notebook.add(logs_frame, text="📝 Logs")
        
        # Área de logs
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=20, state=tk.DISABLED)
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status
        self.status_label = ttk.Label(self.root, text="Status: Pronto ✅")
        self.status_label.pack(side=tk.BOTTOM, pady=5)

    def log(self, message):
        """Adicionar mensagem aos logs"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.logs_text.config(state=tk.NORMAL)
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
        self.logs_text.config(state=tk.DISABLED)

    def salvar_config(self):
        """Salvar configurações"""
        try:
            config = {
                "num_tabs": safe_int(self.num_tabs_var.get(), 5),
                "speed": safe_float(self.speed_var.get(), 3.0),
                "headless": self.headless_var.get(),
                "mini": self.mini_var.get(),
            }
            
            self.config_file.parent.mkdir(exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            self.log("✅ Configurações salvas com sucesso!")
            messagebox.showinfo("Sucesso", "Configurações salvas!")
            
        except Exception as e:
            self.log(f"❌ Erro ao salvar: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")

    def carregar_config(self):
        """Carregar configurações"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                self.num_tabs_var.set(str(config.get("num_tabs", 5)))
                self.speed_var.set(str(config.get("speed", 3.0)))
                self.headless_var.set(config.get("headless", False))
                self.mini_var.set(config.get("mini", False))
                
                self.log("✅ Configurações carregadas!")
            else:
                self.log("ℹ️  Arquivo de config não existe, usando padrões")
                
        except Exception as e:
            self.log(f"❌ Erro ao carregar: {e}")

    def limpar_logs(self):
        """Limpar logs"""
        self.logs_text.config(state=tk.NORMAL)
        self.logs_text.delete(1.0, tk.END)
        self.logs_text.config(state=tk.DISABLED)
        self.log("🧹 Logs limpos")

    def run(self):
        """Executar aplicação"""
        self.carregar_config()
        self.root.mainloop()

def main():
    """Função principal simplificada"""
    try:
        print("Iniciando Keydrop Bot Professional...")
        
        # Verificar dependências básicas
        try:
            import psutil
            print("✅ psutil disponível")
        except ImportError:
            print("⚠️  psutil não disponível (opcional)")
        
        # Criar e executar app
        app = KeydropBotSimples()
        app.run()
        
        print("✅ Aplicação encerrada normalmente")
        
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            messagebox.showerror("Erro Fatal", f"Erro na aplicação:\n{e}")
        except:
            print("Erro ao mostrar messagebox")

if __name__ == "__main__":
    main()
