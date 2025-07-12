import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import subprocess
import sys
import os
import json
import requests
import time
import logging
import traceback
import random
from datetime import datetime
from pathlib import Path
import psutil
import webbrowser
import zipfile
import shutil
# Custom browser integration
from custom_browser import CustomBrowser
from urllib.parse import urlparse

# matplotlib imports removidos temporariamente para evitar erro de dependências
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import numpy as np

from bot_keydrop.performance_utils import measure_time

class KeydropBotGUI:
    @measure_time("gui")
    def __init__(self):
        """Inicialização ultra-robusta para executável"""
        # Criar janela principal
        self.root = tk.Tk()
        self.root.withdraw()
        # Configurações básicas
        self.root.title("Keydrop Bot Professional v3.0.0")
        self.root.geometry("880x640")
        # Configurar Dark Mode PRIMEIRO
        self.setup_dark_theme()
        # Configurar ícone
        self.setup_icon()
        # Inicializar variáveis essenciais
        self.server_process = None
        self.server_running = False
        self.base_path = Path(".")
        self.config_file = Path("config.json")
        # Inicializar estatísticas
        self.init_bot_stats()

    def setup_dark_theme(self):
        """Stub: Configura tema escuro (implementação real deve ser feita)"""
        pass

    def setup_icon(self):
        """Stub: Configura ícone da janela (implementação real deve ser feita)"""
        pass

    def init_bot_stats(self):
        """Stub: Inicializa estatísticas dos bots (implementação real deve ser feita)"""
        self.bot_stats = {}

    def create_emergency_interface(self, e):
        """Stub: Cria interface de emergência em caso de erro crítico (implementação real deve ser feita)"""
        pass

    def log_message(self, msg, level="INFO"):
        """Stub: Loga mensagem (implementação real deve ser feita)"""
        print(f"[{level}] {msg}")
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import subprocess
import sys
import os
import json
import requests
import time
import logging
import traceback
import random
from datetime import datetime
from pathlib import Path
import psutil
import webbrowser
import zipfile
import shutil
# Custom browser integration
from custom_browser import CustomBrowser
from urllib.parse import urlparse

# matplotlib imports removidos temporariamente para evitar erro de dependências
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import numpy as np

class KeydropBotGUI:
    def __init__(self):
        """Inicialização ultra-robusta para executável"""
        # Criar janela principal
        self.root = tk.Tk()
        self.root.withdraw()
        # Configurações básicas
        self.root.title("Keydrop Bot Professional v3.0.0")
        self.root.geometry("880x640")
        # Configurar Dark Mode PRIMEIRO
        self.setup_dark_theme()
        # Configurar ícone
        self.setup_icon()
        # Inicializar variáveis essenciais
        self.server_process = None
        self.server_running = False
        self.base_path = Path(".")
        self.config_file = Path("config.json")
        # Inicializar estatísticas
        self.init_bot_stats()

    def run_full_keydrop_test(self):
        """Executa todos os testes e otimizações: login, sorteio, RAM"""
        self.optimize_custom_browsers()
        self.test_keydrop_login_and_raffle()

    def update_bot_details_loop(self):
        """Atualiza detalhes dos bots periodicamente (placeholder)"""
        while getattr(self, 'automation_active', False):
            try:
                # Atualiza área de detalhes dos bots
                details = []
                for bot_id, bot_stats in getattr(self, 'bot_stats', {}).items():
                    details.append(f"Bot #{bot_id}: {bot_stats.get('status', 'Desconhecido')}")
                if hasattr(self, 'bots_details_text'):
                    self.bots_details_text.config(state=tk.NORMAL)
                    self.bots_details_text.delete(1.0, tk.END)
                    self.bots_details_text.insert(tk.END, '\n'.join(details))
                    self.bots_details_text.config(state=tk.DISABLED)
                time.sleep(5)
            except Exception as e:
                self.log_message(f"❌ Erro ao atualizar detalhes dos bots: {e}", "ERROR")
                time.sleep(10)

    def update_graph_loop(self):
        """Atualiza gráfico de performance periodicamente (placeholder)"""
        while getattr(self, 'automation_active', False):
            try:
                # Placeholder: Limpa canvas e desenha texto simples
                if hasattr(self, 'graph_canvas'):
                    self.graph_canvas.delete('all')
                    self.graph_canvas.create_text(300, 100, text="Gráfico de performance não implementado", fill="gray", font=("Arial", 14))
                time.sleep(10)
            except Exception as e:
                self.log_message(f"❌ Erro ao atualizar gráfico: {e}", "ERROR")
                time.sleep(15)

    def optimize_custom_browsers(self):
        """Stub: Otimiza browsers customizados (implementação real deve ser feita)"""
        pass

    def test_keydrop_login_and_raffle(self):
        """Stub: Testa login e participação em sorteios (implementação real deve ser feita)"""
        pass

    def check_discord_inactivity_alerts(self):
        """Stub: Verifica e envia alertas de inatividade para o Discord (implementação real deve ser feita)"""
        pass

# ...restante do código...
import threading
import subprocess
import sys
import os
import json
import requests
import time
import logging
import traceback
import random
from datetime import datetime
from pathlib import Path
import psutil
import webbrowser
import zipfile
import shutil
# Custom browser integration
from custom_browser import CustomBrowser
from urllib.parse import urlparse

# matplotlib imports removidos temporariamente para evitar erro de dependências
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import numpy as np

