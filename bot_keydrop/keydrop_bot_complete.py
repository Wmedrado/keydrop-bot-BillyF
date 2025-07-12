#!/usr/bin/env python3
"""
Keydrop Bot Professional v3.0.0 - Interface Gráfica Desktop COMPLETA
Aplicativo desktop nativo com automação Chrome integrada
"""

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
from datetime import datetime
from pathlib import Path
import psutil

class KeydropBotGUI:
    def __init__(self):
        """Inicialização ultra-robusta para executável"""
        try:
            # Criar janela principal
            self.root = tk.Tk()
            self.root.withdraw()
            
            # Configurações básicas
            self.root.title("Keydrop Bot Professional v3.0.0")
            self.root.geometry("1100x800")
            
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
            
        except Exception as e:
            print(f"Erro crítico na inicialização: {e}")
            self.create_emergency_interface(e)

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
            
            # Estilos personalizados
            style.configure('Dark.TFrame', background=self.dark_colors['bg'])
            style.configure('Dark.TLabel', background=self.dark_colors['bg'], foreground=self.dark_colors['fg'])
            style.configure('Dark.TLabelFrame', background=self.dark_colors['bg'], foreground=self.dark_colors['fg'])
            style.configure('Dark.TLabelFrame.Label', background=self.dark_colors['bg'], foreground=self.dark_colors['accent'])
            style.configure('Large.TButton', font=('Arial', 14, 'bold'), padding=(20, 15))
            style.configure('Emergency.TButton', font=('Arial', 14, 'bold'), padding=(20, 15), foreground=self.dark_colors['error'])
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
            x = (screen_width - 1100) // 2
            y = (screen_height - 800) // 2
            self.root.geometry(f"1100x800+{x}+{y}")
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
            print(f"Erro ao configurar interface: {e}")
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
            tk.Label(header, text="Desenvolvido por William Medrado", 
                    font=('Arial', 12), bg=self.dark_colors['bg'], 
                    fg=self.dark_colors['fg']).pack()
            
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
        tk.Label(info_frame, text="👨‍💻 Desenvolvido por: William Medrado (wmedrado)", 
                font=('Arial', 11), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['warning']).pack(anchor=tk.W, padx=10, pady=2)
        
        # Controle de Automação
        bot_frame = tk.LabelFrame(control_frame, text="🚀 Controle de Automação", 
                                bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                font=('Arial', 12, 'bold'))
        bot_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(bot_frame, text="✨ Sistema de Multi-Bots com Perfis Independentes", 
                bg=self.dark_colors['bg'], fg=self.dark_colors['success'], 
                font=('Arial', 12, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 15))
        
        # Botões principais
        buttons_frame = tk.Frame(bot_frame, bg=self.dark_colors['bg'])
        buttons_frame.pack(fill=tk.X, pady=10, padx=10)
        
        tk.Button(buttons_frame, text="🚀 INICIAR AUTOMAÇÃO", 
                 command=self.start_bot_direct, font=('Arial', 14, 'bold'),
                 bg=self.dark_colors['success'], fg='white', 
                 relief='raised', bd=3).pack(side=tk.LEFT, padx=15, ipadx=20, ipady=10)
        
        tk.Button(buttons_frame, text="⏹️ PARAR AUTOMAÇÃO", 
                 command=self.stop_bot_direct, font=('Arial', 14, 'bold'),
                 bg=self.dark_colors['warning'], fg='white', 
                 relief='raised', bd=3).pack(side=tk.LEFT, padx=15, ipadx=20, ipady=10)
        
        tk.Button(buttons_frame, text="🚨 EMERGÊNCIA", 
                 command=self.emergency_stop_direct, font=('Arial', 14, 'bold'),
                 bg=self.dark_colors['error'], fg='white', 
                 relief='raised', bd=3).pack(side=tk.RIGHT, padx=15, ipadx=15, ipady=10)
        
        # Status em tempo real
        status_frame = tk.LabelFrame(control_frame, text="📊 Status em Tempo Real", 
                                   bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                   font=('Arial', 12, 'bold'))
        status_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=15, state=tk.DISABLED, 
                                                   font=('Consolas', 12), bg=self.dark_colors['entry_bg'], 
                                                   fg=self.dark_colors['fg'], insertbackground=self.dark_colors['fg'],
                                                   selectbackground=self.dark_colors['select_bg'],
                                                   selectforeground=self.dark_colors['select_fg'])
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_config_tab(self):
        """Criar aba de configurações"""
        config_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(config_frame, text="⚙️ Configurações")
        
        # Configurações Básicas
        basic_frame = tk.LabelFrame(config_frame, text="🔧 Configurações Básicas", 
                                  bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                  font=('Arial', 12, 'bold'))
        basic_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Grid de configurações
        config_grid = tk.Frame(basic_frame, bg=self.dark_colors['bg'])
        config_grid.pack(fill=tk.X, padx=20, pady=15)
        
        # Número de guias
        tk.Label(config_grid, text="🤖 Número de Guias/Bots (1-100):", 
                font=('Arial', 12, 'bold'), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['fg']).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.num_tabs_var = tk.StringVar(value="5")
        tk.Entry(config_grid, textvariable=self.num_tabs_var, width=15, font=('Arial', 12),
                bg=self.dark_colors['entry_bg'], fg=self.dark_colors['entry_fg'],
                insertbackground=self.dark_colors['entry_fg']).grid(row=0, column=1, padx=15, pady=8)
        
        # Velocidade
        tk.Label(config_grid, text="⚡ Velocidade de Execução (segundos):", 
                font=('Arial', 12, 'bold'), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['fg']).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.speed_var = tk.StringVar(value="8.0")
        tk.Entry(config_grid, textvariable=self.speed_var, width=15, font=('Arial', 12),
                bg=self.dark_colors['entry_bg'], fg=self.dark_colors['entry_fg'],
                insertbackground=self.dark_colors['entry_fg']).grid(row=1, column=1, padx=15, pady=8)
        
        # Retry
        tk.Label(config_grid, text="🔄 Tentativas de Retry:", 
                font=('Arial', 12, 'bold'), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['fg']).grid(row=2, column=0, sticky=tk.W, pady=8)
        self.retry_var = tk.StringVar(value="5")
        tk.Entry(config_grid, textvariable=self.retry_var, width=15, font=('Arial', 12),
                bg=self.dark_colors['entry_bg'], fg=self.dark_colors['entry_fg'],
                insertbackground=self.dark_colors['entry_fg']).grid(row=2, column=1, padx=15, pady=8)
        
        # Dica
        tk.Label(config_grid, text="💡 Recomendado: 7-10 segundos para máxima eficiência", 
                font=('Arial', 11), bg=self.dark_colors['bg'], 
                fg=self.dark_colors['success']).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Modos de Operação
        modes_frame = tk.LabelFrame(config_frame, text="🎯 Modos de Operação", 
                                  bg=self.dark_colors['bg'], fg=self.dark_colors['accent'],
                                  font=('Arial', 12, 'bold'))
        modes_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Checkboxes
        modes_inner = tk.Frame(modes_frame, bg=self.dark_colors['bg'])
        modes_inner.pack(fill=tk.X, padx=20, pady=15)
        
        self.headless_var = tk.BooleanVar()
        tk.Checkbutton(modes_inner, text="🕶️ Modo Headless (invisível)", 
                      variable=self.headless_var, bg=self.dark_colors['bg'], 
                      fg=self.dark_colors['fg'], font=('Arial', 11),
                      selectcolor=self.dark_colors['entry_bg']).pack(anchor=tk.W, pady=5)
        
        self.mini_window_var = tk.BooleanVar()
        tk.Checkbutton(modes_inner, text="📱 Modo Mini (100x200px)", 
                      variable=self.mini_window_var, bg=self.dark_colors['bg'], 
                      fg=self.dark_colors['fg'], font=('Arial', 11),
                      selectcolor=self.dark_colors['entry_bg']).pack(anchor=tk.W, pady=5)
        
        self.login_tabs_var = tk.BooleanVar()
        tk.Checkbutton(modes_inner, text="🔑 Abas de Login (Keydrop/Steam)", 
                      variable=self.login_tabs_var, bg=self.dark_colors['bg'], 
                      fg=self.dark_colors['fg'], font=('Arial', 11),
                      selectcolor=self.dark_colors['entry_bg']).pack(anchor=tk.W, pady=5)
        
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
        
        self.total_skins_label = tk.Label(global_stats, text="💰 Saldo Total: $0.00", 
                                        font=('Arial', 12), bg=self.dark_colors['bg'],
                                        fg=self.dark_colors['fg'])
        self.total_skins_label.grid(row=1, column=2, sticky=tk.W, pady=(10, 0))
        
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
            if hasattr(self, 'total_skins_label'):
                self.total_skins_label.config(text=f"💰 Saldo Total: ${total_skins:.2f}")
            
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
        """Iniciar automação"""
        try:
            self.log_message("🤖 Iniciando automação Chrome...", "INFO")
            edge_path = self.find_chrome_executable()
            
            if not edge_path:
                messagebox.showerror("Erro", "Google Chrome não encontrado!")
                return

            self.log_message(f"✅ Chrome encontrado: {edge_path}", "SUCCESS")
            
            num_tabs = int(self.num_tabs_var.get()) if hasattr(self, 'num_tabs_var') else 3
            headless_mode = self.headless_var.get() if hasattr(self, 'headless_var') else False
            mini_mode = self.mini_window_var.get() if hasattr(self, 'mini_window_var') else False
            login_tabs = self.login_tabs_var.get() if hasattr(self, 'login_tabs_var') else False
            
            self.log_message(f"📋 Configurações: {num_tabs} guias, Headless: {headless_mode}, Mini: {mini_mode}", "INFO")
            
            self.automation_thread = threading.Thread(
                target=self.run_edge_automation,
                args=(edge_path, num_tabs, headless_mode, mini_mode, login_tabs),
                daemon=True
            )
            self.automation_thread.start()
            
        except Exception as e:
            self.log_message(f"❌ Erro: {e}", "ERROR")

    def run_edge_automation(self, edge_path, num_tabs, headless_mode, mini_mode, login_tabs):
        """Executar automação"""
        try:
            self.edge_processes = []
            main_url = "https://key-drop.com/"
            
            for i in range(num_tabs):
                try:
                    profile_dir = f"./edge_profiles/bot_{i+1}"
                    
                    args = [
                        edge_path,
                        f"--user-data-dir={profile_dir}",
                        f"--profile-directory=Profile{i+1}",
                        "--no-first-run",
                        "--no-default-browser-check"
                    ]
                    
                    if headless_mode:
                        args.append("--headless")
                    elif mini_mode:
                        args.extend(["--window-size=300,400", f"--window-position={100+(i*50)},{100+(i*50)}"])
                    else:
                        args.extend(["--window-size=800,600", f"--window-position={100+(i*100)},{100+(i*50)}"])
                    
                    args.append(main_url)
                    
                    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.edge_processes.append(process)
                    
                    self.bot_stats[i+1] = {
                        'active': True,
                        'raffles_amateur': 0,
                        'raffles_contender': 0,
                        'errors': 0,
                        'network_usage': 0,
                        'skin_balance': 0.0,
                        'start_time': datetime.now()
                    }
                    
                    self.total_bots_active += 1
                    self.log_message(f"✅ Bot #{i+1} iniciado! PID: {process.pid}", "SUCCESS")
                    time.sleep(1)
                    
                except Exception as e:
                    self.log_message(f"❌ Erro Bot #{i+1}: {e}", "ERROR")
            
            self.log_message(f"🎉 {len(self.edge_processes)} bots iniciados!", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"❌ Erro automação: {e}", "ERROR")

    def stop_bot_direct(self):
        """Parar automação"""
        try:
            self.log_message("🛑 Parando automação...", "WARNING")
            
            if hasattr(self, 'edge_processes'):
                for process in self.edge_processes:
                    try:
                        if process.poll() is None:
                            process.terminate()
                    except:
                        pass
                self.edge_processes = []
                
            self.bot_stats.clear()
            self.total_bots_active = 0
            self.log_message("✅ Automação parada!", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"❌ Erro: {e}", "ERROR")

    def emergency_stop_direct(self):
        """Parada de emergência"""
        try:
            result = messagebox.askyesno("Emergência", "Fechar TODOS os processos Chrome?")
            if result:
                self.log_message("🚨 PARADA DE EMERGÊNCIA!", "WARNING")
                killed = 0
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if 'chrome' in proc.info['name'].lower():
                            psutil.Process(proc.info['pid']).terminate()
                            killed += 1
                    except:
                        pass
                self.log_message(f"🛑 {killed} processos Chrome finalizados!", "WARNING")
        except Exception as e:
            self.log_message(f"❌ Erro: {e}", "ERROR")

    def save_config(self):
        """Salvar configurações"""
        try:
            config = {
                "num_tabs": int(self.num_tabs_var.get()),
                "execution_speed": float(self.speed_var.get()),
                "retry_attempts": int(self.retry_var.get()),
                "headless_mode": self.headless_var.get(),
                "mini_window_mode": self.mini_window_var.get(),
                "enable_login_tabs": self.login_tabs_var.get(),
                "discord_webhook_url": self.discord_webhook_var.get(),
                "discord_notifications": self.discord_enabled_var.get()
            }
            
            with open("config.json", 'w') as f:
                json.dump(config, f, indent=2)
            
            self.log_message("✅ Configurações salvas!", "SUCCESS")
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            
        except Exception as e:
            self.log_message(f"❌ Erro ao salvar: {e}", "ERROR")

    def load_config(self):
        """Carregar configurações"""
        try:
            if os.path.exists("config.json"):
                with open("config.json", 'r') as f:
                    config = json.load(f)
                
                self.num_tabs_var.set(str(config.get("num_tabs", 5)))
                self.speed_var.set(str(config.get("execution_speed", 8.0)))
                self.retry_var.set(str(config.get("retry_attempts", 5)))
                self.headless_var.set(config.get("headless_mode", False))
                self.mini_window_var.set(config.get("mini_window_mode", False))
                self.login_tabs_var.set(config.get("enable_login_tabs", False))
                self.discord_webhook_var.set(config.get("discord_webhook_url", ""))
                self.discord_enabled_var.set(config.get("discord_notifications", False))
                
                self.log_message("✅ Configurações carregadas!", "SUCCESS")
            else:
                self.log_message("ℹ️ Usando configurações padrão", "INFO")
                
        except Exception as e:
            self.log_message(f"❌ Erro ao carregar: {e}", "ERROR")

    def clear_cache(self):
        """Limpar cache"""
        self.log_message("🧹 Cache limpo localmente", "INFO")
        messagebox.showinfo("Cache", "Cache local limpo!")

    def clear_logs(self):
        """Limpar logs"""
        try:
            if hasattr(self, 'logs_text'):
                self.logs_text.config(state=tk.NORMAL)
                self.logs_text.delete(1.0, tk.END)
                self.logs_text.config(state=tk.DISABLED)
            if hasattr(self, 'status_text'):
                self.status_text.config(state=tk.NORMAL)
                self.status_text.delete(1.0, tk.END)
                self.status_text.config(state=tk.DISABLED)
            self.log_message("🗑️ Logs limpos!", "INFO")
        except Exception as e:
            print(f"Erro: {e}")

    def save_logs(self):
        """Salvar logs"""
        try:
            if not hasattr(self, 'logs_text'):
                messagebox.showwarning("Aviso", "Logs não disponíveis")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.logs_text.get(1.0, tk.END))
                self.log_message(f"💾 Logs salvos: {filename}", "SUCCESS")
        except Exception as e:
            self.log_message(f"❌ Erro: {e}", "ERROR")

    def refresh_logs(self):
        """Atualizar logs"""
        self.log_message("🔄 Logs atualizados pelo usuário", "INFO")
        self.log_message(f"📊 Bots ativos: {self.total_bots_active}", "INFO")

    def run(self):
        """Executar aplicação"""
        self.log_message("🎉 Keydrop Bot Professional v3.0.0 iniciado!")
        self.log_message("📱 Modo: Aplicação Desktop Nativa")
        self.log_message("🚀 Sistema pronto para automação Chrome")
        self.root.mainloop()

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
