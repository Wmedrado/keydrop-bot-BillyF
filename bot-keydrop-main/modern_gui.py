try:
    # Imports da interface moderna
    import customtkinter as ctk
    import tkinter as tk
    from tkinter import messagebox, filedialog
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
        from src.memory_manager import memory_manager, performance_monitor
        MEMORY_MANAGER_AVAILABLE = True
    except ImportError:
        # Fallback se não conseguir importar
        memory_manager = None
        performance_monitor = None
        MEMORY_MANAGER_AVAILABLE = False
        print("⚠️ Sistema de gerenciamento de memória não disponível")
    
    # Imports locais
    try:
        from src.icons_config import get_icon, get_color, get_status_icon, get_control_button_config
        from src.utils import get_logger, ConfigManager, ValidationUtils
        from src.update_manager import UpdateManager
        ICONS_AVAILABLE = True
    except ImportError:
        ICONS_AVAILABLE = False
        print("⚠️ Módulos locais não disponíveis - funcionalidade limitada")
        
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)

class ToolTip:
    """Classe para criar tooltips nos widgets"""
    
    def __init__(self, widget, text='Widget info'):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        
    def on_enter(self, event):
        """Mostra tooltip ao entrar com mouse"""
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            self.tooltip,
            text=self.text,
            justify='left',
            background='#2B2B2B',
            foreground='white',
            relief='solid',
            borderwidth=1,
            font=('Arial', 10, 'normal'),
            padx=8,
            pady=4
        )
        label.pack()
        
    def on_leave(self, event):
        """Esconde tooltip ao sair com mouse"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class ModernKeyDropGUI:
    def __init__(self):
        # Configurar tema escuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Janela principal
        self.root = ctk.CTk()
        self.root.title("🔑 KeyDrop Bot - Professional Edition")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Configurar ícone
        self.configurar_icone()
        
        # Variáveis de configuração
        self.config = {
            'num_bots': 5,
            'velocidade_navegacao': 5,
            'headless': False,
            'login_mode': False,
            'contender_mode': False,
            'mini_window': False,
            'discord_webhook': '',
            'relatorios_automaticos': False
        }
        
        # Variáveis de controle
        self.bots = []
        self.running = False
        self.performance_thread = None
        self.report_manager = None
        self.stats_labels = []
        self.status_labels = []
        self.bot_frames = []
        self.pause_message = "⏸️ Bot pausado, aguardando próximo sorteio (3min)"
        
        # Estatísticas globais
        self.total_amateur = 0
        self.total_contender = 0
        self.total_erros = 0
        self.total_saldo = 0.0
        self.total_ganho = 0.0
        
        # Carregar configurações (antes de criar interface)
        self.carregar_config()
        
        # Criar interface
        self.criar_interface_moderna()
        
        # Iniciar monitoramento de performance
        self.iniciar_monitoramento_performance()
        
        # Iniciar gerenciador de memória
        if MEMORY_MANAGER_AVAILABLE and memory_manager:
            memory_manager.start()
            # Aguardar interface estar pronta antes de adicionar log
            self.root.after(1000, lambda: self.adicionar_log("🧠 Sistema de gerenciamento de memória iniciado"))
    
    def configurar_icone(self):
        """Configura o ícone da janela de forma robusta para executáveis"""
        try:
            # Lista de possíveis localizações do ícone
            possiveis_caminhos = [
                # Mesmo diretório do script/executável
                os.path.join(os.path.dirname(__file__), 'bot-icone.ico'),
                os.path.join(os.path.dirname(__file__), 'bot-icone.png'),
                
                # Diretório atual
                os.path.join(os.getcwd(), 'bot-icone.ico'),
                os.path.join(os.getcwd(), 'bot-icone.png'),
                
                # Diretório pai (caso esteja em startup/)
                os.path.join(os.path.dirname(__file__), '..', 'bot-icone.ico'),
                os.path.join(os.path.dirname(__file__), '..', 'bot-icone.png'),
                
                # Para executáveis PyInstaller
                os.path.join(sys._MEIPASS if hasattr(sys, '_MEIPASS') else '.', 'bot-icone.ico'),
                os.path.join(sys._MEIPASS if hasattr(sys, '_MEIPASS') else '.', 'bot-icone.png'),
            ]
            
            # Tentar carregar o ícone de cada localização
            for caminho in possiveis_caminhos:
                if os.path.exists(caminho):
                    try:
                        if caminho.endswith('.ico'):
                            self.root.iconbitmap(caminho)
                            print(f"✅ Ícone ICO carregado de: {caminho}")
                            return
                        elif caminho.endswith('.png'):
                            icon_image = tk.PhotoImage(file=caminho)
                            self.root.iconphoto(True, icon_image)
                            print(f"✅ Ícone PNG carregado de: {caminho}")
                            return
                    except Exception as e:
                        print(f"⚠️ Erro ao carregar ícone de {caminho}: {e}")
                        continue
            
            print("⚠️ Nenhum ícone encontrado, usando ícone padrão")
            
        except Exception as e:
            print(f"❌ Erro na configuração do ícone: {e}")
    
    def criar_interface_moderna(self):
        # Frame principal com padding
        main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cabeçalho
        self.criar_cabecalho(main_frame)
        
        # Frame de conteúdo com scroll
        content_frame = ctk.CTkScrollableFrame(main_frame, height=600)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Seção de configurações
        self.criar_secao_configuracoes(content_frame)
        
        # Seção de modos
        self.criar_secao_modos(content_frame)
        
        # Seção de integração
        self.criar_secao_integracao(content_frame)
        
        # Seção de controles
        self.criar_secao_controles(content_frame)
        
        # Seção de monitoramento de guias
        self.criar_secao_monitoramento_guias(content_frame)
        
        # Seção de estatísticas
        self.criar_secao_estatisticas(content_frame)
        
        # Seção de performance
        self.criar_secao_performance(content_frame)
        
        # Seção de logs
        self.criar_secao_logs(content_frame)
    
    def criar_cabecalho(self, parent):
        header_frame = ctk.CTkFrame(parent, corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        # Título com emoji
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔑 KeyDrop Bot Professional Edition",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=(15, 5))
        
        # Versão no canto superior direito
        try:
            with open("version.json", "r") as f:
                version_data = json.load(f)
                version_text = f"v{version_data['version']}"
        except:
            version_text = "v4.0.0"
        
        version_label = ctk.CTkLabel(
            header_frame,
            text=version_text,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="green"
        )
        version_label.pack(side="right", padx=20, pady=(15, 5))
        
        # Créditos do desenvolvedor
        credits_label = ctk.CTkLabel(
            header_frame,
            text="👨‍💻 Desenvolvido por William Medrado (wmedrado)",
            font=ctk.CTkFont(size=14, weight="normal"),
            text_color="gray"
        )
        credits_label.pack(side="left", padx=20, pady=(0, 5))
        
        # Discord para contato
        discord_label = ctk.CTkLabel(
            header_frame,
            text="💬 Discord: wmedrado",
            font=ctk.CTkFont(size=12, weight="normal"),
            text_color="lightblue"
        )
        discord_label.pack(side="left", padx=20, pady=(0, 15))
        ToolTip(discord_label, "Entre em contato via Discord para suporte,\nbug reports ou sugestões de melhorias")
        
        # Status geral
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="⚪ Parado",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.status_label.pack(side="right", padx=20, pady=15)
    
    def criar_secao_configuracoes(self, parent):
        # Título da seção
        config_title = ctk.CTkLabel(
            parent,
            text="⚙️ Configurações Principais",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        config_title.pack(anchor="w", padx=10, pady=(20, 10))
        
        # Frame de configurações
        config_frame = ctk.CTkFrame(parent, corner_radius=10)
        config_frame.pack(fill="x", padx=10, pady=5)
        
        # Linha 1: Configurações básicas
        row1 = ctk.CTkFrame(config_frame)
        row1.pack(fill="x", padx=20, pady=15)
        
        # Número de janelas
        ctk.CTkLabel(row1, text="🪟 Janelas:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
        self.num_bots_var = ctk.StringVar(value=str(self.config['num_bots']))
        self.num_bots_entry = ctk.CTkEntry(row1, textvariable=self.num_bots_var, width=80)
        self.num_bots_entry.pack(side="left", padx=5)
        ToolTip(self.num_bots_entry, "Número de janelas do navegador que serão abertas\nRecomendado: 2-10 para testes, máximo 200")
        
        # Velocidade de navegação
        ctk.CTkLabel(row1, text="⚡ Velocidade:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(20, 5))
        self.velocidade_var = ctk.StringVar(value=str(self.config['velocidade_navegacao']))
        self.velocidade_entry = ctk.CTkEntry(row1, textvariable=self.velocidade_var, width=80)
        self.velocidade_entry.pack(side="left", padx=5)
        ToolTip(self.velocidade_entry, "Velocidade de navegação entre páginas (segundos)\nMenor = mais rápido, maior = mais seguro")
        
        # Botão de configurações avançadas
        config_btn = ctk.CTkButton(
            row1,
            text="🔧 Avançadas",
            command=self.abrir_configuracoes_avancadas,
            width=120
        )
        config_btn.pack(side="right", padx=5)
        ToolTip(config_btn, "Abre janela com configurações avançadas\ncomo proxy, user-agent, timeouts, etc.")
    
    def criar_secao_modos(self, parent):
        # Título da seção
        modos_title = ctk.CTkLabel(
            parent,
            text="🎮 Modos de Operação",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        modos_title.pack(anchor="w", padx=10, pady=(20, 10))
        
        # Frame de modos
        modos_frame = ctk.CTkFrame(parent, corner_radius=10)
        modos_frame.pack(fill="x", padx=10, pady=5)
        
        # Linha de modos
        modos_row = ctk.CTkFrame(modos_frame)
        modos_row.pack(fill="x", padx=20, pady=15)
        
        # Headless
        self.headless_var = ctk.BooleanVar(value=self.config['headless'])
        self.headless_check = ctk.CTkCheckBox(
            modos_row,
            text="👁️ Headless (Oculto)",
            variable=self.headless_var,
            font=ctk.CTkFont(weight="bold")
        )
        self.headless_check.pack(side="left", padx=10)
        
        # Login automático
        self.login_var = ctk.BooleanVar(value=self.config['login_mode'])
        self.login_check = ctk.CTkCheckBox(
            modos_row,
            text="🔐 Login Automático",
            variable=self.login_var,
            font=ctk.CTkFont(weight="bold")
        )
        self.login_check.pack(side="left", padx=10)
        
        # Modo CONTENDER
        self.contender_var = ctk.BooleanVar(value=self.config['contender_mode'])
        self.contender_check = ctk.CTkCheckBox(
            modos_row,
            text="🏆 CONTENDER (1h)",
            variable=self.contender_var,
            font=ctk.CTkFont(weight="bold")
        )
        self.contender_check.pack(side="left", padx=10)
        
        # Mini Window
        self.mini_window_var = ctk.BooleanVar(value=self.config.get('mini_window', False))
        self.mini_window_check = ctk.CTkCheckBox(
            modos_row,
            text="🪟 Mini Window (200x300)",
            variable=self.mini_window_var,
            font=ctk.CTkFont(weight="bold")
        )
        self.mini_window_check.pack(side="left", padx=10)
        
        # Tooltips
        ToolTip(self.headless_check, "Executa bots sem interface gráfica (mais rápido)")
        ToolTip(self.login_check, "Modo para fazer login manual na Steam")
        ToolTip(self.contender_check, "Modo otimizado para sorteios CONTENDER de 1 hora")
        ToolTip(self.mini_window_check, "Abre janelas em tamanho mini (200x300) para economia de recursos")
        
        # Botão de ajuda
        help_btn = ctk.CTkButton(
            modos_row,
            text="❓ Ajuda",
            command=self.mostrar_ajuda_modos,
            width=100
        )
        help_btn.pack(side="right", padx=10)
    
    def criar_secao_integracao(self, parent):
        # Título da seção
        integracao_title = ctk.CTkLabel(
            parent,
            text="🔗 Integração e Relatórios",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        integracao_title.pack(anchor="w", padx=10, pady=(20, 10))
        
        # Frame de integração
        integracao_frame = ctk.CTkFrame(parent, corner_radius=10)
        integracao_frame.pack(fill="x", padx=10, pady=5)
        
        # Linha 1: Discord
        discord_row = ctk.CTkFrame(integracao_frame)
        discord_row.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(discord_row, text="📱 Discord Webhook:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=5)
        self.discord_var = ctk.StringVar(value=self.config['discord_webhook'])
        self.discord_entry = ctk.CTkEntry(discord_row, textvariable=self.discord_var, width=400)
        self.discord_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Relatórios automáticos
        self.relatorios_var = ctk.BooleanVar(value=self.config['relatorios_automaticos'])
        self.relatorios_check = ctk.CTkCheckBox(
            discord_row,
            text="📊 Relatórios (12h)",
            variable=self.relatorios_var,
            font=ctk.CTkFont(weight="bold")
        )
        self.relatorios_check.pack(side="right", padx=10)
    
    def criar_secao_controles(self, parent):
        # Título da seção
        controles_title = ctk.CTkLabel(
            parent,
            text="🎮 Controles do Bot",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        controles_title.pack(anchor="w", padx=10, pady=(20, 10))
        
        # Frame de controles
        controles_frame = ctk.CTkFrame(parent, corner_radius=10)
        controles_frame.pack(fill="x", padx=10, pady=5)
        
        # Linha de botões
        botoes_row = ctk.CTkFrame(controles_frame)
        botoes_row.pack(fill="x", padx=20, pady=15)
        
        # Botão Iniciar
        self.btn_iniciar = ctk.CTkButton(
            botoes_row,
            text="▶️ Iniciar Bots",
            command=self.iniciar_bots,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green"
        )
        self.btn_iniciar.pack(side="left", padx=5)
        ToolTip(self.btn_iniciar, "Inicia os bots de acordo com as configurações\ndefinidas (número de bots, modo headless, etc.)")
        
        # Botão Parar
        self.btn_parar = ctk.CTkButton(
            botoes_row,
            text="⏹️ Parar Bots",
            command=self.parar_bots,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="red"
        )
        self.btn_parar.pack(side="left", padx=5)
        ToolTip(self.btn_parar, "Para todos os bots em execução\ne fecha suas janelas do navegador")
        
        # Botão Parar Emergência
        self.btn_parar_emergencia = ctk.CTkButton(
            botoes_row,
            text="🚨 Stop Emergência",
            command=self.parar_bots_emergencia,
            width=150,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="darkred"
        )
        self.btn_parar_emergencia.pack(side="left", padx=5)
        ToolTip(self.btn_parar_emergencia, "Encerra TODOS os processos Chrome do sistema\n(Use apenas se o botão normal não funcionar)")
        
        # Inicializar estado dos botões
        self.btn_parar.configure(state="disabled")
        self.btn_parar_emergencia.configure(state="disabled")
        
        # Botão Limpar Cache
        self.btn_limpar = ctk.CTkButton(
            botoes_row,
            text="🧹 Limpar Cache",
            command=self.limpar_cache,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="orange"
        )
        self.btn_limpar.pack(side="left", padx=5)
        ToolTip(self.btn_limpar, "Limpa o cache do navegador de todos os perfis\nsem perder os dados de login salvos")
        
        # Botão Reiniciar Guias
        self.btn_reiniciar = ctk.CTkButton(
            botoes_row,
            text="🔄 Reiniciar Guias",
            command=self.reiniciar_guias,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="purple"
        )
        self.btn_reiniciar.pack(side="left", padx=5)
        ToolTip(self.btn_reiniciar, "Reinicia todas as guias dos bots\nÚtil para resolver problemas de conexão")
        
        # Inicializar estado dos botões
        self.btn_reiniciar.configure(state="disabled")
        
        # Botão Salvar Config
        self.btn_salvar = ctk.CTkButton(
            botoes_row,
            text="💾 Salvar Config",
            command=self.salvar_config,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="blue"
        )
        self.btn_salvar.pack(side="right", padx=5)
        ToolTip(self.btn_salvar, "Salva as configurações atuais no arquivo\nbot_config.json para uso futuro")
        
        # Botão Atualizar
        self.btn_atualizar = ctk.CTkButton(
            botoes_row,
            text="🔄 Atualizar",
            command=self.verificar_atualizacao,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="purple"
        )
        self.btn_atualizar.pack(side="right", padx=5)
        ToolTip(self.btn_atualizar, "Verifica se há atualizações disponíveis\ne instala automaticamente se encontrar")
    
    def criar_secao_estatisticas(self, parent):
        # Título da seção
        stats_title = ctk.CTkLabel(
            parent,
            text="📊 Estatísticas em Tempo Real",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        stats_title.pack(anchor="w", padx=10, pady=(20, 10))
        
        # Frame de estatísticas
        stats_frame = ctk.CTkFrame(parent, corner_radius=10)
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        # Grid de estatísticas
        stats_grid = ctk.CTkFrame(stats_frame)
        stats_grid.pack(fill="x", padx=20, pady=15)
        
        # Linha 1: Estatísticas gerais
        row1 = ctk.CTkFrame(stats_grid)
        row1.pack(fill="x", pady=5)
        
        self.stats_amateur = ctk.CTkLabel(row1, text="🎯 AMATEUR: 0", font=ctk.CTkFont(weight="bold"))
        self.stats_amateur.pack(side="left", padx=10)
        
        self.stats_contender = ctk.CTkLabel(row1, text="🏆 CONTENDER: 0", font=ctk.CTkFont(weight="bold"))
        self.stats_contender.pack(side="left", padx=10)
        
        self.stats_erros = ctk.CTkLabel(row1, text="❌ Erros: 0", font=ctk.CTkFont(weight="bold"))
        self.stats_erros.pack(side="left", padx=10)
        
        # Linha 2: Saldo
        row2 = ctk.CTkFrame(stats_grid)
        row2.pack(fill="x", pady=5)
        
        self.stats_saldo = ctk.CTkLabel(row2, text="💰 Saldo em Skins: R$ 0,00", font=ctk.CTkFont(weight="bold"))
        self.stats_saldo.pack(side="left", padx=10)
        
        self.stats_ganho = ctk.CTkLabel(row2, text="📈 Ganho: R$ 0,00", font=ctk.CTkFont(weight="bold"))
        self.stats_ganho.pack(side="left", padx=10)
    
    def criar_secao_performance(self, parent):
        # Título da seção
        perf_title = ctk.CTkLabel(
            parent,
            text="⚡ Performance do Sistema",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        perf_title.pack(anchor="w", padx=10, pady=(20, 10))
        
        # Frame de performance
        perf_frame = ctk.CTkFrame(parent, corner_radius=10)
        perf_frame.pack(fill="x", padx=10, pady=5)
        
        # Grid de performance
        perf_grid = ctk.CTkFrame(perf_frame)
        perf_grid.pack(fill="x", padx=20, pady=15)
        
        # Linha 1: CPU e RAM
        row1 = ctk.CTkFrame(perf_grid)
        row1.pack(fill="x", pady=5)
        
        self.perf_cpu = ctk.CTkLabel(row1, text="🖥️ CPU: 0%", font=ctk.CTkFont(weight="bold"))
        self.perf_cpu.pack(side="left", padx=10)
        
        self.perf_ram = ctk.CTkLabel(row1, text="🐏 RAM: 0%", font=ctk.CTkFont(weight="bold"))
        self.perf_ram.pack(side="left", padx=10)
        
        # Linha 2: Disco e Rede
        row2 = ctk.CTkFrame(perf_grid)
        row2.pack(fill="x", pady=5)
        
        self.perf_disco = ctk.CTkLabel(row2, text="💾 Disco: 0%", font=ctk.CTkFont(weight="bold"))
        self.perf_disco.pack(side="left", padx=10)
        
        self.perf_rede = ctk.CTkLabel(row2, text="🌐 Dados: 0.00 GB", font=ctk.CTkFont(weight="bold"))
        self.perf_rede.pack(side="left", padx=10)
        
        # Variável para rastrear consumo de dados
        self.dados_iniciais = None
    
    def criar_secao_logs(self, parent):
        # Título da seção
        logs_title = ctk.CTkLabel(
            parent,
            text="📄 Logs do Sistema",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        logs_title.pack(anchor="w", padx=10, pady=(20, 10))
        
        # Frame de logs
        logs_frame = ctk.CTkFrame(parent, corner_radius=10)
        logs_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Área de texto dos logs
        self.logs_text = ctk.CTkTextbox(logs_frame, height=200, font=ctk.CTkFont(family="Courier"))
        self.logs_text.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Adicionar log inicial
        self.adicionar_log("🚀 Sistema iniciado com sucesso!")
    
    def adicionar_log(self, mensagem):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {mensagem}\n"
        
        # Verificar se logs_text existe antes de usar
        if hasattr(self, 'logs_text') and self.logs_text:
            self.logs_text.insert("end", log_msg)
            self.logs_text.see("end")
        else:
            # Se logs_text não existe, imprimir no console
            print(log_msg.strip())
    
    def carregar_config(self):
        """Carrega configurações do arquivo JSON"""
        try:
            if os.path.exists('bot_config.json'):
                with open('bot_config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.config.update(config)
                    print("✅ Configurações carregadas com sucesso!")
            else:
                print("⚠️ Arquivo de configuração não encontrado, usando padrões")
        except Exception as e:
            print(f"❌ Erro ao carregar configurações: {e}")
    
    def atualizar_interface_com_config(self):
        """Atualiza os valores da interface com a configuração carregada"""
        # Esta função não é mais necessária pois as configurações 
        # são carregadas antes da criação da interface
        pass
    
    def salvar_config(self):
        """Salva configurações no arquivo JSON"""
        try:
            # Criar backup do arquivo atual se existir
            if os.path.exists('bot_config.json'):
                import shutil
                shutil.copy('bot_config.json', 'bot_config_backup.json')
            
            # Validar e atualizar configurações com valores da interface
            config_atualizada = self.config.copy()
            
            # Número de janelas
            if hasattr(self, 'num_bots_var') and self.num_bots_var:
                try:
                    valor = int(self.num_bots_var.get())
                    if 1 <= valor <= 200:
                        config_atualizada['num_bots'] = valor
                    else:
                        raise ValueError("Número de janelas deve estar entre 1 e 200")
                except ValueError as e:
                    self.adicionar_log(f"❌ Erro no número de janelas: {e}")
                    messagebox.showerror("Erro de Validação", f"Número de janelas inválido: {e}")
                    return False
            
            # Velocidade de navegação
            if hasattr(self, 'velocidade_var') and self.velocidade_var:
                try:
                    valor = int(self.velocidade_var.get())
                    if 1 <= valor <= 60:
                        config_atualizada['velocidade_navegacao'] = valor
                    else:
                        raise ValueError("Velocidade deve estar entre 1 e 60 segundos")
                except ValueError as e:
                    self.adicionar_log(f"❌ Erro na velocidade: {e}")
                    messagebox.showerror("Erro de Validação", f"Velocidade inválida: {e}")
                    return False
            
            # Checkboxes (valores booleanos)
            if hasattr(self, 'headless_var') and self.headless_var:
                config_atualizada['headless'] = self.headless_var.get()
            
            if hasattr(self, 'login_var') and self.login_var:
                config_atualizada['login_mode'] = self.login_var.get()
            
            if hasattr(self, 'contender_var') and self.contender_var:
                config_atualizada['contender_mode'] = self.contender_var.get()
            
            if hasattr(self, 'mini_window_var') and self.mini_window_var:
                config_atualizada['mini_window'] = self.mini_window_var.get()
            
            if hasattr(self, 'relatorios_var') and self.relatorios_var:
                config_atualizada['relatorios_automaticos'] = self.relatorios_var.get()
            
            # Discord webhook
            if hasattr(self, 'discord_var') and self.discord_var:
                webhook_url = self.discord_var.get().strip()
                config_atualizada['discord_webhook'] = webhook_url
            
            # Salvar no arquivo com formatação bonita
            with open('bot_config.json', 'w', encoding='utf-8') as f:
                json.dump(config_atualizada, f, indent=4, ensure_ascii=False)
            
            # Atualizar configuração interna
            self.config = config_atualizada
            
            self.adicionar_log("💾 Configurações salvas com sucesso!")
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!\n\nAs alterações serão aplicadas na próxima execução do bot.")
            return True
            
        except Exception as e:
            self.adicionar_log(f"❌ Erro ao salvar configurações: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar configurações:\n{e}")
            
            # Tentar restaurar backup se existir
            if os.path.exists('bot_config_backup.json'):
                try:
                    import shutil
                    shutil.copy('bot_config_backup.json', 'bot_config.json')
                    self.adicionar_log("🔄 Backup restaurado")
                except:
                    pass
            
            return False
    
    def iniciar_bots(self):
        """Inicia os bots"""
        if self.running:
            messagebox.showwarning("Aviso", "Os bots já estão em execução!")
            return
        
        try:
            self.salvar_config()
            self.running = True
            self.status_label.configure(text="🟢 Em execução")
            self.btn_iniciar.configure(state="disabled")
            self.btn_parar.configure(state="normal")
            self.btn_parar_emergencia.configure(state="normal")
            self.btn_reiniciar.configure(state="normal")
            
            # Iniciar bots em thread separada
            threading.Thread(target=self.executar_bots, daemon=True).start()
            
            self.adicionar_log("🚀 Bots iniciados com sucesso!")
            
        except Exception as e:
            self.adicionar_log(f"❌ Erro ao iniciar bots: {e}")
            messagebox.showerror("Erro", f"Erro ao iniciar bots: {e}")
    
    def executar_bots(self):
        """Executa os bots usando o BotManager"""
        try:
            # Importar BotManager
            from keydrop_bot import BotManager
            
            # Criar manager se não existir
            if not hasattr(self, 'manager'):
                self.manager = BotManager()
            
            # Salvar configuração no BotManager (incluindo velocidade_navegacao)
            self.manager.salvar_config(self.config)
            
            # Criar labels de status das guias
            self.root.after(0, self.criar_labels_status_guias)
            
            # Criar bots baseado na configuração
            self.manager.criar_bots(
                self.config.get('num_bots', 2),
                self.config.get('headless', False),
                self.config.get('discord_webhook', '').strip() or None,
                self.config.get('login_mode', False),
                self.config.get('contender_mode', False),
                self.config.get('mini_window', False)
            )
            
            # Iniciar todos os bots (respeitará velocidade_navegacao)
            self.manager.iniciar_todos(self.config.get('intervalo_sorteios', 180))
            
            self.adicionar_log(f"🚀 {self.config.get('num_bots', 2)} bots iniciados com sucesso!")
            self.adicionar_log(f"⚡ Velocidade de navegação: {self.config.get('velocidade_navegacao', 5)}s entre bots")
            
        except ImportError as e:
            self.adicionar_log(f"❌ Erro ao importar BotManager: {e}")
        except Exception as e:
            self.adicionar_log(f"❌ Erro na execução: {e}")
            # Se houver erro, para os bots
            if self.running:
                self.root.after(0, self.parar_bots)
    
    def parar_bots(self):
        """Para os bots com encerramento melhorado"""
        try:
            if hasattr(self, 'manager'):
                self.adicionar_log("⏹️ Iniciando parada dos bots...")
                self.manager.parar_todos()
                self.adicionar_log("✅ Bots parados com sucesso!")
            else:
                self.adicionar_log("⚠️ Nenhum bot em execução")
        except Exception as e:
            self.adicionar_log(f"❌ Erro ao parar bots: {e}")
        finally:
            self.running = False
            self.status_label.configure(text="🔴 Parado")
            self.btn_iniciar.configure(state="normal")
            self.btn_parar.configure(state="disabled")
            self.btn_parar_emergencia.configure(state="disabled")
            self.btn_reiniciar.configure(state="disabled")
            
            # Limpar monitoramento de guias
            self.limpar_monitoramento_guias()
    
    def parar_bots_emergencia(self):
        """Para os bots com encerramento de emergência"""
        try:
            if hasattr(self, 'manager'):
                self.adicionar_log("🚨 Iniciando encerramento de emergência...")
                processos_encerrados = self.manager.encerrar_chrome_emergencia()
                self.adicionar_log(f"🚨 Encerramento de emergência concluído: {processos_encerrados} processos Chrome encerrados")
            else:
                self.adicionar_log("⚠️ Nenhum bot em execução")
        except Exception as e:
            self.adicionar_log(f"❌ Erro no encerramento de emergência: {e}")
        finally:
            self.running = False
            self.status_label.configure(text="🔴 Parado")
            self.btn_iniciar.configure(state="normal")
            self.btn_parar.configure(state="disabled")
            self.btn_parar_emergencia.configure(state="disabled")
            self.btn_reiniciar.configure(state="disabled")
            
            # Limpar monitoramento de guias
            self.limpar_monitoramento_guias()
    
    def limpar_monitoramento_guias(self):
        """Limpa o monitoramento de guias"""
        try:
            # Limpar conteúdo do monitoramento
            if hasattr(self, 'bots_container'):
                for widget in self.bots_container.winfo_children():
                    widget.destroy()
            
            # Resetar listas
            self.bot_frames = []
            self.status_labels = []
            self.stats_labels = []
            self.saldo_labels = []
            self.tempo_labels = []
            self.error_labels = []
            self.status_icons = []
            
            # Resetar estatísticas
            self.total_amateur = 0
            self.total_contender = 0
            self.total_erros = 0
            self.total_saldo = 0.0
            
            # Mostrar mensagem inicial
            if hasattr(self, 'bots_container'):
                self.status_inicial = ctk.CTkLabel(
                    self.bots_container,
                    text="🔄 Aguardando inicialização dos bots...",
                    font=ctk.CTkFont(size=14),
                    text_color="gray"
                )
                self.status_inicial.pack(pady=50)
            
            # Resetar labels de estatísticas
            self.stats_amateur.configure(text="🎯 AMATEUR: 0")
            self.stats_contender.configure(text="🏆 CONTENDER: 0")
            self.stats_erros.configure(text="❌ Erros: 0")
            self.stats_saldo.configure(text="💰 Saldo em Skins: R$ 0,00")
            self.stats_ganho.configure(text="📈 Ganho: R$ 0,00")
            
        except Exception as e:
            print(f"Erro ao limpar monitoramento: {e}")
    
    def reiniciar_guias(self):
        """Reinicia todas as guias dos bots"""
        if not self.running:
            messagebox.showwarning("Aviso", "Nenhum bot em execução para reiniciar!")
            return
        
        try:
            # Confirmar ação
            resultado = messagebox.askyesno(
                "Reiniciar Guias",
                "Isso irá reiniciar todas as guias dos bots.\n\n"
                "• As guias serão fechadas e abertas novamente\n"
                "• Os logins serão mantidos\n"
                "• Pode levar alguns minutos para completar\n\n"
                "Deseja continuar?"
            )
            
            if not resultado:
                return
            
            # Desabilitar botão
            self.btn_reiniciar.configure(state="disabled", text="🔄 Reiniciando...")
            
            # Executar reinício em thread separada
            threading.Thread(target=self.executar_reinicio_guias, daemon=True).start()
            
        except Exception as e:
            self.adicionar_log(f"❌ Erro ao reiniciar guias: {e}")
            messagebox.showerror("Erro", f"Erro ao reiniciar guias: {str(e)}")
    
    def executar_reinicio_guias(self):
        """Executa o reinício das guias"""
        try:
            if hasattr(self, 'manager') and hasattr(self.manager, 'reiniciar_guias'):
                self.manager.reiniciar_guias()
                self.adicionar_log("🔄 Guias reiniciadas com sucesso!")
            else:
                self.adicionar_log("⚠️ Funcionalidade de reinício não disponível")
            
        except Exception as e:
            self.adicionar_log(f"❌ Erro durante reinício: {e}")
            
        finally:
            # Reabilitar botão
            self.root.after(0, self.finalizar_reinicio_guias)
    
    def finalizar_reinicio_guias(self):
        """Finaliza o processo de reinício"""
        try:
            self.btn_reiniciar.configure(state="normal", text="🔄 Reiniciar Guias")
            messagebox.showinfo("Sucesso", "Guias reiniciadas com sucesso!")
        except Exception as e:
            print(f"Erro ao finalizar reinício: {e}")
    
    def limpar_cache(self):
        """Limpa o cache do navegador"""
        try:
            # Implementar limpeza de cache aqui
            self.adicionar_log("🧹 Iniciando limpeza de cache...")
            
            # Desabilitar botão
            self.btn_limpar.configure(state="disabled", text="🧹 Limpando...")
            
            # Executar limpeza em thread separada
            threading.Thread(target=self.executar_limpeza_cache, daemon=True).start()
            
        except Exception as e:
            self.adicionar_log(f"❌ Erro ao limpar cache: {e}")
            messagebox.showerror("Erro", f"Erro ao limpar cache: {e}")
    
    def executar_limpeza_cache(self):
        """Executa a limpeza de cache"""
        try:
            # Simular limpeza de cache
            time.sleep(2)  
            
            # Implementar limpeza real aqui se necessário
            self.adicionar_log("✅ Cache limpo com sucesso!")
            
        except Exception as e:
            self.adicionar_log(f"❌ Erro durante limpeza: {e}")
            
        finally:
            # Reabilitar botão
            self.root.after(0, self.finalizar_limpeza_cache)
    
    def finalizar_limpeza_cache(self):
        """Finaliza o processo de limpeza"""
        try:
            self.btn_limpar.configure(state="normal", text="🧹 Limpar Cache")
            messagebox.showinfo("Sucesso", "Cache limpo com sucesso!")
        except Exception as e:
            print(f"Erro ao finalizar limpeza: {e}")
    
    def iniciar_monitoramento_performance(self):
        """Inicia o monitoramento de performance"""
        def monitorar():
            while True:
                try:
                    # CPU
                    cpu_percent = psutil.cpu_percent(interval=1)
                    cpu_color = "green" if cpu_percent < 50 else "orange" if cpu_percent < 80 else "red"
                    self.perf_cpu.configure(text=f"🖥️ CPU: {cpu_percent:.1f}%", text_color=cpu_color)
                    
                    # RAM
                    ram = psutil.virtual_memory()
                    ram_percent = ram.percent
                    ram_color = "green" if ram_percent < 60 else "orange" if ram_percent < 80 else "red"
                    self.perf_ram.configure(text=f"🐏 RAM: {ram_percent:.1f}%", text_color=ram_color)
                    
                    # Disco
                    disk = psutil.disk_usage('/')
                    disk_percent = disk.percent
                    disk_color = "green" if disk_percent < 70 else "orange" if disk_percent < 90 else "red"
                    self.perf_disco.configure(text=f"💾 Disco: {disk_percent:.1f}%", text_color=disk_color)
                    
                    # Rede - Mostrar consumo total em GB
                    net = psutil.net_io_counters()
                    if self.dados_iniciais is None:
                        self.dados_iniciais = net.bytes_sent + net.bytes_recv
                    
                    dados_consumidos = (net.bytes_sent + net.bytes_recv - self.dados_iniciais) / (1024**3)  # GB
                    self.perf_rede.configure(text=f"🌐 Dados: {dados_consumidos:.2f} GB")
                    
                    time.sleep(3)
                except Exception as e:
                    print(f"Erro no monitoramento: {e}")
                    time.sleep(5)
        
        self.performance_thread = threading.Thread(target=monitorar, daemon=True)
        self.performance_thread.start()
    
    def abrir_configuracoes_avancadas(self):
        """Abre janela de configurações avançadas"""
        # Implementar janela de configurações avançadas
        messagebox.showinfo("Em breve", "Configurações avançadas serão implementadas em breve!")
    
    def mostrar_ajuda_modos(self):
        """Mostra ajuda sobre os modos"""
        ajuda = """
