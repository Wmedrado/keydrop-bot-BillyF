#!/usr/bin/env python3
"""
Interface moderna melhorada v2.0.8 - KeyDrop Bot Professional Edition
Seções bem divididas, mais leve e com melhor organização
"""

try:
    import customtkinter as ctk
    import tkinter as tk
    from tkinter import messagebox, filedialog, ttk
    import threading
    import time
    import json
    import os
    from datetime import datetime
    import subprocess
    import sys
    
    # Tentar importar psutil
    try:
        import psutil
        PSUTIL_AVAILABLE = True
    except ImportError:
        PSUTIL_AVAILABLE = False
        print("⚠️ psutil não disponível - monitoramento limitado")
    
    # Importar sistema de gerenciamento de memória
    try:
        from src.memory_manager import MemoryManager
        MEMORY_MANAGER_AVAILABLE = True
    except ImportError:
        MemoryManager = None
        MEMORY_MANAGER_AVAILABLE = False
        print("⚠️ Sistema de gerenciamento de memória não disponível")
    
    # Imports locais do bot
    from keydrop_bot import KeyDropBot, BotManager
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)

class ModernKeyDropInterface:
    """Interface moderna melhorada com seções bem organizadas"""
    
    def __init__(self):
        # Configurações da interface
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Janela principal
        self.root = ctk.CTk()
        self.root.title("KeyDrop Bot Professional Edition v2.1.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Configurar ícone se disponível
        try:
            self.root.iconbitmap("bot-icone.ico")
        except:
            pass
        
        # Inicializar sistema de gerenciamento de memória
        self.memory_manager = MemoryManager() if MEMORY_MANAGER_AVAILABLE else None
        if self.memory_manager:
            self.memory_manager.start()
        
        # Gerenciador de bots
        self.bot_manager = BotManager()
        
        # Controles da interface
        self.bot_frames = {}
        self.config = self.carregar_config()
        self.running = False
        
        # Sistema de relatórios
        self.report_manager = None
        self.telegram_bot = None
        
        # Criar interface
        self.criar_interface()
        
        # Iniciar monitoramento
        self.iniciar_monitoramento()
        
        # Iniciar sistemas auxiliares
        self.iniciar_sistemas_auxiliares()
        
    def criar_interface(self):
        """Cria a interface com seções bem organizadas"""
        
        # Frame principal com scroll
        self.main_frame = ctk.CTkScrollableFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Seção 1: Cabeçalho e Informações
        self.criar_secao_header()
        
        # Seção 2: Configuração Global
        self.criar_secao_configuracao()
        
        # Seção 3: Controles Gerais
        self.criar_secao_controles()
        
        # Seção 4: Bots Individuais
        self.criar_secao_bots()
        
        # Seção 5: Monitoramento do Sistema
        self.criar_secao_monitoramento()
        
        # Seção 6: Logs e Status
        self.criar_secao_logs()
        
    def criar_secao_header(self):
        """Cria seção do cabeçalho"""
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🤖 KeyDrop Bot Professional Edition", 
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=10)
        
        # Informações da versão
        version_frame = ctk.CTkFrame(header_frame)
        version_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Versão
        version_info = self.obter_versao()
        version_label = ctk.CTkLabel(
            version_frame,
            text=f"📦 Versão: {version_info['version']} | 🔧 Build: {version_info['build']}",
            font=("Arial", 12)
        )
        version_label.pack(side="left", padx=10, pady=5)
        
        # Status do sistema
        self.system_status_label = ctk.CTkLabel(
            version_frame,
            text="🟢 Sistema Operacional",
            font=("Arial", 12)
        )
        self.system_status_label.pack(side="right", padx=10, pady=5)
        
    def criar_secao_configuracao(self):
        """Cria seção de configuração global"""
        config_frame = ctk.CTkFrame(self.main_frame)
        config_frame.pack(fill="x", pady=(0, 10))
        
        # Título da seção
        config_title = ctk.CTkLabel(
            config_frame, 
            text="⚙️ Configuração Global", 
            font=("Arial", 16, "bold")
        )
        config_title.pack(pady=(10, 5))
        
        # Frame para opções
        options_frame = ctk.CTkFrame(config_frame)
        options_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Linha 1: Opções básicas
        row1_frame = ctk.CTkFrame(options_frame)
        row1_frame.pack(fill="x", pady=5)
        
        # Modo headless
        self.headless_var = tk.BooleanVar(value=self.config.get('headless', False))
        headless_check = ctk.CTkCheckBox(
            row1_frame,
            text="🚫 Modo Headless (sem interface gráfica)",
            variable=self.headless_var
        )
        headless_check.pack(side="left", padx=10, pady=5)
        
        # Mini Window
        self.mini_window_var = tk.BooleanVar(value=self.config.get('mini_window', False))
        mini_window_check = ctk.CTkCheckBox(
            row1_frame,
            text="🔽 Mini Window (200x300)",
            variable=self.mini_window_var
        )
        mini_window_check.pack(side="left", padx=10, pady=5)
        
        # Linha 2: Configurações avançadas
        row2_frame = ctk.CTkFrame(options_frame)
        row2_frame.pack(fill="x", pady=5)
        
        # Modo login
        self.login_mode_var = tk.BooleanVar(value=self.config.get('login_mode', False))
        login_check = ctk.CTkCheckBox(
            row2_frame,
            text="🔐 Modo Login (aguardar login manual)",
            variable=self.login_mode_var
        )
        login_check.pack(side="left", padx=10, pady=5)
        
        # Modo contender
        self.contender_mode_var = tk.BooleanVar(value=self.config.get('contender_mode', False))
        contender_check = ctk.CTkCheckBox(
            row2_frame,
            text="🏆 Modo Contender (sorteios 1h)",
            variable=self.contender_mode_var
        )
        contender_check.pack(side="left", padx=10, pady=5)
        
        # Linha 3: Configurações de perfil e retry
        row3_frame = ctk.CTkFrame(options_frame)
        row3_frame.pack(fill="x", pady=5)
        
        # Caminho do perfil
        profile_label = ctk.CTkLabel(row3_frame, text="📁 Caminho do Perfil:")
        profile_label.pack(side="left", padx=10, pady=5)
        
        self.profile_entry = ctk.CTkEntry(
            row3_frame,
            width=300,
            placeholder_text="Caminho para o perfil Chrome..."
        )
        self.profile_entry.pack(side="left", padx=5, pady=5)
        self.profile_entry.insert(0, self.config.get('profile_path', ''))
        
        profile_button = ctk.CTkButton(
            row3_frame,
            text="📂 Selecionar",
            width=100,
            command=self.selecionar_perfil
        )
        profile_button.pack(side="left", padx=5, pady=5)
        
        # Linha 4: Configurações de retry
        row4_frame = ctk.CTkFrame(options_frame)
        row4_frame.pack(fill="x", pady=5)
        
        # Número máximo de tentativas
        tentativas_label = ctk.CTkLabel(row4_frame, text="🔄 Máximo de Tentativas:")
        tentativas_label.pack(side="left", padx=10, pady=5)
        
        self.max_tentativas_var = tk.StringVar(value=str(self.config.get('max_tentativas', 3)))
        self.max_tentativas_entry = ctk.CTkEntry(
            row4_frame,
            width=80,
            textvariable=self.max_tentativas_var,
            placeholder_text="3"
        )
        self.max_tentativas_entry.pack(side="left", padx=5, pady=5)
        
        # Tooltip para explicar o campo
        tentativas_tooltip = ctk.CTkLabel(
            row4_frame,
            text="💡 Número de tentativas para join antes de reiniciar a guia",
            font=("Arial", 10),
            text_color="gray"
        )
        tentativas_tooltip.pack(side="left", padx=10, pady=5)
        
        # Linha 5: Configurações de relatório Discord
        row5_frame = ctk.CTkFrame(options_frame)
        row5_frame.pack(fill="x", pady=5)
        
        # Tempo do relatório Discord
        discord_label = ctk.CTkLabel(row5_frame, text="📱 Intervalo Relatório Discord (horas):")
        discord_label.pack(side="left", padx=10, pady=5)
        
        self.discord_report_hours_var = tk.StringVar(value=str(self.config.get('discord_report_hours', 12)))
        self.discord_report_hours_entry = ctk.CTkEntry(
            row5_frame,
            width=80,
            textvariable=self.discord_report_hours_var,
            placeholder_text="12"
        )
        self.discord_report_hours_entry.pack(side="left", padx=5, pady=5)
        
        # Tooltip para explicar o campo
        discord_tooltip = ctk.CTkLabel(
            row5_frame,
            text="💡 Intervalo em horas para envio automático de relatórios (ex: 12h, 24h)",
            font=("Arial", 10),
            text_color="gray"
        )
        discord_tooltip.pack(side="left", padx=10, pady=5)
        
        # Linha 6: Configurações do Telegram
        row6_frame = ctk.CTkFrame(options_frame)
        row6_frame.pack(fill="x", pady=5)
        
        # Token do Telegram
        telegram_label = ctk.CTkLabel(row6_frame, text="📱 Token Telegram Bot:")
        telegram_label.pack(side="left", padx=10, pady=5)
        
        self.telegram_token_var = tk.StringVar(value=self.config.get('telegram_token', ''))
        self.telegram_token_entry = ctk.CTkEntry(
            row6_frame,
            width=300,
            textvariable=self.telegram_token_var,
            placeholder_text="Digite o token do Telegram Bot...",
            show="*"
        )
        self.telegram_token_entry.pack(side="left", padx=5, pady=5)
        
        # Botão para testar Telegram
        telegram_test_button = ctk.CTkButton(
            row6_frame,
            text="🧪 Testar",
            width=80,
            command=self.testar_telegram
        )
        telegram_test_button.pack(side="left", padx=5, pady=5)
        
    def criar_secao_controles(self):
        """Cria seção de controles gerais"""
        controls_frame = ctk.CTkFrame(self.main_frame)
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Título da seção
        controls_title = ctk.CTkLabel(
            controls_frame, 
            text="🎮 Controles Gerais", 
            font=("Arial", 16, "bold")
        )
        controls_title.pack(pady=(10, 5))
        
        # Frame para botões
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Linha 1: Controles principais
        main_controls_frame = ctk.CTkFrame(buttons_frame)
        main_controls_frame.pack(fill="x", pady=5)
        
        # Botão Iniciar/Parar
        self.start_stop_button = ctk.CTkButton(
            main_controls_frame,
            text="🚀 Iniciar Todos os Bots",
            width=200,
            height=40,
            command=self.toggle_bots,
            fg_color=("green", "darkgreen")
        )
        self.start_stop_button.pack(side="left", padx=10, pady=5)
        
        # Botão Reiniciar
        restart_button = ctk.CTkButton(
            main_controls_frame,
            text="🔄 Reiniciar Todos",
            width=150,
            height=40,
            command=self.reiniciar_todos,
            fg_color=("orange", "darkorange")
        )
        restart_button.pack(side="left", padx=10, pady=5)
        
        # Botão Emergência
        emergency_button = ctk.CTkButton(
            main_controls_frame,
            text="🚨 PARADA EMERGENCIAL",
            width=200,
            height=40,
            command=self.parada_emergencial,
            fg_color=("red", "darkred")
        )
        emergency_button.pack(side="left", padx=10, pady=5)
        
        # Linha 2: Controles secundários
        secondary_controls_frame = ctk.CTkFrame(buttons_frame)
        secondary_controls_frame.pack(fill="x", pady=5)
        
        # Botão Salvar Config
        save_button = ctk.CTkButton(
            secondary_controls_frame,
            text="💾 Salvar Configuração",
            width=150,
            command=self.salvar_config
        )
        save_button.pack(side="left", padx=10, pady=5)
        
        # Botão Verificar Atualizações
        update_button = ctk.CTkButton(
            secondary_controls_frame,
            text="🔄 Verificar Atualizações",
            width=150,
            command=self.verificar_atualizacoes
        )
        update_button.pack(side="left", padx=10, pady=5)
        
        # Botão Logs
        logs_button = ctk.CTkButton(
            secondary_controls_frame,
            text="📜 Abrir Logs",
            width=150,
            command=self.abrir_logs
        )
        logs_button.pack(side="left", padx=10, pady=5)
        
    def criar_secao_bots(self):
        """Cria seção dos bots individuais"""
        bots_frame = ctk.CTkFrame(self.main_frame)
        bots_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Título da seção
        bots_title = ctk.CTkLabel(
            bots_frame, 
            text="🤖 Bots Individuais", 
            font=("Arial", 16, "bold")
        )
        bots_title.pack(pady=(10, 5))
        
        # Frame scrollable para bots
        self.bots_scroll_frame = ctk.CTkScrollableFrame(bots_frame, height=300)
        self.bots_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Criar bots iniciais
        self.criar_bot_inicial()
        
        # Botão para adicionar bot
        add_bot_button = ctk.CTkButton(
            bots_frame,
            text="➕ Adicionar Bot",
            width=150,
            command=self.adicionar_bot
        )
        add_bot_button.pack(pady=(0, 10))
        
    def criar_secao_monitoramento(self):
        """Cria seção de monitoramento do sistema"""
        monitor_frame = ctk.CTkFrame(self.main_frame)
        monitor_frame.pack(fill="x", pady=(0, 10))
        
        # Título da seção
        monitor_title = ctk.CTkLabel(
            monitor_frame, 
            text="📊 Monitoramento do Sistema", 
            font=("Arial", 16, "bold")
        )
        monitor_title.pack(pady=(10, 5))
        
        # Frame para métricas
        metrics_frame = ctk.CTkFrame(monitor_frame)
        metrics_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Linha 1: Métricas de sistema
        system_metrics_frame = ctk.CTkFrame(metrics_frame)
        system_metrics_frame.pack(fill="x", pady=5)
        
        # CPU
        self.cpu_label = ctk.CTkLabel(
            system_metrics_frame,
            text="💻 CPU: 0%",
            font=("Arial", 12)
        )
        self.cpu_label.pack(side="left", padx=10, pady=5)
        
        # RAM
        self.ram_label = ctk.CTkLabel(
            system_metrics_frame,
            text="🧠 RAM: 0 MB",
            font=("Arial", 12)
        )
        self.ram_label.pack(side="left", padx=10, pady=5)
        
        # Processos Chrome
        self.chrome_label = ctk.CTkLabel(
            system_metrics_frame,
            text="🌐 Chrome: 0 processos",
            font=("Arial", 12)
        )
        self.chrome_label.pack(side="left", padx=10, pady=5)
        
        # Uptime
        self.uptime_label = ctk.CTkLabel(
            system_metrics_frame,
            text="⏱️ Uptime: 0s",
            font=("Arial", 12)
        )
        self.uptime_label.pack(side="left", padx=10, pady=5)
        
        # Linha 2: Métricas detalhadas
        detailed_metrics_frame = ctk.CTkFrame(metrics_frame)
        detailed_metrics_frame.pack(fill="x", pady=5)
        
        # Memória Virtual
        self.virtual_mem_label = ctk.CTkLabel(
            detailed_metrics_frame,
            text="💾 Mem. Virtual: 0 MB",
            font=("Arial", 12)
        )
        self.virtual_mem_label.pack(side="left", padx=10, pady=5)
        
        # Disco
        self.disk_label = ctk.CTkLabel(
            detailed_metrics_frame,
            text="💿 Disco: 0%",
            font=("Arial", 12)
        )
        self.disk_label.pack(side="left", padx=10, pady=5)
        
        # Rede
        self.network_label = ctk.CTkLabel(
            detailed_metrics_frame,
            text="🌐 Rede: 0 MB",
            font=("Arial", 12)
        )
        self.network_label.pack(side="left", padx=10, pady=5)
        
        # Limpezas
        self.cleanup_label = ctk.CTkLabel(
            detailed_metrics_frame,
            text="🧹 Limpezas: 0",
            font=("Arial", 12)
        )
        self.cleanup_label.pack(side="left", padx=10, pady=5)
        
    def criar_secao_logs(self):
        """Cria seção de logs e status"""
        logs_frame = ctk.CTkFrame(self.main_frame)
        logs_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Título da seção
        logs_title = ctk.CTkLabel(
            logs_frame, 
            text="📜 Logs e Status", 
            font=("Arial", 16, "bold")
        )
        logs_title.pack(pady=(10, 5))
        
        # Text widget para logs
        self.logs_text = ctk.CTkTextbox(
            logs_frame,
            height=150,
            font=("Consolas", 10)
        )
        self.logs_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Adicionar log inicial
        self.adicionar_log("🚀 Interface iniciada com sucesso!")
        
    def criar_bot_inicial(self):
        """Cria o primeiro bot"""
        self.adicionar_bot()
        
    def adicionar_bot(self):
        """Adiciona um novo bot à interface"""
        bot_id = len(self.bot_frames) + 1
        
        # Frame para o bot
        bot_frame = ctk.CTkFrame(self.bots_scroll_frame)
        bot_frame.pack(fill="x", pady=5)
        
        # Header do bot
        bot_header = ctk.CTkFrame(bot_frame)
        bot_header.pack(fill="x", padx=10, pady=5)
        
        # Nome do bot
        bot_name_label = ctk.CTkLabel(
            bot_header,
            text=f"🤖 Bot {bot_id}",
            font=("Arial", 14, "bold")
        )
        bot_name_label.pack(side="left", padx=10, pady=5)
        
        # Status do bot
        bot_status_label = ctk.CTkLabel(
            bot_header,
            text="⏹️ Parado",
            font=("Arial", 12)
        )
        bot_status_label.pack(side="left", padx=10, pady=5)
        
        # Controles do bot
        bot_controls_frame = ctk.CTkFrame(bot_header)
        bot_controls_frame.pack(side="right", padx=10, pady=5)
        
        # Botão Iniciar/Parar bot
        bot_toggle_button = ctk.CTkButton(
            bot_controls_frame,
            text="▶️ Iniciar",
            width=80,
            command=lambda: self.toggle_bot(bot_id)
        )
        bot_toggle_button.pack(side="left", padx=2)
        
        # Botão Reiniciar bot
        bot_restart_button = ctk.CTkButton(
            bot_controls_frame,
            text="🔄",
            width=40,
            command=lambda: self.reiniciar_bot(bot_id)
        )
        bot_restart_button.pack(side="left", padx=2)
        
        # Botão Remover bot
        bot_remove_button = ctk.CTkButton(
            bot_controls_frame,
            text="❌",
            width=40,
            command=lambda: self.remover_bot(bot_id),
            fg_color=("red", "darkred")
        )
        bot_remove_button.pack(side="left", padx=2)
        
        # Estatísticas do bot
        bot_stats_frame = ctk.CTkFrame(bot_frame)
        bot_stats_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        # Linha 1: Participações
        stats_row1 = ctk.CTkFrame(bot_stats_frame)
        stats_row1.pack(fill="x", pady=2)
        
        amateur_label = ctk.CTkLabel(stats_row1, text="🏅 Amateur: 0")
        amateur_label.pack(side="left", padx=10, pady=2)
        
        contender_label = ctk.CTkLabel(stats_row1, text="🏆 Contender: 0")
        contender_label.pack(side="left", padx=10, pady=2)
        
        errors_label = ctk.CTkLabel(stats_row1, text="❌ Erros: 0")
        errors_label.pack(side="left", padx=10, pady=2)
        
        # Linha 2: Saldo e tempo
        stats_row2 = ctk.CTkFrame(bot_stats_frame)
        stats_row2.pack(fill="x", pady=2)
        
        saldo_label = ctk.CTkLabel(stats_row2, text="💰 Saldo: R$ 0,00")
        saldo_label.pack(side="left", padx=10, pady=2)
        
        ultima_atividade_label = ctk.CTkLabel(stats_row2, text="📅 Última: Nunca")
        ultima_atividade_label.pack(side="left", padx=10, pady=2)
        
        # Salvar referências
        self.bot_frames[bot_id] = {
            'frame': bot_frame,
            'status_label': bot_status_label,
            'toggle_button': bot_toggle_button,
            'amateur_label': amateur_label,
            'contender_label': contender_label,
            'errors_label': errors_label,
            'saldo_label': saldo_label,
            'ultima_atividade_label': ultima_atividade_label
        }
        
        self.adicionar_log(f"➕ Bot {bot_id} adicionado à interface")
        
    def remover_bot(self, bot_id):
        """Remove um bot"""
        if bot_id in self.bot_frames:
            # Parar o bot primeiro
            if self.bot_manager.bot_existe(bot_id):
                self.bot_manager.parar_bot(bot_id)
                
            # Remover da interface
            self.bot_frames[bot_id]['frame'].destroy()
            del self.bot_frames[bot_id]
            
            self.adicionar_log(f"❌ Bot {bot_id} removido")
            
    def toggle_bot(self, bot_id):
        """Alterna estado do bot"""
        if self.bot_manager.bot_existe(bot_id):
            if self.bot_manager.bot_rodando(bot_id):
                self.bot_manager.parar_bot(bot_id)
                self.adicionar_log(f"⏹️ Bot {bot_id} parado")
            else:
                self.bot_manager.iniciar_bot(bot_id)
                self.adicionar_log(f"▶️ Bot {bot_id} iniciado")
        else:
            # Criar novo bot
            profile_path = self.profile_entry.get() or f"Profile-{bot_id}"
            
            # Validar número de tentativas
            try:
                max_tentativas = int(self.max_tentativas_var.get())
                if max_tentativas < 1:
                    max_tentativas = 1
                elif max_tentativas > 10:
                    max_tentativas = 10
            except ValueError:
                max_tentativas = 3
                self.max_tentativas_var.set("3")
                self.adicionar_log(f"⚠️ Valor inválido para tentativas, usando padrão (3)")
            
            bot = KeyDropBot(
                profile_path=profile_path,
                bot_id=bot_id,
                headless=self.headless_var.get(),
                login_mode=self.login_mode_var.get(),
                contender_mode=self.contender_mode_var.get(),
                mini_window=self.mini_window_var.get(),
                max_tentativas=max_tentativas
            )
            
            self.bot_manager.adicionar_bot(bot)
            self.bot_manager.iniciar_bot(bot_id)
            self.adicionar_log(f"🚀 Bot {bot_id} criado e iniciado (max tentativas: {max_tentativas})")
            
    def reiniciar_bot(self, bot_id):
        """Reinicia um bot específico"""
        if self.bot_manager.bot_existe(bot_id):
            self.bot_manager.reiniciar_bot(bot_id)
            self.adicionar_log(f"🔄 Bot {bot_id} reiniciado")
            
    def toggle_bots(self):
        """Alterna estado de todos os bots"""
        if self.running:
            self.parar_todos_bots()
        else:
            self.iniciar_todos_bots()
            
    def iniciar_todos_bots(self):
        """Inicia todos os bots"""
        self.running = True
        self.start_stop_button.configure(
            text="⏹️ Parar Todos os Bots",
            fg_color=("red", "darkred")
        )
        
        for bot_id in self.bot_frames.keys():
            self.toggle_bot(bot_id)
            
        self.adicionar_log("🚀 Todos os bots iniciados")
        
    def parar_todos_bots(self):
        """Para todos os bots"""
        self.running = False
        self.start_stop_button.configure(
            text="🚀 Iniciar Todos os Bots",
            fg_color=("green", "darkgreen")
        )
        
        self.bot_manager.parar_todos()
        self.adicionar_log("⏹️ Todos os bots parados")
        
    def reiniciar_todos(self):
        """Reinicia todos os bots"""
        self.bot_manager.reiniciar_todos()
        self.adicionar_log("🔄 Todos os bots reiniciados")
        
    def parada_emergencial(self):
        """Parada emergencial do sistema"""
        self.bot_manager.parada_emergencial()
        self.running = False
        self.start_stop_button.configure(
            text="🚀 Iniciar Todos os Bots",
            fg_color=("green", "darkgreen")
        )
        self.adicionar_log("🚨 PARADA EMERGENCIAL EXECUTADA")
        
    def selecionar_perfil(self):
        """Seleciona pasta do perfil"""
        pasta = filedialog.askdirectory(title="Selecionar Pasta do Perfil Chrome")
        if pasta:
            self.profile_entry.delete(0, tk.END)
            self.profile_entry.insert(0, pasta)
            self.adicionar_log(f"📁 Perfil selecionado: {pasta}")
            
    def carregar_config(self):
        """Carrega configuração do arquivo"""
        try:
            with open('bot_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Validar e adicionar campos padrão se necessário
                if 'max_tentativas' not in config:
                    config['max_tentativas'] = 3
                elif config['max_tentativas'] < 1:
                    config['max_tentativas'] = 1
                elif config['max_tentativas'] > 10:
                    config['max_tentativas'] = 10
                
                if 'discord_report_hours' not in config:
                    config['discord_report_hours'] = 12
                elif config['discord_report_hours'] < 1:
                    config['discord_report_hours'] = 1
                elif config['discord_report_hours'] > 168:
                    config['discord_report_hours'] = 168
                
                if 'telegram_token' not in config:
                    config['telegram_token'] = ''
                
                return config
        except:
            return {
                'max_tentativas': 3,
                'discord_report_hours': 12,
                'telegram_token': ''
            }
            
    def salvar_config(self):
        """Salva configuração atual"""
        # Validar número de tentativas
        try:
            max_tentativas = int(self.max_tentativas_var.get())
            if max_tentativas < 1:
                max_tentativas = 1
            elif max_tentativas > 10:
                max_tentativas = 10
        except ValueError:
            max_tentativas = 3
            self.max_tentativas_var.set("3")
        
        # Validar horas do relatório Discord
        try:
            discord_report_hours = int(self.discord_report_hours_var.get())
            if discord_report_hours < 1:
                discord_report_hours = 1
            elif discord_report_hours > 168:  # Máximo 1 semana
                discord_report_hours = 168
        except ValueError:
            discord_report_hours = 12
            self.discord_report_hours_var.set("12")
        
        config = {
            'profile_path': self.profile_entry.get(),
            'headless': self.headless_var.get(),
            'login_mode': self.login_mode_var.get(),
            'contender_mode': self.contender_mode_var.get(),
            'mini_window': self.mini_window_var.get(),
            'max_tentativas': max_tentativas,
            'discord_report_hours': discord_report_hours,
            'telegram_token': self.telegram_token_var.get()
        }
        
        try:
            with open('bot_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # Atualizar configuração interna
            self.config = config
            
            # Atualizar sistemas auxiliares
            self.atualizar_sistemas_auxiliares()
            
            self.adicionar_log(f"💾 Configuração salva (tentativas: {max_tentativas}, Discord: {discord_report_hours}h)")
            messagebox.showinfo("Sucesso", "Configuração salva com sucesso!")
        except Exception as e:
            self.adicionar_log(f"❌ Erro ao salvar configuração: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar configuração: {e}")
            
    def verificar_atualizacoes(self):
        """Verifica atualizações disponíveis"""
        try:
            from src.improved_update_manager import ImprovedUpdateManager
            
            update_manager = ImprovedUpdateManager()
            result = update_manager.check_for_updates()
            
            if result.get('available'):
                version = result.get('version')
                self.adicionar_log(f"🔄 Atualização disponível: v{version}")
                
                response = messagebox.askyesno(
                    "Atualização Disponível",
                    f"Nova versão {version} disponível!\n\nDeseja baixar agora?"
                )
                
                if response:
                    self.adicionar_log("📥 Iniciando download da atualização...")
                    # Implementar download em thread separada
                    threading.Thread(
                        target=self.download_update,
                        args=(update_manager,),
                        daemon=True
                    ).start()
            else:
                self.adicionar_log("✅ Sistema está atualizado")
                messagebox.showinfo("Atualizado", "Sistema está na versão mais recente!")
                
        except Exception as e:
            self.adicionar_log(f"❌ Erro ao verificar atualizações: {e}")
            messagebox.showerror("Erro", f"Erro ao verificar atualizações: {e}")
            
    def download_update(self, update_manager):
        """Faz download da atualização"""
        try:
            success = update_manager.download_update()
            if success:
                self.adicionar_log("✅ Atualização baixada com sucesso!")
                messagebox.showinfo("Sucesso", "Atualização baixada! Reinicie o programa.")
            else:
                self.adicionar_log("❌ Falha no download da atualização")
                messagebox.showerror("Erro", "Falha no download da atualização")
        except Exception as e:
            self.adicionar_log(f"❌ Erro no download: {e}")
            
    def abrir_logs(self):
        """Abre pasta de logs"""
        try:
            if os.path.exists("logs"):
                os.startfile("logs")
            else:
                messagebox.showwarning("Aviso", "Pasta de logs não encontrada")
        except Exception as e:
            self.adicionar_log(f"❌ Erro ao abrir logs: {e}")
            
    def obter_versao(self):
        """Obtém informações da versão"""
        try:
            with open('version.json', 'r') as f:
                return json.load(f)
        except:
            return {'version': '2.0.8', 'build': 'unknown'}
            
    def adicionar_log(self, mensagem):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {mensagem}\n"
        
        self.logs_text.insert("end", log_entry)
        self.logs_text.see("end")
        
    def iniciar_monitoramento(self):
        """Inicia thread de monitoramento"""
        self.monitor_thread = threading.Thread(
            target=self.monitor_loop,
            daemon=True
        )
        self.monitor_thread.start()
        
    def monitor_loop(self):
        """Loop de monitoramento do sistema"""
        while True:
            try:
                self.atualizar_interface()
                time.sleep(10)  # Atualizar a cada 10 segundos
            except Exception as e:
                print(f"Erro no monitoramento: {e}")
                time.sleep(10)
                
    def atualizar_interface(self):
        """Atualiza interface com dados atuais"""
        try:
            # Atualizar métricas do sistema
            if self.memory_manager and MEMORY_MANAGER_AVAILABLE:
                stats = self.memory_manager.get_stats()
                
                # Atualizar labels de sistema
                self.cpu_label.configure(text=f"💻 CPU: {stats.get('cpu_percent', 0):.1f}%")
                self.ram_label.configure(text=f"🧠 RAM: {stats.get('memory_mb', 0):.1f} MB")
                self.chrome_label.configure(text=f"🌐 Chrome: {stats.get('chrome_processes', 0)} processos")
                
                # Calcular uptime
                uptime = stats.get('uptime', 0)
                uptime_str = f"{int(uptime//3600)}h {int((uptime%3600)//60)}m {int(uptime%60)}s"
                self.uptime_label.configure(text=f"⏱️ Uptime: {uptime_str}")
                
                # Métricas detalhadas
                self.virtual_mem_label.configure(text=f"💾 Mem. Virtual: {stats.get('virtual_memory_mb', 0):.1f} MB")
                self.disk_label.configure(text=f"💿 Disco: {stats.get('disk_usage', 0):.1f}%")
                
                # Rede
                net_io = stats.get('network_io', {'bytes_sent': 0, 'bytes_recv': 0})
                total_net = net_io['bytes_sent'] + net_io['bytes_recv']
                self.network_label.configure(text=f"🌐 Rede: {total_net:.1f} MB")
                
                # Limpezas
                self.cleanup_label.configure(text=f"🧹 Limpezas: {stats.get('total_cleanups', 0)}")
                
            # Atualizar status dos bots
            for bot_id, frame_data in self.bot_frames.items():
                if self.bot_manager.bot_existe(bot_id):
                    bot = self.bot_manager.get_bot(bot_id)
                    stats = bot.obter_stats()
                    
                    # Atualizar status
                    status = bot.status
                    frame_data['status_label'].configure(text=status)
                    
                    # Atualizar botão
                    if self.bot_manager.bot_rodando(bot_id):
                        frame_data['toggle_button'].configure(text="⏹️ Parar")
                    else:
                        frame_data['toggle_button'].configure(text="▶️ Iniciar")
                    
                    # Atualizar estatísticas
                    frame_data['amateur_label'].configure(text=f"🏅 Amateur: {stats.get('amateur', 0)}")
                    frame_data['contender_label'].configure(text=f"🏆 Contender: {stats.get('contender', 0)}")
                    frame_data['errors_label'].configure(text=f"❌ Erros: {stats.get('erros', 0)}")
                    frame_data['saldo_label'].configure(text=f"💰 Saldo: {stats.get('saldo_skins', 'R$ 0,00')}")
                    frame_data['ultima_atividade_label'].configure(text=f"📅 {stats.get('ultima_atividade', 'Nunca')}")
                    
            # Atualizar status do sistema
            if self.running:
                self.system_status_label.configure(text="🟢 Sistema Ativo")
            else:
                self.system_status_label.configure(text="🔴 Sistema Parado")
                
        except Exception as e:
            print(f"Erro ao atualizar interface: {e}")
            
    def on_closing(self):
        """Chamado quando a janela é fechada"""
        try:
            # Parar todos os bots
            self.bot_manager.parar_todos("Interface fechada")
            
            # Parar sistemas auxiliares
            self.parar_sistemas_auxiliares()
            
            # Parar gerenciador de memória
            if self.memory_manager:
                self.memory_manager.stop()
                
            # Salvar configuração
            self.salvar_config()
            
            # Fechar aplicação
            self.root.destroy()
            
        except Exception as e:
            print(f"Erro ao fechar aplicação: {e}")
            self.root.destroy()
            
    def executar(self):
        """Inicia a aplicação"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def testar_telegram(self):
        """Testa conexão com o Telegram Bot"""
        token = self.telegram_token_var.get().strip()
        
        if not token:
            messagebox.showwarning("Aviso", "Digite o token do Telegram Bot primeiro!")
            return
        
        try:
            # Testa se o token é válido
            import requests
            response = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=5)
            
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get('ok'):
                    bot_name = bot_info['result']['first_name']
                    username = bot_info['result']['username']
                    self.adicionar_log(f"✅ Telegram conectado: @{username} ({bot_name})")
                    messagebox.showinfo("Sucesso", f"Telegram conectado com sucesso!\n\nBot: @{username}\nNome: {bot_name}")
                else:
                    self.adicionar_log("❌ Token do Telegram inválido")
                    messagebox.showerror("Erro", "Token do Telegram inválido!")
            else:
                self.adicionar_log("❌ Erro ao conectar com Telegram")
                messagebox.showerror("Erro", "Erro ao conectar com o Telegram!")
                
        except Exception as e:
            self.adicionar_log(f"❌ Erro no teste do Telegram: {e}")
            messagebox.showerror("Erro", f"Erro no teste do Telegram: {e}")
            
    def iniciar_telegram_bot(self):
        """Inicia o bot do Telegram"""
        try:
            from src.telegram_integration import TelegramBot, init_telegram_bot
            
            token = self.config.get('telegram_token', '').strip()
            if not token:
                self.adicionar_log("⚠️ Token do Telegram não configurado")
                return
            
            # Inicializar bot do Telegram
            telegram_bot = init_telegram_bot(token, self.bot_manager)
            if telegram_bot:
                self.adicionar_log("🤖 Bot do Telegram iniciado com sucesso!")
                return telegram_bot
            else:
                self.adicionar_log("❌ Falha ao iniciar bot do Telegram")
                return None
                
        except Exception as e:
            self.adicionar_log(f"❌ Erro ao iniciar Telegram: {e}")
            return None
        
    def iniciar_sistemas_auxiliares(self):
        """Inicia sistemas auxiliares (relatórios, telegram)"""
        try:
            # Inicializar sistema de relatórios
            from src.report_manager import init_report_manager
            self.report_manager = init_report_manager(self.bot_manager)
            
            if self.report_manager:
                self.report_manager.update_config(self.config)
                self.report_manager.start()
                self.adicionar_log("📊 Sistema de relatórios iniciado")
            
            # Inicializar bot do Telegram se configurado
            token = self.config.get('telegram_token', '').strip()
            if token:
                self.telegram_bot = self.iniciar_telegram_bot()
                if self.telegram_bot:
                    self.adicionar_log("🤖 Bot do Telegram conectado")
                    
        except Exception as e:
            self.adicionar_log(f"⚠️ Erro ao iniciar sistemas auxiliares: {e}")
    
    def parar_sistemas_auxiliares(self):
        """Para sistemas auxiliares"""
        try:
            if self.report_manager:
                self.report_manager.stop()
                self.adicionar_log("📊 Sistema de relatórios parado")
            
            if self.telegram_bot:
                from src.telegram_integration import stop_telegram_bot
                stop_telegram_bot()
                self.adicionar_log("🤖 Bot do Telegram desconectado")
                
        except Exception as e:
            self.adicionar_log(f"⚠️ Erro ao parar sistemas auxiliares: {e}")
    
    def atualizar_sistemas_auxiliares(self):
        """Atualiza configurações dos sistemas auxiliares"""
        try:
            if self.report_manager:
                self.report_manager.update_config(self.config)
                self.adicionar_log("📊 Configurações de relatório atualizadas")
                
        except Exception as e:
            self.adicionar_log(f"⚠️ Erro ao atualizar sistemas auxiliares: {e}")