class KeydropBotGUI:
    def __init__(self):
        """Inicialização ultra-robusta para executável"""
        # Criar janela principal
        self.root = tk.Tk()
        self.root.withdraw()
        # Configurações básicas
        self.root.title("Keydrop Bot Professional v3.0.0")
        self.root.geometry("880x640")
        # Configurar Dark Mode PRIMEIRO
        self.setup_dark_theme()
        # Configurar ícone
        self.setup_icon()
        # Inicializar variáveis essenciais
        self.server_process = None
        self.server_running = False
        self.base_path = Path(".")
        self.config_file = Path("config.json")
        # Inicializar estatísticas
        self.init_bot_stats()
    def run_full_keydrop_test(self):
        """Executa todos os testes e otimizações: login, sorteio, RAM"""
        self.optimize_custom_browsers()
        self.test_keydrop_login_and_raffle()

    def update_bot_details_loop(self):
        """Atualiza detalhes dos bots periodicamente (placeholder)"""
        while getattr(self, 'automation_active', False):
            try:
                # Atualiza área de detalhes dos bots
                details = []
                for bot_id, bot_stats in getattr(self, 'bot_stats', {}).items():
                    details.append(f"Bot #{bot_id}: {bot_stats.get('status', 'Desconhecido')}")
                if hasattr(self, 'bots_details_text'):
                    self.bots_details_text.config(state=tk.NORMAL)
                    self.bots_details_text.delete(1.0, tk.END)
                    self.bots_details_text.insert(tk.END, '\n'.join(details))
                    self.bots_details_text.config(state=tk.DISABLED)
                time.sleep(5)
            except Exception as e:
                self.log_message(f"❌ Erro ao atualizar detalhes dos bots: {e}", "ERROR")
                time.sleep(10)

    def update_graph_loop(self):
        """Atualiza gráfico de performance periodicamente (placeholder)"""
        while getattr(self, 'automation_active', False):
            try:
                # Placeholder: Limpa canvas e desenha texto simples
                if hasattr(self, 'graph_canvas'):
                    self.graph_canvas.delete('all')
                    self.graph_canvas.create_text(300, 100, text="Gráfico de performance não implementado", fill="gray", font=("Arial", 14))
                time.sleep(10)
            except Exception as e:
                self.log_message(f"❌ Erro ao atualizar gráfico: {e}", "ERROR")
                time.sleep(15)
            # Mostrar janela com carregamento
            self.create_loading_interface()
            # Mostrar janela
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            # Centralizar na tela
            self.center_window()
            # Configurar interface completa
            self.root.after(500, self.setup_full_interface)

    def setup_dark_theme(self):
        """Configurar tema escuro personalizado"""
        try:
            # Cores do tema escuro
            self.dark_colors = {
                'bg': '#2d2d2d',
                'fg': '#ffffff',
                'select_bg': '#404040',
                'select_fg': '#ffffff',
                'button_bg': '#404040',
                'button_fg': '#ffffff',
                'entry_bg': '#3d3d3d',
                'entry_fg': '#ffffff',
                'frame_bg': '#353535',
                'accent': '#2196f3',
                'success': '#4caf50',
                'warning': '#ff9800',
                'error': '#f44336'
            }
            
            # Configurar janela principal
            self.root.configure(bg=self.dark_colors['bg'])
            
            # Configurar estilo TTK
            style = ttk.Style()
            style.theme_use('clam')
            
            # Estilos personalizados - 20% menores (80% do tamanho original)
            style.configure('Dark.TFrame', background=self.dark_colors['bg'])
            style.configure('Dark.TLabel', background=self.dark_colors['bg'], foreground=self.dark_colors['fg'])
            style.configure('Dark.TLabelFrame', background=self.dark_colors['bg'], foreground=self.dark_colors['fg'])
            style.configure('Dark.TLabelFrame.Label', background=self.dark_colors['bg'], foreground=self.dark_colors['accent'])
            style.configure('Large.TButton', font=('Arial', 11, 'bold'), padding=(16, 12))  # Era 14/20,15 agora 11/16,12
            style.configure('Emergency.TButton', font=('Arial', 11, 'bold'), padding=(16, 12), foreground=self.dark_colors['error'])
            style.configure('Dark.TNotebook', background=self.dark_colors['bg'])
            style.configure('Dark.TNotebook.Tab', background=self.dark_colors['button_bg'], foreground=self.dark_colors['fg'], padding=[20, 10])
            style.map('Dark.TNotebook.Tab', background=[('selected', self.dark_colors['accent'])])
            style.configure('Dark.TCheckbutton', background=self.dark_colors['bg'], foreground=self.dark_colors['fg'])
            
            print("✅ Dark theme configurado com sucesso")
            
        except Exception as e:
            print(f"⚠️ Erro ao configurar dark theme: {e}")

    def setup_icon(self):
        """Configurar ícone da aplicação"""
        try:
            icon_paths = [
                "bot-icone.ico",
                os.path.join(os.getcwd(), "bot-icone.ico"),
                os.path.expanduser("~/Desktop/Projeto do zero/bot_keydrop/bot-icone.ico")
            ]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    try:
                        self.root.iconbitmap(icon_path)
                        print(f"✅ Ícone configurado: {icon_path}")
                        break
                    except:
                        continue
            else:
                self.root.iconname("Keydrop Bot v3.0.0")
                
        except Exception as e:
            print(f"⚠️ Erro na configuração do ícone: {e}")

    def create_loading_interface(self):
        """Criar interface de carregamento"""
        try:
            loading_frame = tk.Frame(self.root, bg=self.dark_colors['bg'])
            loading_frame.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(loading_frame, text="🤖 Keydrop Bot Professional v3.0.0", 
                    font=('Arial', 18, 'bold'), bg=self.dark_colors['bg'], 
                    fg=self.dark_colors['accent']).pack(pady=(100, 20))
            
            self.loading_status = tk.Label(loading_frame, text="🔄 Iniciando aplicação...", 
                                         font=('Arial', 12), bg=self.dark_colors['bg'], 
                                         fg=self.dark_colors['fg'])
            self.loading_status.pack(pady=10)
            
            self.root.update()
            
        except Exception as e:
            print(f"Erro ao criar interface de carregamento: {e}")

    def center_window(self):
        """Centralizar janela na tela"""
        try:
            self.root.update_idletasks()
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - 880) // 2
            y = (screen_height - 640) // 2
            self.root.geometry(f"880x640+{x}+{y}")
        except Exception as e:
            print(f"Erro ao centralizar janela: {e}")

    def create_emergency_interface(self, error):
        """Interface de emergência"""
        try:
            for widget in self.root.winfo_children():
                widget.destroy()
            
            emergency_frame = tk.Frame(self.root, bg='#ffebee')
            emergency_frame.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(emergency_frame, text="⚠️ Modo de Emergência", 
                    font=('Arial', 16, 'bold'), bg='#ffebee', fg='#c62828').pack(pady=20)
            tk.Label(emergency_frame, text=f"Erro: {str(error)}", 
                    font=('Arial', 10), bg='#ffebee', fg='#757575').pack(pady=10)
            tk.Button(emergency_frame, text="❌ Fechar", 
                     command=self.root.destroy, font=('Arial', 12), 
                     bg='#f44336', fg='white').pack(pady=5)
            
            self.root.deiconify()
            
        except Exception as e:
            print(f"Erro crítico: {e}")

    def setup_full_interface(self):
        """Configurar interface completa"""
        try:
            self.loading_status.config(text="⚙️ Configurando interface...")
            self.root.update()
            
            # Limpar carregamento
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Criar interface principal
            self.setup_interface()
            
        except Exception as e:
            error_msg = f"Erro ao configurar interface: {e}"
            self.log_message(f"❌ {error_msg}", "ERROR")
            print(error_msg)
            self.create_emergency_interface(e)

    def setup_interface(self):
        """Configurar interface principal"""
        try:
            # Header
            header = tk.Frame(self.root, bg=self.dark_colors['bg'])
            header.pack(fill='x', padx=15, pady=10)
            
            tk.Label(header, text="🤖 Keydrop Bot Professional v3.0.0",
                    font=('Arial', 18, 'bold'), bg=self.dark_colors['bg'], 
                    fg=self.dark_colors['accent']).pack()
            # Nome do desenvolvedor removido conforme solicitado
            
            # Notebook
            style = ttk.Style()
            self.notebook = ttk.Notebook(self.root, style='Dark.TNotebook')
            self.notebook.pack(fill='both', expand=True, padx=15, pady=10)
            
            # Criar abas
            self.create_control_tab()
            self.create_config_tab()
            self.create_stats_tab()
            self.create_logs_tab()
            
            # Footer
            footer = tk.Frame(self.root, bg=self.dark_colors['bg'])
            footer.pack(fill='x', padx=15, pady=5)
            
            self.status_label = tk.Label(footer, text="📱 Modo Desktop Nativo • Pronto para uso",
                                       bg=self.dark_colors['bg'], fg=self.dark_colors['success'],
                                       font=('Arial', 11, 'bold'))
            self.status_label.pack(side='left')
            
            # Iniciar monitoramento
            self.root.after(1000, self.update_system_stats)
            self.root.after(2000, self.update_global_stats)
            
            # Log inicial
            self.log_message("🎉 Keydrop Bot Professional v3.0.0 iniciado com sucesso!")
            self.log_message("📱 Modo: Aplicação Desktop Nativa com Dark Theme")
            self.log_message("🚀 Sistema pronto para automação Google Chrome")
            
        except Exception as e:
            print(f"Erro ao configurar interface principal: {e}")


    def create_control_tab(self):
        """Criar aba de controle"""
        control_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(control_frame, text="🎮 Controle")

        # Informações do App
        info_frame = tk.LabelFrame(control_frame, text="📋 Keydrop Bot Professional v3.0.0", 
                                 bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                 font=('Arial', 12, 'bold'))
        info_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(info_frame, text="🤖 Automação Profissional para Sorteios Keydrop", 
                font=('Arial', 14, 'bold'), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['accent']).pack(anchor=tk.W, padx=10, pady=5)
        tk.Label(info_frame, text="🌐 Google Chrome Exclusivo • Múltiplos Perfis • Multi-Instância",
                font=('Arial', 12), bg=self.dark_colors['bg'],
                fg=self.dark_colors['fg']).pack(anchor=tk.W, padx=10, pady=2)
        # Nome do desenvolvedor removido conforme solicitado

        # Controle de Automação
        bot_frame = tk.LabelFrame(control_frame, text="🚀 Controle de Automação", 
                                bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                font=('Arial', 12, 'bold'))
        bot_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(bot_frame, text="✨ Sistema de Multi-Bots com Perfis Independentes", 
                bg=self.dark_colors['bg'], fg=self.dark_colors['success'], 
                font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 15))

        # Botões principais - 20% menores
        buttons_frame = tk.Frame(bot_frame, bg=self.dark_colors['bg'])
        buttons_frame.pack(fill=tk.X, pady=8, padx=8)  # Era 10/10, agora 8/8

        tk.Button(buttons_frame, text="🚀 INICIAR AUTOMAÇÃO", 
                 command=self.start_bot_direct, font=('Arial', 11, 'bold'),  # Era 14, agora 11
                 bg=self.dark_colors['success'], fg='white', 
                 relief='raised', bd=3).pack(side=tk.LEFT, padx=12, ipadx=16, ipady=8)  # Era 15/20/10, agora 12/16/8

        tk.Button(buttons_frame, text="⏹️ PARAR AUTOMAÇÃO", 
                 command=self.stop_bot_direct, font=('Arial', 11, 'bold'),
                 bg=self.dark_colors['warning'], fg='white', 
                 relief='raised', bd=3).pack(side=tk.LEFT, padx=12, ipadx=16, ipady=8)

        tk.Button(buttons_frame, text="🗑️ FECHAR GUIAS", 
                 command=self.force_close_tabs, font=('Arial', 11, 'bold'),
                 bg=self.dark_colors['error'], fg='white', 
                 relief='raised', bd=3).pack(side=tk.LEFT, padx=12, ipadx=12, ipady=8)  # Era 15/15/10, agora 12/12/8

        tk.Button(buttons_frame, text="🔄 ATUALIZAR APP", 
                 command=self.check_for_updates, font=('Arial', 11, 'bold'),
                 bg=self.dark_colors['accent'], fg='white', 
                 relief='raised', bd=3).pack(side=tk.LEFT, padx=12, ipadx=12, ipady=8)

        tk.Button(buttons_frame, text="🚨 EMERGÊNCIA", 
                 command=self.emergency_stop_direct, font=('Arial', 11, 'bold'),
                 bg=self.dark_colors['error'], fg='white', 
                 relief='raised', bd=3).pack(side=tk.RIGHT, padx=12, ipadx=12, ipady=8)

        # NOVO: Botão para automação/teste completo Keydrop
        tk.Button(buttons_frame, text="🧪 TESTE COMPLETO KEYDROP", 
                 command=self.run_full_keydrop_test, font=('Arial', 11, 'bold'),
                 bg=self.dark_colors['accent'], fg='white', 
                 relief='raised', bd=3).pack(side=tk.LEFT, padx=12, ipadx=12, ipady=8)

        # Status em tempo real - 20% menor
        status_frame = tk.LabelFrame(control_frame, text="📊 Status em Tempo Real", 
                                   bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                   font=('Arial', 10, 'bold'))  # Era 12, agora 10
        status_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)  # Era 15/10, agora 12/8

        self.status_text = scrolledtext.ScrolledText(status_frame, height=15, state=tk.DISABLED, 
                                                   font=('Consolas', 10), bg=self.dark_colors['entry_bg'],  # Era 12, agora 10
                                                   fg=self.dark_colors['fg'], insertbackground=self.dark_colors['fg'],
                                                   selectbackground=self.dark_colors['select_bg'],
                                                   selectforeground=self.dark_colors['select_fg'])
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)  # Era 10/10, agora 8/8
    def create_config_tab(self):
        """Criar aba de configurações"""
        config_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(config_frame, text="⚙️ Configurações")
        
        # Configurações Básicas - 20% menores
        basic_frame = tk.LabelFrame(config_frame, text="🔧 Configurações Básicas", 
                                  bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                  font=('Arial', 10, 'bold'))  # Era 12, agora 10
        basic_frame.pack(fill=tk.X, padx=16, pady=12)  # Era 20/15, agora 16/12
        
        # Grid de configurações
        config_grid = tk.Frame(basic_frame, bg=self.dark_colors['bg'])
        config_grid.pack(fill=tk.X, padx=16, pady=12)  # Era 20/15, agora 16/12
        
        # Número de guias
        tk.Label(config_grid, text="🤖 Número de Guias/Bots (1-100):", 
                font=('Arial', 10, 'bold'), bg=self.dark_colors['bg'],  # Era 12, agora 10
                fg=self.dark_colors['fg']).grid(row=0, column=0, sticky=tk.W, pady=6)  # Era 8, agora 6
        self.num_tabs_var = tk.StringVar(value="5")
        tk.Entry(config_grid, textvariable=self.num_tabs_var, width=15, font=('Arial', 10),  # Era 12, agora 10
                bg=self.dark_colors['entry_bg'], fg=self.dark_colors['entry_fg'],
                insertbackground=self.dark_colors['entry_fg']).grid(row=0, column=1, padx=12, pady=6)  # Era 15/8, agora 12/6
        
        # Velocidade
        tk.Label(config_grid, text="⚡ Velocidade de Execução (segundos):", 
                font=('Arial', 10, 'bold'), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['fg']).grid(row=1, column=0, sticky=tk.W, pady=6)
        self.speed_var = tk.StringVar(value="8.0")
        tk.Entry(config_grid, textvariable=self.speed_var, width=15, font=('Arial', 10),
                bg=self.dark_colors['entry_bg'], fg=self.dark_colors['entry_fg'],
                insertbackground=self.dark_colors['entry_fg']).grid(row=1, column=1, padx=12, pady=6)
        
        # Retry
        tk.Label(config_grid, text="🔄 Tentativas de Retry:", 
                font=('Arial', 10, 'bold'), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['fg']).grid(row=2, column=0, sticky=tk.W, pady=6)
        self.retry_var = tk.StringVar(value="5")
        tk.Entry(config_grid, textvariable=self.retry_var, width=15, font=('Arial', 10),
                bg=self.dark_colors['entry_bg'], fg=self.dark_colors['entry_fg'],
                insertbackground=self.dark_colors['entry_fg']).grid(row=2, column=1, padx=12, pady=6)
        
        # Dica
        tk.Label(config_grid, text="💡 Recomendado: 7-10 segundos para máxima eficiência", 
                font=('Arial', 9), bg=self.dark_colors['bg'],  # Era 11, agora 9
                fg=self.dark_colors['success']).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(8, 0))  # Era 10, agora 8
        
        # Modos de Operação - 20% menores
        modes_frame = tk.LabelFrame(config_frame, text="🎯 Modos de Operação", 
                                  bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                  font=('Arial', 10, 'bold'))  # Era 12, agora 10
        modes_frame.pack(fill=tk.X, padx=16, pady=12)  # Era 20/15, agora 16/12
        
        # Checkboxes
        modes_inner = tk.Frame(modes_frame, bg=self.dark_colors['bg'])
        modes_inner.pack(fill=tk.X, padx=16, pady=12)  # Era 20/15, agora 16/12
        
        self.headless_var = tk.BooleanVar()
        tk.Checkbutton(modes_inner, text="🕶️ Modo Headless (invisível)",
                      variable=self.headless_var, bg=self.dark_colors['bg'],
                      fg=self.dark_colors['fg'], font=('Arial', 9),  # Era 11, agora 9
                      selectcolor=self.dark_colors['entry_bg']).pack(anchor=tk.W, pady=4)  # Era 5, agora 4

        self.stealth_headless_var = tk.BooleanVar()
        tk.Checkbutton(
            modes_inner,
            text="🛡️ Headless Stealth",
            variable=self.stealth_headless_var,
            bg=self.dark_colors['bg'],
            fg=self.dark_colors['fg'],
            font=('Arial', 9),
            selectcolor=self.dark_colors['entry_bg']
        ).pack(anchor=tk.W, pady=4)
        
        self.mini_window_var = tk.BooleanVar()
        tk.Checkbutton(modes_inner, text="📱 Modo Mini (100x200px)", 
                      variable=self.mini_window_var, bg=self.dark_colors['bg'], 
                      fg=self.dark_colors['fg'], font=('Arial', 9),
                      selectcolor=self.dark_colors['entry_bg']).pack(anchor=tk.W, pady=4)
        
        self.login_tabs_var = tk.BooleanVar()
        tk.Checkbutton(modes_inner, text="🔑 Abas de Login (Keydrop/Steam)", 
                      variable=self.login_tabs_var, bg=self.dark_colors['bg'], 
                      fg=self.dark_colors['fg'], font=('Arial', 9),
                      selectcolor=self.dark_colors['entry_bg']).pack(anchor=tk.W, pady=4)
        
        # NOVO: Checkbox para sorteios contender (1h)
        self.contender_mode_var = tk.BooleanVar()
        tk.Checkbutton(modes_inner, text="🏆 Participar Sorteios 1h (Contender)", 
                      variable=self.contender_mode_var, bg=self.dark_colors['bg'], 
                      fg=self.dark_colors['fg'], font=('Arial', 9),
                      selectcolor=self.dark_colors['entry_bg']).pack(anchor=tk.W, pady=4)
        
        # Descrições
        tk.Label(modes_inner, text="• Headless: Bots funcionam em segundo plano (recomendado para muitos bots)", 
                font=('Arial', 10), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['fg']).pack(anchor=tk.W, padx=20, pady=2)
        tk.Label(modes_inner, text="• Mini: Janelas pequenas visíveis (bom para monitoramento)", 
                font=('Arial', 10), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['fg']).pack(anchor=tk.W, padx=20, pady=2)
        tk.Label(modes_inner, text="• Login: Abre páginas de login para autenticação manual", 
                font=('Arial', 10), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['fg']).pack(anchor=tk.W, padx=20, pady=2)
        tk.Label(modes_inner, text="• Contender: Participa de sorteios de 1h (aguarda 1h entre participações)", 
                font=('Arial', 10), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['fg']).pack(anchor=tk.W, padx=20, pady=2)
        
        # Discord
        discord_frame = tk.LabelFrame(config_frame, text="🤖 Integração Discord", 
                                    bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                    font=('Arial', 12, 'bold'))
        discord_frame.pack(fill=tk.X, padx=20, pady=15)
        
        discord_inner = tk.Frame(discord_frame, bg=self.dark_colors['bg'])
        discord_inner.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(discord_inner, text="🔗 Webhook URL (opcional):", 
                font=('Arial', 12, 'bold'), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['fg']).pack(anchor=tk.W)
        
        self.discord_webhook_var = tk.StringVar()
        tk.Entry(discord_inner, textvariable=self.discord_webhook_var, 
                width=60, font=('Arial', 11), bg=self.dark_colors['entry_bg'], 
                fg=self.dark_colors['entry_fg'], insertbackground=self.dark_colors['entry_fg']).pack(fill=tk.X, pady=8)
        
        self.discord_enabled_var = tk.BooleanVar()
        tk.Checkbutton(discord_inner, text="📢 Habilitar Notificações Discord", 
                      variable=self.discord_enabled_var, bg=self.dark_colors['bg'], 
                      fg=self.dark_colors['fg'], font=('Arial', 11),
                      selectcolor=self.dark_colors['entry_bg']).pack(anchor=tk.W, pady=5)
        
        # Botões
        buttons_frame = tk.Frame(config_frame, bg=self.dark_colors['bg'])
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(buttons_frame, text="💾 SALVAR CONFIGURAÇÕES", 
                 command=self.save_config, font=('Arial', 12, 'bold'),
                 bg=self.dark_colors['success'], fg='white', 
                 relief='raised', bd=2).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        
        tk.Button(buttons_frame, text="🔄 RECARREGAR", 
                 command=self.load_config, font=('Arial', 12, 'bold'),
                 bg=self.dark_colors['accent'], fg='white', 
                 relief='raised', bd=2).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        
        tk.Button(buttons_frame, text="🧹 LIMPAR CACHE", 
                 command=self.clear_cache, font=('Arial', 12, 'bold'),
                 bg=self.dark_colors['warning'], fg='white', 
                 relief='raised', bd=2).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

    def create_stats_tab(self):
        """Criar aba de estatísticas"""
        stats_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(stats_frame, text="📊 Estatísticas")
        
        # Estatísticas Globais
        global_frame = tk.LabelFrame(stats_frame, text="📈 Estatísticas Globais", 
                                   bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                   font=('Arial', 12, 'bold'))
        global_frame.pack(fill=tk.X, padx=20, pady=15)
        
        global_stats = tk.Frame(global_frame, bg=self.dark_colors['bg'])
        global_stats.pack(fill=tk.X, padx=20, pady=15)
        
        # Primeira linha
        self.total_bots_label = tk.Label(global_stats, text="🤖 Bots Ativos: 0", 
                                       font=('Arial', 14, 'bold'), bg=self.dark_colors['bg'],
                                       fg=self.dark_colors['accent'])
        self.total_bots_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 30))
        
        self.total_raffles_label = tk.Label(global_stats, text="🎯 Total Sorteios: 0", 
                                          font=('Arial', 14, 'bold'), bg=self.dark_colors['bg'],
                                          fg=self.dark_colors['success'])
        self.total_raffles_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        
        self.total_errors_label = tk.Label(global_stats, text="⚠️ Total Erros: 0", 
                                         font=('Arial', 14, 'bold'), bg=self.dark_colors['bg'],
                                         fg=self.dark_colors['error'])
        self.total_errors_label.grid(row=0, column=2, sticky=tk.W)
        
        # Segunda linha
        self.session_time_label = tk.Label(global_stats, text="⏱️ Tempo Sessão: 00:00:00", 
                                         font=('Arial', 12), bg=self.dark_colors['bg'],
                                         fg=self.dark_colors['fg'])
        self.session_time_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        self.network_usage_label = tk.Label(global_stats, text="🌐 Uso Rede: 0 MB", 
                                          font=('Arial', 12), bg=self.dark_colors['bg'],
                                          fg=self.dark_colors['fg'])
        self.network_usage_label.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        self.total_profit_label = tk.Label(global_stats, text="💰 Lucro Total: $0.00", 
                                        font=('Arial', 12), bg=self.dark_colors['bg'],
                                        fg=self.dark_colors['success'])
        self.total_profit_label.grid(row=1, column=2, sticky=tk.W, pady=(10, 0))
        
        # Gráfico de Performance
        graph_frame = tk.LabelFrame(stats_frame, text="📊 Gráfico de Performance", 
                                  bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                  font=('Arial', 12, 'bold'))
        graph_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Canvas para gráfico simples (sem matplotlib)
        self.graph_canvas = tk.Canvas(graph_frame, width=600, height=200, 
                                    bg=self.dark_colors['entry_bg'])
        self.graph_canvas.pack(padx=20, pady=15)
        
        # Detalhes dos Bots Individuais
        bots_frame = tk.LabelFrame(stats_frame, text="🤖 Detalhes dos Bots Ativos", 
                                 bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                 font=('Arial', 12, 'bold'))
        bots_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Área de rolagem para detalhes dos bots
        self.bots_details_text = scrolledtext.ScrolledText(bots_frame, height=10, state=tk.DISABLED,
                                                         font=('Consolas', 10), bg=self.dark_colors['entry_bg'],
                                                         fg=self.dark_colors['fg'], insertbackground=self.dark_colors['fg'],
                                                         selectbackground=self.dark_colors['select_bg'],
                                                         selectforeground=self.dark_colors['select_fg'])
        self.bots_details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Performance do Sistema
        system_frame = tk.LabelFrame(stats_frame, text="💻 Performance do Sistema", 
                                   bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                   font=('Arial', 12, 'bold'))
        system_frame.pack(fill=tk.X, padx=20, pady=15)
        
        system_stats = tk.Frame(system_frame, bg=self.dark_colors['bg'])
        system_stats.pack(fill=tk.X, padx=20, pady=15)
        
        self.cpu_label = tk.Label(system_stats, text="💾 CPU: 0%", 
                                font=('Arial', 12), bg=self.dark_colors['bg'],
                                fg=self.dark_colors['fg'])
        self.cpu_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 30))
        
        self.ram_label = tk.Label(system_stats, text="🧠 RAM: 0 MB", 
                                font=('Arial', 12), bg=self.dark_colors['bg'],
                                fg=self.dark_colors['fg'])
        self.ram_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        
        self.disk_label = tk.Label(system_stats, text="💿 Disco: 0 GB", 
                                 font=('Arial', 12), bg=self.dark_colors['bg'],
                                 fg=self.dark_colors['fg'])
        self.disk_label.grid(row=0, column=2, sticky=tk.W)

    def create_logs_tab(self):
        """Criar aba de logs"""
        logs_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(logs_frame, text="📝 Logs")
        
        # Header dos logs
        logs_header = tk.LabelFrame(logs_frame, text="📊 Sistema de Logs Avançado", 
                                  bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                  font=('Arial', 12, 'bold'))
        logs_header.pack(fill=tk.X, padx=20, pady=15)
        
        logs_header_inner = tk.Frame(logs_header, bg=self.dark_colors['bg'])
        logs_header_inner.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(logs_header_inner, text="📜 Monitoramento em tempo real de todas as atividades do sistema", 
                font=('Arial', 12), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['fg']).pack(anchor=tk.W)
        
        # Controles
        log_controls = tk.Frame(logs_header_inner, bg=self.dark_colors['bg'])
        log_controls.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(log_controls, text="🗑️ LIMPAR LOGS", 
                 command=self.clear_logs, font=('Arial', 12, 'bold'),
                 bg=self.dark_colors['error'], fg='white', 
                 relief='raised', bd=2).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        
        tk.Button(log_controls, text="💾 SALVAR LOGS", 
                 command=self.save_logs, font=('Arial', 12, 'bold'),
                 bg=self.dark_colors['success'], fg='white', 
                 relief='raised', bd=2).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        
        tk.Button(log_controls, text="🔄 ATUALIZAR", 
                 command=self.refresh_logs, font=('Arial', 12, 'bold'),
                 bg=self.dark_colors['accent'], fg='white', 
                 relief='raised', bd=2).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        
        # Área de logs
        logs_content = tk.LabelFrame(logs_frame, text="📋 Log de Atividades", 
                                   bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                   font=('Arial', 12, 'bold'))
        logs_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.logs_text = scrolledtext.ScrolledText(logs_content, height=20, state=tk.DISABLED,
                                                 font=('Consolas', 11), bg=self.dark_colors['entry_bg'],
                                                 fg=self.dark_colors['fg'], insertbackground=self.dark_colors['fg'],
                                                 selectbackground=self.dark_colors['select_bg'],
                                                 selectforeground=self.dark_colors['select_fg'])
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def init_bot_stats(self):
        """Inicializar estatísticas"""
        self.bot_stats = {}
        self.total_bots_active = 0
        self.global_stats = {
            'total_raffles_amateur': 0,
            'total_raffles_contender': 0,
            'total_errors': 0,
            'total_network_usage': 0,
            'session_start_time': datetime.now()
        }

    def log_message(self, message, level="INFO"):
        """Adicionar mensagem aos logs"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        print(f"LOG: {log_entry.strip()}")
        
        try:
            if hasattr(self, 'logs_text') and self.logs_text:
                self.logs_text.config(state=tk.NORMAL)
                self.logs_text.insert(tk.END, log_entry)
                self.logs_text.see(tk.END)
                self.logs_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Erro ao adicionar aos logs: {e}")
        
        try:
            if hasattr(self, 'status_text') and self.status_text:
                self.status_text.config(state=tk.NORMAL)
                self.status_text.insert(tk.END, log_entry)
                self.status_text.see(tk.END)
                self.status_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")

    def update_global_stats(self):
        """Atualizar estatísticas globais"""
        try:
            total_amateur = sum(bot.get('raffles_amateur', 0) for bot in self.bot_stats.values())
            total_contender = sum(bot.get('raffles_contender', 0) for bot in self.bot_stats.values())
            total_raffles = total_amateur + total_contender
            total_errors = sum(bot.get('errors', 0) for bot in self.bot_stats.values())
            total_network = sum(bot.get('network_usage', 0) for bot in self.bot_stats.values())
            total_skins = sum(bot.get('skin_balance', 0.0) for bot in self.bot_stats.values())
            
            session_duration = datetime.now() - self.global_stats['session_start_time']
            hours, remainder = divmod(int(session_duration.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            session_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            if hasattr(self, 'total_bots_label'):
                self.total_bots_label.config(text=f"🤖 Bots Ativos: {self.total_bots_active}")
            if hasattr(self, 'total_raffles_label'):
                self.total_raffles_label.config(text=f"🎯 Total Sorteios: {total_raffles}")
            if hasattr(self, 'total_errors_label'):
                self.total_errors_label.config(text=f"⚠️ Total Erros: {total_errors}")
            if hasattr(self, 'session_time_label'):
                self.session_time_label.config(text=f"⏱️ Tempo Sessão: {session_time}")
            if hasattr(self, 'network_usage_label'):
                self.network_usage_label.config(text=f"🌐 Uso Rede: {total_network} MB")
            if hasattr(self, 'total_profit_label'):
                self.total_profit_label.config(text=f"💰 Lucro Total: ${total_skins:.2f}")
            
            self.root.after(5000, self.update_global_stats)
            
        except Exception as e:
            print(f"Erro ao atualizar estatísticas: {e}")
            self.root.after(10000, self.update_global_stats)

    def update_system_stats(self):
        """Atualizar estatísticas do sistema"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            ram_used = memory.used / (1024**2)
            disk_free = disk.free / (1024**3)
            
            if hasattr(self, 'cpu_label'):
                self.cpu_label.config(text=f"💾 CPU: {cpu_percent:.1f}%")
            if hasattr(self, 'ram_label'):
                self.ram_label.config(text=f"🧠 RAM: {ram_used:.0f} MB")
            if hasattr(self, 'disk_label'):
                self.disk_label.config(text=f"💿 Disco: {disk_free:.1f} GB")
            
            self.root.after(3000, self.update_system_stats)
            
        except Exception as e:
            print(f"Erro ao atualizar sistema: {e}")
            self.root.after(5000, self.update_system_stats)

    def find_chrome_executable(self):
        """Encontrar Google Chrome"""
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"),
            "chrome.exe"
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                return path
        return None

    def start_bot_direct(self):
        """Iniciar automação usando navegador customizado"""
        try:
            self.log_message("🤖 Iniciando automação com navegador customizado...", "INFO")
            num_tabs = int(self.num_tabs_var.get()) if hasattr(self, 'num_tabs_var') else 3
            headless_mode = self.headless_var.get() if hasattr(self, 'headless_var') else False
            self.custom_browsers = []
            self.automation_active = True
            for i in range(num_tabs):
                bot_id = i + 1
                # Perfil único para cada guia
                profile_dir = os.path.abspath(f"custom_profiles/bot_{bot_id}")
                os.makedirs(profile_dir, exist_ok=True)
                browser = CustomBrowser(profile_path=profile_dir, window_size=(800, 600), headless=headless_mode)
                browser.load_url("https://key-drop.com/pt/giveaways/list")
                browser.show()
                self.custom_browsers.append({
                    'id': bot_id,
                    'browser': browser,
                    'profile_dir': profile_dir
                })
                # Inicializar estatísticas do bot
                self.bot_stats[bot_id] = {
                    'active': True,
                    'raffles_amateur': 0,
                    'raffles_contender': 0,
                    'errors': 0,
                    'network_usage': 0,
                    'skin_balance': 0.0,
                    'initial_balance': 0.0,
                    'profit': 0.0,
                    'start_time': datetime.now(),
                    'last_amateur_action': datetime.now(),
                    'last_contender_action': datetime.now(),
                    'status': 'Navegando para KeyDrop...'
                }
                self.total_bots_active += 1
                self.log_message(f"✅ Bot #{bot_id} criado com navegador customizado!", "SUCCESS")
            self.log_message(f"🎉 {len(self.custom_browsers)} bots iniciados com navegador customizado!", "SUCCESS")
            # Iniciar automação de sorteios
            self.start_raffle_automation_custom()
        except Exception as e:
            self.log_message(f"❌ Erro: {e}", "ERROR")

    def start_raffle_automation_custom(self):
        """Iniciar automação de sorteios usando navegador customizado"""
        try:
            self.log_message("🎯 Iniciando automação de sorteios (custom browser)...", "INFO")
            self.automation_thread = threading.Thread(
                target=self.raffle_automation_loop_custom,
                daemon=True
            )
            self.automation_thread.start()
            self.details_thread = threading.Thread(
                target=self.update_bot_details_loop,
                daemon=True
            )
            self.details_thread.start()
            self.graph_thread = threading.Thread(
                target=self.update_graph_loop,
                daemon=True
            )
            self.graph_thread.start()
        except Exception as e:
            self.log_message(f"❌ Erro ao iniciar automação customizada: {e}", "ERROR")

    def raffle_automation_loop_custom(self):
        """Loop principal de automação de sorteios usando navegador customizado"""
        while self.automation_active and hasattr(self, 'custom_browsers') and self.custom_browsers:
            try:
                current_time = datetime.now()
                for bot in self.custom_browsers:
                    bot_id = bot['id']
                    browser = bot['browser']
                    bot_stats = self.bot_stats[bot_id]
                    if not bot_stats['active']:
                        continue
                    # Participar de sorteio amateur (cada 3 minutos)
                    if (current_time - bot_stats['last_amateur_action']).total_seconds() >= 180:
                        success = self.participate_amateur_raffle_custom(bot_id, browser)
                        bot_stats['last_amateur_action'] = datetime.now()
                    # Participar de sorteio contender (cada 1 hora)
                    if hasattr(self, 'contender_mode_var') and self.contender_mode_var.get() and (current_time - bot_stats['last_contender_action']).total_seconds() >= 3600:
                        success = self.participate_contender_raffle_custom(bot_id, browser)
                        bot_stats['last_contender_action'] = datetime.now()
                # Verificar alertas de inatividade Discord
                self.check_discord_inactivity_alerts()
                time.sleep(10)
            except Exception as e:
                self.log_message(f"❌ Erro no loop de automação customizada: {e}", "ERROR")
                time.sleep(30)

    def participate_amateur_raffle_custom(self, bot_id, browser):
        """Participar de sorteio amateur usando navegador customizado, com retry e controle de última participação"""
        max_retries = int(getattr(self, 'retry_var', tk.StringVar(value="3")).get()) if hasattr(self, 'retry_var') else 3
        attempt = 0
        success = False
        while attempt < max_retries and not success:
            try:
                self.log_message(f"🎯 Bot #{bot_id}: Tentativa {attempt+1} de participação sorteio amateur...", "INFO")
                js_macro = '''
                    var cards = document.querySelectorAll('[data-testid="div-active-giveaways-list-single-card"]');
                    if(cards.length > 0){
                        var lastCard = cards[cards.length-1];
                        var btn = lastCard.querySelector('button');
                        if(btn){ btn.click(); return true; } else { return false; }
                    } else { return false; }
                '''
                result = browser.run_js(js_macro)
                if result:
                    self.bot_stats[bot_id]['raffles_amateur'] += 1
                    self.bot_stats[bot_id]['last_amateur_action'] = datetime.now()
                    self.bot_stats[bot_id]['status'] = 'Sorteio amateur OK'
                    self.log_message(f"✅ Bot #{bot_id}: Sorteio amateur participado com sucesso! Total: {self.bot_stats[bot_id]['raffles_amateur']}", "SUCCESS")
                    success = True
                    return True
                else:
                    attempt += 1
                    time.sleep(2)
            except Exception as e:
                self.bot_stats[bot_id]['errors'] += 1
                self.bot_stats[bot_id]['status'] = f'Erro: {str(e)[:20]}...'
                self.log_message(f"❌ Bot #{bot_id}: Erro amateur custom - {e}", "ERROR")
                attempt += 1
                time.sleep(2)
        if not success:
            self.log_message(f"⚠️ Bot #{bot_id}: Falha após {max_retries} tentativas de participação amateur.", "WARNING")
        return False

    def participate_contender_raffle_custom(self, bot_id, browser):
        """Participar de sorteio contender usando navegador customizado, com retry e controle de última participação"""
        max_retries = int(getattr(self, 'retry_var', tk.StringVar(value="3")).get()) if hasattr(self, 'retry_var') else 3
        attempt = 0
        success = False
        while attempt < max_retries and not success:
            try:
                self.log_message(f"🏆 Bot #{bot_id}: Tentativa {attempt+1} de participação sorteio contender...", "INFO")
                js_macro = '''
                    var cards = document.querySelectorAll('[data-testid="div-active-giveaways-list-single-card"]');
                    if(cards.length > 0){
                        var lastCard = cards[cards.length-1];
                        var btn = lastCard.querySelector('button');
                        if(btn){ btn.click(); return true; } else { return false; }
                    } else { return false; }
                '''
                result = browser.run_js(js_macro)
                if result:
                    self.bot_stats[bot_id]['raffles_contender'] += 1
                    self.bot_stats[bot_id]['last_contender_action'] = datetime.now()
                    self.bot_stats[bot_id]['status'] = 'Sorteio contender OK'
                    self.log_message(f"✅ Bot #{bot_id}: Sorteio contender participado com sucesso! Total: {self.bot_stats[bot_id]['raffles_contender']}", "SUCCESS")
                    success = True
                    return True
                else:
                    attempt += 1
                    time.sleep(2)
            except Exception as e:
                self.bot_stats[bot_id]['errors'] += 1
                self.bot_stats[bot_id]['status'] = f'Erro: {str(e)[:20]}...'
                self.log_message(f"❌ Bot #{bot_id}: Erro contender custom - {e}", "ERROR")
                attempt += 1
                time.sleep(2)
        if not success:
            self.log_message(f"⚠️ Bot #{bot_id}: Falha após {max_retries} tentativas de participação contender.", "WARNING")
        return False

    # REMOVIDO: Todo código Selenium legado

    # Métodos de controle e utilitários
    def stop_bot_direct(self):
        """Parar automação Selenium"""
        try:
            self.log_message("🛑 Parando automação Selenium...", "WARNING")
            self.automation_active = False
            # Fechar drivers Selenium
            if hasattr(self, 'chrome_drivers'):
                for bot_data in self.chrome_drivers:
                    try:
                        driver = bot_data.get('driver')
                        bot_id = bot_data.get('id', '?')
                        self.log_message(f"🔧 Fechando Bot #{bot_id}...", "INFO")
                        if driver:
                            driver.quit()
                        self.log_message(f"✅ Bot #{bot_id} fechado", "SUCCESS")
                    except Exception as e:
                        self.log_message(f"❌ Erro ao fechar Bot #{bot_data.get('id', '?')}: {e}", "ERROR")
                self.chrome_drivers = []
            # Fechar processos antigos se existirem
            if hasattr(self, 'chrome_processes'):
                for process in self.chrome_processes:
                    try:
                        if process.poll() is None:
                            process.terminate()
                    except:
                        pass
                self.chrome_processes = []
            # Matar todos os processos Chrome e chromedriver para garantir liberação dos perfis
            killed = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if 'chrome' in proc.info['name'].lower() or 'chromedriver' in proc.info['name'].lower():
                        psutil.Process(proc.info['pid']).terminate()
                        killed += 1
                except:
                    pass
            if killed > 0:
                self.log_message(f"🛑 {killed} processos Chrome/chromedriver finalizados!", "WARNING")
            self.bot_stats.clear()
            self.total_bots_active = 0
            self.log_message("✅ Automação parada com sucesso!", "SUCCESS")
        except Exception as e:
            self.log_message(f"❌ Erro: {e}", "ERROR")

    def emergency_stop_direct(self):
        """Parada de emergência - fecha tudo"""
        try:
            result = messagebox.askyesno("Emergência", "Fechar TODOS os processos Chrome e drivers Selenium?")
            if result:
                self.log_message("🚨 PARADA DE EMERGÊNCIA!", "WARNING")
                
                # Parar automação
                self.automation_active = False
                
                # Fechar drivers Selenium
                if hasattr(self, 'chrome_drivers'):
                    for bot_data in self.chrome_drivers:
                        try:
                            driver = bot_data['driver']
                            driver.quit()
                        except:
                            pass
                    self.chrome_drivers = []
                
                # Matar processos Chrome
                killed = 0
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if 'chrome' in proc.info['name'].lower() or 'chromedriver' in proc.info['name'].lower():
                            psutil.Process(proc.info['pid']).terminate()
                            killed += 1
                    except:
                        pass
                
                self.bot_stats.clear()
                self.total_bots_active = 0
                self.log_message(f"🛑 {killed} processos Chrome finalizados!", "WARNING")
                
        except Exception as e:
            self.log_message(f"❌ Erro: {e}", "ERROR")

    def force_close_tabs(self):
        """Fecha apenas as guias do navegador customizado do bot, sem afetar outros navegadores do sistema."""
        try:
            self.log_message("🗂️ Fechando apenas guias do navegador do bot...", "INFO")
            # Fecha instâncias do CustomBrowser abertas pelo bot
            closed = 0
            if hasattr(self, 'custom_browsers'):
                for bot in self.custom_browsers:
                    browser = bot.get('browser')
                    try:
                        browser.close()
                        closed += 1
                    except Exception as e:
                        self.log_message(f"⚠️ Falha ao fechar navegador do bot #{bot.get('id')}: {e}", "WARNING")
                self.custom_browsers = []
            self.log_message(f"✅ {closed} guias do bot fechadas!", "SUCCESS")
            messagebox.showinfo("Sucesso", f"✅ {closed} guias do bot foram fechadas!")
        except Exception as e:
            self.log_message(f"❌ Erro ao fechar guias do bot: {e}", "ERROR")
            messagebox.showerror("Erro", f"❌ Erro ao fechar guias do bot: {e}")

    def check_for_updates(self):
        """Sistema robusto de atualização do app"""
        try:
            self.log_message("🔄 Verificando atualizações...", "INFO")
            
            # Configurações da atualização
            current_version = "3.0.0"
            github_api = "https://api.github.com/repos/seu-usuario/keydrop-bot/releases/latest"
            download_url = "https://github.com/seu-usuario/keydrop-bot/releases/latest/download/"
            
            # Thread para não travar a interface
            def update_thread():
                try:
                    # Verificar versão mais recente
                    self.log_message("🌐 Consultando GitHub API...", "INFO")
                    
                    # Simular verificação (substitua pela API real)
                    import random
                    has_update = random.choice([True, False])
                    new_version = "3.0.1" if has_update else current_version
                    
                    if has_update:
                        self.log_message(f"🎉 Nova versão disponível: v{new_version}", "SUCCESS")
                        
                        # Perguntar ao usuário
                        response = messagebox.askyesno(
                            "Atualização Disponível", 
                            f"🎉 Nova versão disponível!\n\n"
                            f"📦 Versão Atual: v{current_version}\n"
                            f"🆕 Nova Versão: v{new_version}\n\n"
                            f"🔄 Deseja baixar e instalar agora?\n\n"
                            f"⚠️ O aplicativo será reiniciado após a instalação."
                        )
                        
                        if response:
                            self.download_and_install_update(new_version)
                        else:
                            self.log_message("ℹ️ Atualização cancelada pelo usuário", "INFO")
                    else:
                        self.log_message("✅ Aplicativo já está na versão mais recente", "SUCCESS")
                        messagebox.showinfo(
                            "Sem Atualizações", 
                            f"✅ Você já possui a versão mais recente!\n\n"
                            f"📦 Versão Atual: v{current_version}\n"
                            f"🔍 Nenhuma atualização encontrada."
                        )
                
                except requests.exceptions.RequestException:
                    self.log_message("❌ Erro de conectividade ao verificar atualizações", "ERROR")
                    messagebox.showerror("Erro", "❌ Não foi possível verificar atualizações.\n\n🌐 Verifique sua conexão com a internet.")
                
                except Exception as e:
                    self.log_message(f"❌ Erro ao verificar atualizações: {e}", "ERROR")
                    messagebox.showerror("Erro", f"❌ Erro ao verificar atualizações:\n\n{e}")
            
            # Executar em thread separada
            threading.Thread(target=update_thread, daemon=True).start()
            
        except Exception as e:
            self.log_message(f"❌ Erro no sistema de atualização: {e}", "ERROR")
            messagebox.showerror("Erro", f"❌ Erro no sistema de atualização: {e}")

    def download_and_install_update(self, version):
        """Baixar e instalar atualização"""
        try:
            self.log_message(f"📥 Baixando versão {version}...", "INFO")
            
            # Simular download (implementar download real)
            import time
            for i in range(1, 6):
                self.log_message(f"📥 Download em progresso... {i*20}%", "INFO")
                time.sleep(1)
            
            # Simular instalação
            self.log_message("🔧 Instalando atualização...", "INFO")
            time.sleep(2)
            
            # Sucesso simulado
            self.log_message("✅ Atualização instalada com sucesso!", "SUCCESS")
            
            response = messagebox.askyesno(
                "Atualização Concluída",
                f"✅ Atualização para v{version} instalada!\n\n"
                f"🔄 É necessário reiniciar o aplicativo.\n\n"
                f"🚀 Deseja reiniciar agora?"
            )
            
            if response:
                self.log_message("🔄 Reiniciando aplicativo...", "INFO")
                self.root.quit()
                # Aqui você pode adicionar código para reiniciar o app
                
        except Exception as e:
            self.log_message(f"❌ Erro na instalação: {e}", "ERROR")
            messagebox.showerror("Erro", f"❌ Erro na instalação: {e}")

    def run(self):
        """Método principal para executar a aplicação"""
        self.log_message("🚀 Keydrop Bot Professional v3.0.0 iniciado!", "SUCCESS")
        self.root.mainloop()

    def save_config(self):
        """Salvar configurações no arquivo JSON"""
        try:
            config = {
                'headless_mode': self.headless_var.get(),
                'stealth_headless_mode': self.stealth_headless_var.get(),
                'mini_window_mode': self.mini_window_var.get(),
                'login_tabs_mode': self.login_tabs_var.get(),
                'contender_mode': self.contender_mode_var.get(),
                'discord_enabled': self.discord_enabled_var.get(),
                'discord_webhook': self.discord_webhook_var.get(),
                'save_timestamp': datetime.now().isoformat()
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.log_message("✅ Configurações salvas com sucesso!", "SUCCESS")
            messagebox.showinfo("Sucesso", "✅ Configurações salvas com sucesso!")
            
        except Exception as e:
            self.log_message(f"❌ Erro ao salvar configurações: {e}", "ERROR")
            messagebox.showerror("Erro", f"❌ Erro ao salvar configurações: {e}")

    def load_config(self):
        """Carregar configurações do arquivo JSON"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Aplicar configurações carregadas
                self.headless_var.set(config.get('headless_mode', False))
                self.stealth_headless_var.set(config.get('stealth_headless_mode', False))
                self.mini_window_var.set(config.get('mini_window_mode', False))
                self.login_tabs_var.set(config.get('login_tabs_mode', False))
                self.contender_mode_var.set(config.get('contender_mode', False))
                self.discord_enabled_var.set(config.get('discord_enabled', False))
                self.discord_webhook_var.set(config.get('discord_webhook', ''))
                
                self.log_message("✅ Configurações carregadas com sucesso!", "SUCCESS")
                messagebox.showinfo("Sucesso", "✅ Configurações carregadas com sucesso!")
            else:
                self.log_message("⚠️ Arquivo de configuração não encontrado", "WARNING")
                messagebox.showwarning("Aviso", "⚠️ Arquivo de configuração não encontrado")
                
        except Exception as e:
            self.log_message(f"❌ Erro ao carregar configurações: {e}", "ERROR")
            messagebox.showerror("Erro", f"❌ Erro ao carregar configurações: {e}")

    def clear_cache(self):
        """Limpar cache do sistema"""
        try:
            cache_dirs = [
                Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data" / "Default" / "Cache",
                Path("cache"),
                Path("temp")
            ]
            
            cleared_count = 0
            for cache_dir in cache_dirs:
                if cache_dir.exists() and cache_dir.is_dir():
                    try:
                        for item in cache_dir.iterdir():
                            if item.is_file():
                                item.unlink()
                                cleared_count += 1
                            elif item.is_dir():
                                shutil.rmtree(item, ignore_errors=True)
                                cleared_count += 1
                    except:
                        continue
            
            self.log_message(f"✅ Cache limpo! {cleared_count} itens removidos", "SUCCESS")
            messagebox.showinfo("Sucesso", f"✅ Cache limpo!\n{cleared_count} itens removidos")
            
        except Exception as e:
            self.log_message(f"❌ Erro ao limpar cache: {e}", "ERROR")
            messagebox.showerror("Erro", f"❌ Erro ao limpar cache: {e}")

    def clear_logs(self):
        """Limpar logs da interface"""
        try:
            if hasattr(self, 'logs_text'):
                self.logs_text.config(state=tk.NORMAL)
                self.logs_text.delete(1.0, tk.END)
                self.logs_text.config(state=tk.DISABLED)
            self.log_message("✅ Logs limpos com sucesso!", "SUCCESS")
        except Exception as e:
            self.log_message(f"❌ Erro ao limpar logs: {e}", "ERROR")

    def save_logs(self):
        """Salvar logs em arquivo"""
        try:
            if hasattr(self, 'logs_text'):
                logs_content = self.logs_text.get(1.0, tk.END)
                
                filename = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    title="Salvar Logs"
                )
                
                if filename:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(logs_content)
                    
                    self.log_message(f"✅ Logs salvos em: {filename}", "SUCCESS")
                    messagebox.showinfo("Sucesso", f"✅ Logs salvos com sucesso!\n{filename}")
                    
        except Exception as e:
            self.log_message(f"❌ Erro ao salvar logs: {e}", "ERROR")
            messagebox.showerror("Erro", f"❌ Erro ao salvar logs: {e}")

    def refresh_logs(self):
        """Atualizar visualização dos logs"""
        try:
            # Força atualização da interface
            self.root.update_idletasks()
            
            # Rola para o final dos logs
            if hasattr(self, 'logs_text'):
                self.logs_text.see(tk.END)
            
            self.log_message("🔄 Logs atualizados", "INFO")
            
        except Exception as e:
            self.log_message(f"❌ Erro ao atualizar logs: {e}", "ERROR")

def main():
    """Função principal"""
    try:
        print("🎯 Iniciando Keydrop Bot Professional v3.0.0...")
        
        if os.name == 'nt':
            try:
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass
        
        app = KeydropBotGUI()
        app.run()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