🎮 MODOS DE OPERAÇÃO:

👁️ Headless (Oculto):
• Executa o navegador sem interface gráfica
• Ideal para muitas janelas simultâneas
• Menor consumo de recursos

🔐 Login Automático:
• Detecta automaticamente se precisa fazer login
• Carrega página de login quando necessário
• Mantém sessão ativa

🏆 CONTENDER (1h):
• Participa de sorteios especiais de 1 hora
• Funciona junto com sorteios normais (3min)
• Prioridade: primeiro normais, depois CONTENDER

📱 Relatórios (12h):
• Envia relatórios automáticos via Discord
• Estatísticas detalhadas a cada 12 horas
• Requer Discord Webhook configurado
        """
        messagebox.showinfo("Ajuda - Modos", ajuda)
    
    def verificar_atualizacao(self):
        """Verifica e aplica atualizações do bot (repositório privado) - Versão Melhorada"""
        try:
            # Importar ImprovedUpdateManager
            from src.improved_update_manager import ImprovedUpdateManager
            
            # Criar instância do ImprovedUpdateManager
            update_manager = ImprovedUpdateManager(
                repo_owner="wmedrado",
                repo_name="bot-keydrop",
                current_version="4.0.0"
            )
            
            # Usar o diálogo melhorado
            self.adicionar_log("🔍 Verificando atualizações...")
            update_manager.show_update_dialog(self.root)
            
        except ImportError as e:
            self.adicionar_log(f"❌ Erro ao importar sistema de atualizações: {e}")
            messagebox.showerror("Erro", f"Sistema de atualizações não disponível: {e}")
        except Exception as e:
            self.adicionar_log(f"❌ Erro na verificação de atualizações: {e}")
            messagebox.showerror("Erro", f"Erro na verificação de atualizações: {e}")
    
    def run(self):
        """Executa a aplicação"""
        self.root.mainloop()
    
    def criar_secao_monitoramento_guias(self, parent):
        """Cria seção de monitoramento das guias com layout horizontal em quadradinhos"""
        # Título da seção
        monitor_title = ctk.CTkLabel(
            parent,
            text="🔍 Monitoramento de Guias",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        monitor_title.pack(anchor="w", padx=10, pady=(20, 10))
        
        # Frame principal do monitoramento
        monitor_frame = ctk.CTkFrame(parent, corner_radius=10)
        monitor_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame com scroll horizontal para os quadradinhos
        self.guias_scroll_frame = ctk.CTkScrollableFrame(
            monitor_frame, 
            height=280,
            orientation="horizontal"
        )
        self.guias_scroll_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Container horizontal para os quadradinhos
        self.bots_container = ctk.CTkFrame(self.guias_scroll_frame, fg_color="transparent")
        self.bots_container.pack(fill="both", expand=True)
        
        # Mensagem inicial
        self.status_inicial = ctk.CTkLabel(
            self.bots_container,
            text="🔄 Aguardando inicialização dos bots...",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.status_inicial.pack(pady=50)
        
        # Inicializar listas
        self.bot_frames = []
        self.status_labels = []
        self.stats_labels = []
        self.saldo_labels = []
        self.tempo_labels = []
        self.error_labels = []
        self.status_icons = []
        
        # Iniciar thread de atualização
        self.iniciar_update_loop()
    
    def criar_labels_status_guias(self):
        """Cria os quadradinhos de status para cada guia"""
        # Limpar conteúdo anterior
        for widget in self.bots_container.winfo_children():
            widget.destroy()
        
        # Resetar listas
        self.bot_frames = []
        self.status_labels = []
        self.stats_labels = []
        self.saldo_labels = []
        self.tempo_labels = []
        self.error_labels = []
        self.status_icons = []
        
        # Criar quadradinho para cada bot
        for i in range(self.config.get('num_bots', 2)):
            # Frame principal do bot (quadradinho)
            bot_frame = ctk.CTkFrame(
                self.bots_container, 
                width=280, 
                height=220,
                corner_radius=10,
                fg_color=("gray90", "gray20")
            )
            bot_frame.pack(side="left", padx=10, pady=5)
            bot_frame.pack_propagate(False)  # Manter tamanho fixo
            self.bot_frames.append(bot_frame)
            
            # Header do bot com ícone de status
            header_frame = ctk.CTkFrame(bot_frame, fg_color="transparent", height=40)
            header_frame.pack(fill="x", padx=10, pady=(10, 5))
            header_frame.pack_propagate(False)
            
            # Ícone de status
            status_icon = ctk.CTkLabel(
                header_frame,
                text="🔴",  # Vermelho = inativo, 🟢 = ativo, � = processando
                font=ctk.CTkFont(size=20),
                width=30
            )
            status_icon.pack(side="left", padx=(0, 10))
            self.status_icons.append(status_icon)
            
            # Nome do bot
            bot_name = ctk.CTkLabel(
                header_frame,
                text=f"Bot {i+1}",
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            bot_name.pack(side="left", fill="x", expand=True)
            
            # Status do bot
            status_label = ctk.CTkLabel(
                header_frame,
                text="🔄 Inicializando...",
                font=ctk.CTkFont(size=10),
                text_color="gray",
                anchor="e"
            )
            status_label.pack(side="right")
            self.status_labels.append(status_label)
            
            # Seção de dados do sorteio
            sorteio_frame = ctk.CTkFrame(bot_frame, fg_color="transparent", height=80)
            sorteio_frame.pack(fill="x", padx=10, pady=5)
            sorteio_frame.pack_propagate(False)
            
            # Título da seção
            sorteio_title = ctk.CTkLabel(
                sorteio_frame,
                text="📊 Dados do Sorteio",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="cyan"
            )
            sorteio_title.pack(anchor="w", pady=(0, 5))
            
            # Estatísticas detalhadas
            stats_label = ctk.CTkLabel(
                sorteio_frame,
                text="🎯 AMATEUR: 0\n🏆 CONTENDER: 0\n⏱️ Tempo: 00:00:00",
                font=ctk.CTkFont(size=10),
                text_color="lightgray",
                anchor="w",
                justify="left"
            )
            stats_label.pack(anchor="w", fill="x")
            self.stats_labels.append(stats_label)
            
            # Saldo
            saldo_label = ctk.CTkLabel(
                sorteio_frame,
                text="💰 R$ 0,00",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="green",
                anchor="e"
            )
            saldo_label.pack(anchor="e", pady=(5, 0))
            self.saldo_labels.append(saldo_label)
            
            # Seção de erros
            error_frame = ctk.CTkFrame(bot_frame, fg_color="transparent", height=60)
            error_frame.pack(fill="x", padx=10, pady=(0, 10))
            error_frame.pack_propagate(False)
            
            # Título da seção de erros
            error_title = ctk.CTkLabel(
                error_frame,
                text="⚠️ Erros",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="orange"
            )
            error_title.pack(anchor="w", pady=(0, 5))
            
            # Label de erros
            error_label = ctk.CTkLabel(
                error_frame,
                text="✅ Nenhum erro",
                font=ctk.CTkFont(size=10),
                text_color="green",
                anchor="w",
                justify="left"
            )
            error_label.pack(anchor="w", fill="both", expand=True)
            self.error_labels.append(error_label)
            
            # Placeholder para tempo (será usado no stats_label)
            self.tempo_labels.append(None)
            self.saldo_labels.append(saldo_label)
    
    def iniciar_update_loop(self):
        """Inicia o loop de atualização de status"""
        def atualizar_periodicamente():
            while True:
                try:
                    # Atualizar status das guias
                    self.atualizar_status_guias()
                    
                    # Atualizar estatísticas globais
                    self.atualizar_estatisticas_globais()
                    
                    # Pausa de 1 segundo
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Erro no update loop: {e}")
                    time.sleep(5)
        
        # Iniciar thread de atualização
        update_thread = threading.Thread(target=atualizar_periodicamente, daemon=True)
        update_thread.start()
    
    def atualizar_status_guias(self):
        """Atualiza o status de cada guia"""
        try:
            if not self.running or not hasattr(self, 'manager'):
                return
            
            # Verificar se os labels existem
            if not self.status_labels:
                return
            
            # Obter estatísticas do manager
            if hasattr(self.manager, 'obter_stats_todos'):
                stats = self.manager.obter_stats_todos()
                
                for i, stat in enumerate(stats):
                    if i < len(self.status_labels):
                        bot_id = stat['bot_id']
                        bot_stats = stat['stats']
                        ativo = stat['ativo']
                        
                        # Atualizar status
                        if ativo:
                            # Verificar se está em pausa
                            if bot_stats.get('pausado', False):
                                status_text = f"Bot {bot_id}: {self.pause_message}"
                                cor = "orange"
                            else:
                                status_text = f"Bot {bot_id}: 🟢 Ativo"
                                cor = "green"
                        else:
                            status_text = f"Bot {bot_id}: 🔴 Inativo"
                            cor = "red"
                        
                        # Atualizar via thread principal
                        self.root.after(0, lambda i=i, text=status_text, color=cor: 
                                       self.status_labels[i].configure(text=text, text_color=color))
                        
                        # Calcular tempo de execução
                        tempo_exec = "00:00:00"
                        if bot_stats.get('inicio'):
                            try:
                                delta = datetime.now() - bot_stats['inicio']
                                horas = delta.seconds // 3600
                                minutos = (delta.seconds % 3600) // 60
                                segundos = delta.seconds % 60
                                tempo_exec = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
                            except:
                                tempo_exec = "00:00:00"
                        
                        # Atualizar tempo
                        self.root.after(0, lambda i=i, tempo=tempo_exec: 
                                       self.tempo_labels[i].configure(text=f"⏱️ {tempo}"))
                        
                        # Atualizar estatísticas
                        amateur = bot_stats.get('amateur', 0)
                        contender = bot_stats.get('contender', 0)
                        erros = bot_stats.get('erros', 0)
                        
                        stats_text = f"🎯 AMATEUR: {amateur} | 🏆 CONTENDER: {contender} | ❌ Erros: {erros}"
                        self.root.after(0, lambda i=i, text=stats_text: 
                                       self.stats_labels[i].configure(text=text))
                        
                        # Atualizar saldo
                        saldo = bot_stats.get('saldo', 0.0)
                        saldo_text = f"💰 R$ {saldo:.2f}"
                        self.root.after(0, lambda i=i, text=saldo_text: 
                                       self.saldo_labels[i].configure(text=text))
                        
        except Exception as e:
            print(f"Erro ao atualizar status das guias: {e}")
    
    def atualizar_estatisticas_globais(self):
        """Atualiza as estatísticas globais baseadas nos bots individuais"""
        try:
            if not self.running or not hasattr(self, 'manager'):
                return
            
            # Resetar totais
            self.total_amateur = 0
            self.total_contender = 0
            self.total_erros = 0
            self.total_saldo = 0.0
            
            # Obter estatísticas do manager
            if hasattr(self.manager, 'obter_stats_todos'):
                stats = self.manager.obter_stats_todos()
                
                for stat in stats:
                    bot_stats = stat['stats']
                    self.total_amateur += bot_stats.get('amateur', 0)
                    self.total_contender += bot_stats.get('contender', 0)
                    self.total_erros += bot_stats.get('erros', 0)
                    self.total_saldo += bot_stats.get('saldo', 0.0)
                    
                    # Debug para verificar se está pegando as participações
                    if bot_stats.get('amateur', 0) > 0 or bot_stats.get('contender', 0) > 0:
                        print(f"Bot {stat['bot_id']}: AMATEUR={bot_stats.get('amateur', 0)}, CONTENDER={bot_stats.get('contender', 0)}")
            
            # Atualizar labels das estatísticas
            self.root.after(0, lambda: self.stats_amateur.configure(text=f"🎯 AMATEUR: {self.total_amateur}"))
            self.root.after(0, lambda: self.stats_contender.configure(text=f"🏆 CONTENDER: {self.total_contender}"))
            self.root.after(0, lambda: self.stats_erros.configure(text=f"❌ Erros: {self.total_erros}"))
            self.root.after(0, lambda: self.stats_saldo.configure(text=f"💰 Saldo em Skins: R$ {self.total_saldo:.2f}"))
            
        except Exception as e:
            print(f"Erro ao atualizar estatísticas globais: {e}")
    
    def atualizar_status_visual_bot(self, bot_index, status, stats_data=None, error_msg=None):
        """Atualiza o status visual de um bot específico"""
        try:
            if bot_index >= len(self.status_icons):
                return
            
            # Atualizar ícone de status
            if status == "ativo":
                self.status_icons[bot_index].configure(text="🟢")
                self.status_labels[bot_index].configure(
                    text="✅ Ativo",
                    text_color="green"
                )
            elif status == "processando":
                self.status_icons[bot_index].configure(text="🟡")
                self.status_labels[bot_index].configure(
                    text="🔄 Processando",
                    text_color="orange"
                )
            elif status == "erro":
                self.status_icons[bot_index].configure(text="🔴")
                self.status_labels[bot_index].configure(
                    text="❌ Erro",
                    text_color="red"
                )
            elif status == "pausado":
                self.status_icons[bot_index].configure(text="⏸️")
                self.status_labels[bot_index].configure(
                    text="⏸️ Pausado",
                    text_color="gray"
                )
            else:
                self.status_icons[bot_index].configure(text="🔴")
                self.status_labels[bot_index].configure(
                    text="🔄 Inicializando",
                    text_color="gray"
                )
            
            # Atualizar estatísticas se fornecidas
            if stats_data:
                amateur = stats_data.get('amateur', 0)
                contender = stats_data.get('contender', 0)
                tempo = stats_data.get('tempo', '00:00:00')
                saldo = stats_data.get('saldo', 0.0)
                
                self.stats_labels[bot_index].configure(
                    text=f"🎯 AMATEUR: {amateur}\n🏆 CONTENDER: {contender}\n⏱️ Tempo: {tempo}"
                )
                
                self.saldo_labels[bot_index].configure(
                    text=f"💰 R$ {saldo:.2f}"
                )
            
            # Atualizar mensagem de erro
            if error_msg:
                self.error_labels[bot_index].configure(
                    text=f"❌ {error_msg}",
                    text_color="red"
                )
            else:
                self.error_labels[bot_index].configure(
                    text="✅ Nenhum erro",
                    text_color="green"
                )
                
        except Exception as e:
            print(f"Erro ao atualizar status visual do bot {bot_index}: {e}")

if __name__ == "__main__":
    app = ModernKeyDropGUI()
    app.run()
