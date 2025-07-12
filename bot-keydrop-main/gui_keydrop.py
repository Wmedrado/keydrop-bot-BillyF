import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import json
import os
import sys
import psutil
from datetime import datetime
from keydrop_bot import BotManager

# Ícone na bandeja
try:
    import pystray
    from PIL import Image
    PYSTRAY_AVAILABLE = True
except Exception:
    PYSTRAY_AVAILABLE = False

class ToolTip:
    """Classe para criar tooltips explicativos"""
    
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip = None
        self.id = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Button-1>", self.on_click)
    
    def on_enter(self, event=None):
        self.schedule_tooltip()
    
    def on_leave(self, event=None):
        self.cancel_tooltip()
        self.hide_tooltip()
    
    def on_click(self, event=None):
        self.show_info_popup()
    
    def schedule_tooltip(self):
        self.cancel_tooltip()
        self.id = self.widget.after(self.delay, self.show_tooltip)
    
    def cancel_tooltip(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
    
    def show_tooltip(self):
        if self.tooltip:
            return
        
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            self.tooltip,
            text=self.text,
            background="#2C2F33",
            foreground="white",
            relief="solid",
            borderwidth=1,
            font=("Arial", 9),
            padx=8,
            pady=4
        )
        label.pack()
    
    def hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
    
    def show_info_popup(self):
        """Mostra popup com informações detalhadas"""
        if "Headless" in self.text:
            title = "🔳 Modo Headless"
            message = """MODO HEADLESS - Execução Silenciosa

📋 DESCRIÇÃO:
• Executa o navegador sem interface gráfica
• Consome menos recursos do sistema
• Ideal para uso em segundo plano

✅ VANTAGENS:
• Menor uso de CPU e RAM
• Não interfere no trabalho
• Melhor performance geral

❌ DESVANTAGENS:
• Não é possível visualizar o navegador
• Mais difícil para debug
• Pode ser detectado por alguns sites

🎯 RECOMENDADO PARA:
• Execução em massa (50+ janelas)
• Servidores sem interface gráfica
• Uso profissional 24/7"""
        
        elif "Login" in self.text:
            title = "🔐 Modo Login"
            message = """MODO LOGIN - Autenticação Manual

📋 DESCRIÇÃO:
• Permite login manual nas contas
• Mantém sessão entre execuções
• Navegador visível para interação

✅ VANTAGENS:
• Suporte a contas logadas
• Maior taxa de sucesso
• Evita captchas frequentes

❌ DESVANTAGENS:
• Requer configuração manual
• Mais lento para iniciar
• Consome mais recursos

🎯 RECOMENDADO PARA:
• Contas premium/VIP
• Sorteios com requisitos especiais
• Uso com poucas janelas (1-10)"""
        
        elif "CONTENDER" in self.text:
            title = "🏆 Modo CONTENDER"
            message = """MODO CONTENDER - Entrada Horária

📋 DESCRIÇÃO:
• Entra em sorteios a cada 1 hora
• Prioriza sorteios de maior valor
• Estatísticas separadas do modo normal

✅ VANTAGENS:
• Foco em sorteios premium
• Menor desgaste do sistema
• Melhor custo-benefício

❌ DESVANTAGENS:
• Menos entradas por dia
• Não cobre todos os sorteios
• Requer monitoramento

🎯 RECOMENDADO PARA:
• Contas com muitos tickets
• Sorteios de alto valor
• Uso estratégico focado

⚠️ AVISO: Combina com outros modos!"""
        
        else:
            return
        
        # Criar janela popup
        popup = tk.Toplevel(self.widget)
        popup.title(title)
        popup.geometry("450x400")
        popup.configure(bg="#2C2F33")
        popup.resizable(False, False)
        
        # Centralizar popup
        popup.transient(self.widget.winfo_toplevel())
        popup.grab_set()
        
        # Centralizar na tela
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (450 // 2)
        y = (popup.winfo_screenheight() // 2) - (400 // 2)
        popup.geometry(f"450x400+{x}+{y}")
        
        # Conteúdo do popup
        text_widget = tk.Text(
            popup,
            wrap=tk.WORD,
            bg="#23272A",
            fg="white",
            font=("Arial", 10),
            padx=20,
            pady=20,
            state="disabled"
        )
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Inserir texto
        text_widget.config(state="normal")
        text_widget.insert("1.0", message)
        text_widget.config(state="disabled")
        
        # Botão fechar
        tk.Button(
            popup,
            text="✅ Entendi",
            command=popup.destroy,
            bg="#43B581",
            fg="white",
            font=("Arial", 10, "bold"),
            pady=8,
            cursor="hand2"
        ).pack(pady=10)

class KeyDropGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KeyDrop Bot - Professional Edition")
        self.root.geometry("1000x650")
        self.root.configure(bg="#2C2F33")
        self.root.resizable(True, True)
        
        # Configurar ícone
        self.configurar_icone()
        
        # Centralizar janela
        self.centralizar_janela()
        
        # Variáveis
        self.manager = BotManager()
        self.config = self.manager.carregar_config()
        self.discord_webhook_var = tk.StringVar(value=self.config.get('discord_webhook', ''))
        self.bots_rodando = False
        self.status_labels = []
        self.stats_labels = []
        self.progress_bars = []
        self.update_thread = None
        self.start_time = None
        
        # Variáveis para monitoramento de rede
        self.bytes_sent_prev = 0
        self.bytes_recv_prev = 0
        self.last_net_check = time.time()
        
        # Criar interface
        self.criar_interface()

        # Configurar ícone na bandeja
        self.setup_tray_icon()
        
        # Iniciar update loop
        self.iniciar_update_loop()
    
    def add_hover_effect(self, widget, hover_color, original_color):
        """Adiciona efeito hover aos botões"""
        def on_enter(e):
            widget.config(bg=hover_color)
        
        def on_leave(e):
            widget.config(bg=original_color)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def criar_interface(self):
        """Cria a interface principal"""
        # Título
        titulo_frame = tk.Frame(self.root, bg="#2C2F33")
        titulo_frame.pack(fill="x", pady=10)
        
        titulo = tk.Label(
            titulo_frame,
            text="KeyDrop Bot - Professional Edition",
            font=("Arial", 20, "bold"),
            fg="#FFFFFF",
            bg="#2C2F33"
        )
        titulo.pack()
        
        subtitulo = tk.Label(
            titulo_frame,
            text="Sistema Avançado de Participação em Sorteios - by William Medrado",
            font=("Arial", 10),
            fg="#99AAB5",
            bg="#2C2F33"
        )
        subtitulo.pack()
        
        # Banner informativo
        info_frame = tk.Frame(self.root, bg="#2C2F33")
        info_frame.pack(fill="x", padx=20, pady=(5, 10))
        
        # Faixa informativa
        info_banner = tk.Frame(info_frame, bg="#1E2328", relief="solid", bd=1)
        info_banner.pack(fill="x", pady=5)
        
        info_text = tk.Label(
            info_banner,
            text="💡 DICA: Passe o mouse sobre os elementos para ver dicas | Clique nos modos para ver explicações detalhadas",
            font=("Arial", 9, "italic"),
            fg="#7289DA",
            bg="#1E2328",
            pady=8
        )
        info_text.pack()
        
        # Tooltip para o banner
        ToolTip(info_text, "Interface interativa com tooltips\nClique nos modos para informações completas")
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#2C2F33")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Lado esquerdo - Configurações
        self.criar_painel_config(main_frame)
        
        # Lado direito - Status e estatísticas
        self.criar_painel_status(main_frame)
        
        # Rodapé
        self.criar_rodape()
    
    def criar_painel_config(self, parent):
        """Cria o painel de configurações"""
        config_frame = tk.Frame(parent, bg="#23272A", relief="raised", bd=2)
        config_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Título do painel
        tk.Label(
            config_frame,
            text="⚙️ Configurações",
            font=("Arial", 14, "bold"),
            fg="#FFFFFF",
            bg="#23272A"
        ).pack(pady=10)
        
        # Configurações
        config_content = tk.Frame(config_frame, bg="#23272A")
        config_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Linha 1: Número de janelas + Intervalo entre abas
        linha1_frame = tk.Frame(config_content, bg="#23272A")
        linha1_frame.pack(fill="x", pady=(0, 15))
        
        # Número de janelas
        janelas_label = tk.Label(
            linha1_frame,
            text="Janelas:",
            font=("Arial", 10, "bold"),
            fg="#FFFFFF",
            bg="#23272A"
        )
        janelas_label.pack(side="left")
        
        self.num_bots_var = tk.IntVar(value=self.config.get('num_bots', 2))
        janelas_spinbox = tk.Spinbox(
            linha1_frame,
            from_=1,
            to=200,
            textvariable=self.num_bots_var,
            width=8,
            bg="#2C2F33",
            fg="white",
            buttonbackground="#7289DA",
            cursor="hand2"
        )
        janelas_spinbox.pack(side="left", padx=(5, 20))
        
        # Tooltip para número de janelas
        ToolTip(janelas_label, "Número de janelas do navegador\nMais janelas = mais sorteios")
        ToolTip(janelas_spinbox, "Recomendado: 2-10 para início\nProfissional: 50-200 janelas")
        
        # Separador
        tk.Label(linha1_frame, text="•", font=("Arial", 12), fg="#99AAB5", bg="#23272A").pack(side="left", padx=10)
        
        # Intervalo entre abas (mudança de descrição)
        velocidade_label = tk.Label(
            linha1_frame,
            text="Velocidade de Navegação:",
            font=("Arial", 10, "bold"),
            fg="#FFFFFF",
            bg="#23272A"
        )
        velocidade_label.pack(side="left")
        
        self.intervalo_tabs_var = tk.IntVar(value=self.config.get('intervalo_tabs', 2))
        velocidade_entry = tk.Entry(
            linha1_frame,
            textvariable=self.intervalo_tabs_var,
            width=8,
            bg="#2C2F33",
            fg="white",
            insertbackground="white",
            cursor="hand2"
        )
        velocidade_entry.pack(side="left", padx=(5, 5))
        
        velocidade_desc = tk.Label(
            linha1_frame,
            text="seg (delay entre abas)",
            font=("Arial", 9),
            fg="#99AAB5",
            bg="#23272A"
        )
        velocidade_desc.pack(side="left")
        
        # Tooltips para velocidade
        ToolTip(velocidade_label, "Tempo entre abertura de abas\nMenor = mais rápido")
        ToolTip(velocidade_entry, "Recomendado: 1-3 segundos\nMuito baixo pode causar erros")
        ToolTip(velocidade_desc, "Intervalo fixo: 3min entre sorteios\nCONTENDER: 1 hora entre sorteios")
        
        # Configurar intervalo de sorteios como fixo (não editável)
        self.intervalo_sorteios_var = tk.IntVar(value=180)  # 3 minutos fixo
        # Linha 2: Modos (Headless + Login + CONTENDER)
        linha2_frame = tk.Frame(config_content, bg="#23272A")
        linha2_frame.pack(fill="x", pady=(0, 15))
        
        # Modo headless
        self.headless_var = tk.BooleanVar(value=self.config.get('headless', False))
        headless_check = tk.Checkbutton(
            linha2_frame,
            text="🔳 Headless (Silencioso)",
            variable=self.headless_var,
            bg="#23272A",
            fg="white",
            selectcolor="#2C2F33",
            activebackground="#23272A",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        headless_check.pack(side="left")
        
        # Tooltip para modo headless
        ToolTip(headless_check, "Execução sem interface gráfica\nClique para mais informações")
        
        # Separador
        tk.Label(linha2_frame, text="•", font=("Arial", 12), fg="#99AAB5", bg="#23272A").pack(side="left", padx=10)
        
        # Modo login
        self.login_mode_var = tk.BooleanVar(value=self.config.get('login_mode', False))
        login_check = tk.Checkbutton(
            linha2_frame,
            text="🔐 Login (Manual)",
            variable=self.login_mode_var,
            command=self.on_login_mode_change,
            bg="#23272A",
            fg="white",
            selectcolor="#2C2F33",
            activebackground="#23272A",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        login_check.pack(side="left")
        
        # Tooltip para modo login
        ToolTip(login_check, "Navegador visível para login manual\nClique para mais informações")
        
        # Separador
        tk.Label(linha2_frame, text="•", font=("Arial", 12), fg="#99AAB5", bg="#23272A").pack(side="left", padx=10)
        
        # Modo CONTENDER
        self.contender_mode_var = tk.BooleanVar(value=self.config.get('contender_mode', False))
        contender_check = tk.Checkbutton(
            linha2_frame,
            text="🏆 CONTENDER (1h)",
            variable=self.contender_mode_var,
            bg="#23272A",
            fg="white",
            selectcolor="#2C2F33",
            activebackground="#23272A",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        contender_check.pack(side="left")
        
        # Tooltip para modo CONTENDER
        ToolTip(contender_check, "Sorteios a cada 1 hora (premium)\nClique para mais informações")
        
        # Informações sobre intervalos
        info_intervalos = tk.Frame(config_content, bg="#23272A")
        info_intervalos.pack(fill="x", pady=(8, 0))
        
        tk.Label(
            info_intervalos,
            text="⏱️ Intervalos: AMATEUR (3 min) • CONTENDER (1 hora) • Navegação (configurável)",
            font=("Arial", 9, "italic"),
            fg="#99AAB5",
            bg="#23272A"
        ).pack(anchor="w")
        
        # Webhook Discord
        webhook_frame = tk.Frame(config_content, bg="#23272A")
        webhook_frame.pack(fill="x", pady=(0, 15))
        
        webhook_label = tk.Label(
            webhook_frame,
            text="🔔 Discord Webhook:",
            font=("Arial", 10, "bold"),
            fg="#FFFFFF",
            bg="#23272A"
        )
        webhook_label.pack(anchor="w", pady=(0, 5))
        
        webhook_entry = tk.Entry(
            webhook_frame,
            textvariable=self.discord_webhook_var,
            width=60,
            bg="#2C2F33",
            fg="white",
            insertbackground="white",
            cursor="hand2"
        )
        webhook_entry.pack(fill="x")
        
        # Tooltips para webhook
        ToolTip(webhook_label, "Notificações via Discord\nReceba alertas de vitórias!")
        ToolTip(webhook_entry, "Cole aqui o webhook do Discord\nOpcional - deixe vazio para desativar")
        
        # Botões de controle principais
        botoes_principais_frame = tk.Frame(config_content, bg="#23272A")
        botoes_principais_frame.pack(fill="x", pady=(15, 10))
        
        # Linha 1: Botões principais (Iniciar/Parar) - Tamanho igual
        linha_botoes1 = tk.Frame(botoes_principais_frame, bg="#23272A")
        linha_botoes1.pack(fill="x", pady=(0, 6))
        
        # Configurar grid para botões principais
        linha_botoes1.grid_columnconfigure(0, weight=1)
        linha_botoes1.grid_columnconfigure(1, weight=1)
        
        self.btn_iniciar = tk.Button(
            linha_botoes1,
            text="🚀 INICIAR BOTS",
            command=self.iniciar_bots,
            bg="#43B581",
            fg="white",
            font=("Arial", 12, "bold"),
            pady=14,
            cursor="hand2",
            relief="flat",
            borderwidth=0
        )
        self.btn_iniciar.grid(row=0, column=0, sticky="ew", padx=(0, 3))
        
        self.btn_parar = tk.Button(
            linha_botoes1,
            text="⏹️ PARAR BOTS",
            command=self.parar_bots,
            bg="#F04747",
            fg="white",
            font=("Arial", 12, "bold"),
            pady=14,
            cursor="hand2",
            state="disabled",
            relief="flat",
            borderwidth=0
        )
        self.btn_parar.grid(row=0, column=1, sticky="ew", padx=(3, 0))
        
        # Linha 2: Botões secundários - Tamanho igual
        linha_botoes2 = tk.Frame(botoes_principais_frame, bg="#23272A")
        linha_botoes2.pack(fill="x", pady=(0, 6))
        
        # Configurar grid para botões secundários
        linha_botoes2.grid_columnconfigure(0, weight=1)
        linha_botoes2.grid_columnconfigure(1, weight=1)
        
        self.btn_reiniciar = tk.Button(
            linha_botoes2,
            text="🔄 REINICIAR",
            command=self.reiniciar_guias,
            bg="#FF6B35",
            fg="white",
            font=("Arial", 10, "bold"),
            pady=10,
            cursor="hand2",
            state="disabled",
            relief="flat",
            borderwidth=0
        )
        self.btn_reiniciar.grid(row=0, column=0, sticky="ew", padx=(0, 3))
        
        self.btn_limpar_cache = tk.Button(
            linha_botoes2,
            text="🧹 LIMPAR CACHE",
            command=self.limpar_cache_navegador,
            bg="#9B59B6",
            fg="white",
            font=("Arial", 10, "bold"),
            pady=10,
            cursor="hand2",
            state="disabled",
            relief="flat",
            borderwidth=0
        )
        self.btn_limpar_cache.grid(row=0, column=1, sticky="ew", padx=(3, 0))
        
        # Linha 3: Botões de configuração - Tamanho igual
        linha_botoes3 = tk.Frame(botoes_principais_frame, bg="#23272A")
        linha_botoes3.pack(fill="x")
        
        # Configurar grid para botões de configuração
        linha_botoes3.grid_columnconfigure(0, weight=1)
        linha_botoes3.grid_columnconfigure(1, weight=1)
        
        self.btn_salvar = tk.Button(
            linha_botoes3,
            text="💾 SALVAR CONFIG",
            command=self.salvar_config,
            bg="#7289DA",
            fg="white",
            font=("Arial", 9, "bold"),
            pady=8,
            cursor="hand2",
            relief="flat",
            borderwidth=0
        )
        self.btn_salvar.grid(row=0, column=0, sticky="ew", padx=(0, 3))
        
        btn_startup = tk.Button(
            linha_botoes3,
            text="🚀 STARTUP",
            command=self.configurar_startup,
            bg="#FAA61A",
            fg="white",
            font=("Arial", 9, "bold"),
            pady=8,
            cursor="hand2",
            relief="flat",
            borderwidth=0
        )
        btn_startup.grid(row=0, column=1, sticky="ew", padx=(3, 0))
        
        # Tooltips para os botões
        ToolTip(self.btn_iniciar, "Inicia todos os bots configurados\nClique para começar")
        ToolTip(self.btn_parar, "Para todos os bots em execução\nClique para parar")
        ToolTip(self.btn_reiniciar, "Reinicia as guias do navegador\nÚtil para resolver problemas")
        ToolTip(self.btn_limpar_cache, "Limpa cache do navegador\nMelhora performance")
        ToolTip(self.btn_salvar, "Salva configurações atuais\nAutomático ao iniciar")
        ToolTip(btn_startup, "Configura inicialização automática\nInicia com o Windows")
        
        # Efeitos hover para os botões
        self.add_hover_effect(self.btn_iniciar, "#3CA374", "#43B581")
        self.add_hover_effect(self.btn_parar, "#D9403A", "#F04747")
        self.add_hover_effect(self.btn_reiniciar, "#E65A28", "#FF6B35")
        self.add_hover_effect(self.btn_limpar_cache, "#8B4A9C", "#9B59B6")
        self.add_hover_effect(self.btn_salvar, "#5E7DD3", "#7289DA")
        self.add_hover_effect(btn_startup, "#E19710", "#FAA61A")
        
        # Espaçamento final
        tk.Frame(config_content, bg="#23272A", height=20).pack()
    
    def criar_painel_status(self, parent):
        """Cria o painel de status"""
        status_frame = tk.Frame(parent, bg="#23272A", relief="raised", bd=2)
        status_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Título
        tk.Label(
            status_frame,
            text="📊 Status dos Bots",
            font=("Arial", 14, "bold"),
            fg="#FFFFFF",
            bg="#23272A"
        ).pack(pady=10)
        
        # Área de scroll para status
        self.criar_area_scroll(status_frame)
    
    def criar_area_scroll(self, parent):
        """Cria área com scroll para status"""
        # Canvas e scrollbar
        canvas = tk.Canvas(parent, bg="#23272A", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        
        self.status_content = tk.Frame(canvas, bg="#23272A")
        
        # Configurar scroll
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.create_window((0, 0), window=self.status_content, anchor="nw")
        
        # Pack
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Atualizar scroll region
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        self.status_content.bind("<Configure>", configure_scroll)
    
    def criar_rodape(self):
        """Cria o rodapé com informações de performance"""
        rodape = tk.Frame(self.root, bg="#23272A", height=120)
        rodape.pack(fill="x", side="bottom")
        
        # Título do painel de performance
        tk.Label(
            rodape,
            text="📊 Performance do Sistema",
            font=("Arial", 11, "bold"),
            fg="#FFFFFF",
            bg="#23272A"
        ).pack(pady=(5, 0))
        
        # Frame para métricas de performance
        perf_frame = tk.Frame(rodape, bg="#23272A")
        perf_frame.pack(fill="x", pady=(5, 5))
        
        # Linha 1: CPU e RAM
        linha1_perf = tk.Frame(perf_frame, bg="#23272A")
        linha1_perf.pack(fill="x", padx=20, pady=2)
        
        # CPU
        cpu_container = tk.Frame(linha1_perf, bg="#2C2F33", relief="raised", bd=1)
        cpu_container.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Label(
            cpu_container,
            text="🖥️ CPU:",
            font=("Arial", 9, "bold"),
            fg="#FFFFFF",
            bg="#2C2F33"
        ).pack(side="left", padx=5)
        
        self.cpu_label = tk.Label(
            cpu_container,
            text="0%",
            font=("Arial", 9, "bold"),
            fg="#43B581",
            bg="#2C2F33"
        )
        self.cpu_label.pack(side="right", padx=5)
        
        # RAM
        ram_container = tk.Frame(linha1_perf, bg="#2C2F33", relief="raised", bd=1)
        ram_container.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        tk.Label(
            ram_container,
            text="🧠 RAM:",
            font=("Arial", 9, "bold"),
            fg="#FFFFFF",
            bg="#2C2F33"
        ).pack(side="left", padx=5)
        
        self.ram_label = tk.Label(
            ram_container,
            text="0%",
            font=("Arial", 9, "bold"),
            fg="#7289DA",
            bg="#2C2F33"
        )
        self.ram_label.pack(side="right", padx=5)
        
        # Linha 2: Disco e Rede
        linha2_perf = tk.Frame(perf_frame, bg="#23272A")
        linha2_perf.pack(fill="x", padx=20, pady=2)
        
        # Disco
        disco_container = tk.Frame(linha2_perf, bg="#2C2F33", relief="raised", bd=1)
        disco_container.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Label(
            disco_container,
            text="💾 HD:",
            font=("Arial", 9, "bold"),
            fg="#FFFFFF",
            bg="#2C2F33"
        ).pack(side="left", padx=5)
        
        self.disco_label = tk.Label(
            disco_container,
            text="0%",
            font=("Arial", 9, "bold"),
            fg="#FAA61A",
            bg="#2C2F33"
        )
        self.disco_label.pack(side="right", padx=5)
        
        # Rede
        rede_container = tk.Frame(linha2_perf, bg="#2C2F33", relief="raised", bd=1)
        rede_container.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        tk.Label(
            rede_container,
            text="🌐 Rede:",
            font=("Arial", 9, "bold"),
            fg="#FFFFFF",
            bg="#2C2F33"
        ).pack(side="left", padx=5)
        
        self.rede_label = tk.Label(
            rede_container,
            text="0 KB/s",
            font=("Arial", 9, "bold"),
            fg="#9B59B6",
            bg="#2C2F33"
        )
        self.rede_label.pack(side="right", padx=5)
        
        # Créditos
        tk.Label(
            rodape,
            text="KeyDrop Bot v2.0 - Desenvolvido por William Medrado para uso profissional 24/7",
            font=("Arial", 8),
            fg="#99AAB5",
            bg="#23272A"
        ).pack(pady=(5, 5))
    
    def iniciar_bots(self):
        """Inicia todos os bots"""
        try:
            # Feedback visual
            self.btn_iniciar.config(text="⏳ INICIANDO...", state="disabled")
            self.root.update_idletasks()

            # Validar configurações
            if self.num_bots_var.get() < 1 or self.num_bots_var.get() > 200:
                messagebox.showerror("Erro", "Número de bots deve estar entre 1 e 200")
                self.btn_iniciar.config(text="🚀 INICIAR BOTS", state="normal")
                return
            
            if self.num_bots_var.get() > 50:
                response = messagebox.askyesno(
                    "Confirmação",
                    f"Você está iniciando {self.num_bots_var.get()} bots.\n\n"
                    "Isso pode consumir muitos recursos do sistema.\n"
                    "Recomenda-se uso em modo headless para performance.\n\n"
                    "Deseja continuar?"
                )
                if not response:
                    self.btn_iniciar.config(text="🚀 INICIAR BOTS", state="normal")
                    return
            
            if self.intervalo_sorteios_var.get() < 10:
                messagebox.showerror("Erro", "Intervalo entre sorteios deve ser no mínimo 10 segundos")
                self.btn_iniciar.config(text="🚀 INICIAR BOTS", state="normal")
                return
            
            # Salvar configurações
            self.salvar_config()
            
            # Criar bots
            self.manager.criar_bots(
                self.num_bots_var.get(), 
                self.headless_var.get(),
                self.discord_webhook_var.get().strip() or None,
                self.login_mode_var.get(),
                self.contender_mode_var.get()
            )
            
            # Atualizar interface
            self.btn_iniciar.config(state="disabled")
            self.btn_parar.config(state="normal")
            self.btn_reiniciar.config(state="normal")
            self.btn_limpar_cache.config(state="normal")
            self.bots_rodando = True
            self.start_time = time.time()  # Marcar tempo de início
            
            # Limpar status anterior
            for widget in self.status_content.winfo_children():
                widget.destroy()
            self.status_labels = []
            self.stats_labels = []
            self.progress_bars = []
            
            # Criar labels de status
            self.criar_labels_status()
            
            # Iniciar bots em thread separada
            threading.Thread(
                target=self.manager.iniciar_todos,
                args=(self.intervalo_sorteios_var.get(),),
                daemon=True
            ).start()

            self.btn_iniciar.config(text="🚀 INICIAR BOTS")
            
            messagebox.showinfo(
                "Sucesso",
                f"Iniciando {self.num_bots_var.get()} bots!\n\n"
                f"Modo headless: {'Ativado' if self.headless_var.get() else 'Desativado'}\n"
                f"Modo login: {'Ativado' if self.login_mode_var.get() else 'Desativado'}\n"
                f"Modo CONTENDER: {'Ativado' if self.contender_mode_var.get() else 'Desativado'}\n"
                f"Discord webhook: {'Configurado' if self.discord_webhook_var.get().strip() else 'Não configurado'}\n\n"
                f"{'🔐 Modo Login: Faça login em cada janela e depois desmarque a opção' if self.login_mode_var.get() else '🚀 Bots começarão automaticamente'}\n\n"
                "✅ Notificação de início enviada para o Discord (se configurado)!"
            )
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar bots: {str(e)}")
            self.btn_iniciar.config(text="🚀 INICIAR BOTS", state="normal")
    
    def parar_bots(self):
        """Para todos os bots"""
        try:
            self.bots_rodando = False
            self.manager.parar_todos()
            
            self.btn_iniciar.config(state="normal")
            self.btn_parar.config(state="disabled")
            self.btn_reiniciar.config(state="disabled")
            self.btn_limpar_cache.config(state="disabled")
            
            # Atualizar status
            for i, label in enumerate(self.status_labels):
                label.config(text=f"Bot {i+1}: ⏹️ Parado", fg="#F04747")

            for bar in self.progress_bars:
                bar['value'] = 0
            
            messagebox.showinfo("Sucesso", "Todos os bots foram parados!\n\n✅ Notificação de parada enviada para o Discord (se configurado)!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao parar bots: {str(e)}")
    
    def salvar_config(self):
        """Salva as configurações"""
        try:
            # Feedback visual
            if hasattr(self, 'btn_salvar'):
                self.btn_salvar.config(text="💾 Salvando...", state="disabled")
                self.root.update_idletasks()

            config = {
                'num_bots': self.num_bots_var.get(),
                'intervalo_sorteios': self.intervalo_sorteios_var.get(),
                'intervalo_tabs': self.intervalo_tabs_var.get(),
                'headless': self.headless_var.get(),
                'login_mode': self.login_mode_var.get(),
                'contender_mode': self.contender_mode_var.get(),
                'discord_webhook': self.discord_webhook_var.get().strip()
            }
            self.manager.salvar_config(config)
            self.config = config
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")
        finally:
            if hasattr(self, 'btn_salvar'):
                self.btn_salvar.config(text="💾 SALVAR CONFIG", state="normal")
    
    def criar_labels_status(self):
        """Cria labels para mostrar status dos bots"""
        for i in range(self.num_bots_var.get()):
            # Frame para cada bot
            bot_frame = tk.Frame(self.status_content, bg="#2C2F33", relief="raised", bd=1)
            bot_frame.pack(fill="x", pady=5, padx=10)
            
            # Status do bot
            status_label = tk.Label(
                bot_frame,
                text=f"Bot {i+1}: 🔄 Inicializando...",
                font=("Arial", 10, "bold"),
                fg="#FFFFFF",
                bg="#2C2F33"
            )
            status_label.pack(anchor="w", padx=10, pady=5)
            self.status_labels.append(status_label)
            
            # Frame para estatísticas e saldo
            stats_frame = tk.Frame(bot_frame, bg="#2C2F33")
            stats_frame.pack(fill="x", padx=10, pady=(0, 5))
            
            # Estatísticas
            stats_label = tk.Label(
                stats_frame,
                text="AMATEUR: 0 | CONTENDER: 0 | Erros: 0 | Tempo: 00:00:00",
                font=("Arial", 9),
                fg="#99AAB5",
                bg="#2C2F33"
            )
            stats_label.pack(side="left")
            self.stats_labels.append(stats_label)

            # Saldo (lado direito)
            saldo_label = tk.Label(
                stats_frame,
                text="R$ 0,00",
                font=("Arial", 9, "bold"),
                fg="#43B581",
                bg="#2C2F33"
            )
            saldo_label.pack(side="right")
            self.stats_labels.append(saldo_label)  # Usar mesma lista para simplificar

            # Barra de progresso
            progress = ttk.Progressbar(
                bot_frame,
                maximum=self.intervalo_sorteios_var.get(),
                length=200
            )
            progress.pack(fill="x", padx=10, pady=(0, 5))
            self.progress_bars.append(progress)
            ToolTip(progress, "Tempo restante para próximo ciclo")
    
    def iniciar_update_loop(self):
        """Inicia o loop de atualização de status"""
        self.update_thread = threading.Thread(target=self.atualizar_status_loop, daemon=True)
        self.update_thread.start()
    
    def atualizar_status_loop(self):
        """Loop para atualizar status dos bots e performance do sistema"""
        while True:
            try:
                # Atualizar informações de performance
                self.atualizar_performance()
                
                if self.bots_rodando and hasattr(self.manager, 'bots'):
                    stats = self.manager.obter_stats_todos()
                    
                    for i, stat in enumerate(stats):
                        if i < len(self.status_labels):
                            bot_id = stat['bot_id']
                            bot_stats = stat['stats']
                            ativo = stat['ativo']
                            
                            # Atualizar status
                            if ativo:
                                status_text = f"Bot {bot_id}: 🟢 Ativo"
                                cor = "#43B581"
                            else:
                                status_text = f"Bot {bot_id}: 🔴 Inativo"
                                cor = "#F04747"
                            
                            self.status_labels[i].config(text=status_text, fg=cor)
                            
                            # Calcular tempo de execução
                            tempo_exec = "00:00:00"
                            if bot_stats['inicio']:
                                delta = datetime.now() - bot_stats['inicio']
                                horas = delta.seconds // 3600
                                minutos = (delta.seconds % 3600) // 60
                                segundos = delta.seconds % 60
                                tempo_exec = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
                            
                            # Atualizar estatísticas
                            normal = bot_stats['participacoes']
                            contender = bot_stats.get('participacoes_contender', 0)
                            stats_text = f"AMATEUR: {normal} | CONTENDER: {contender} | Erros: {bot_stats['erros']} | Tempo: {tempo_exec}"
                            
                            # Atualizar saldo (se disponível)
                            saldo = bot_stats.get('saldo_skins', 'R$ 0,00')

                            # Verificar se temos label de saldo (cada bot tem 2 labels no stats_labels)
                            if (i * 2 + 1) < len(self.stats_labels):
                                self.stats_labels[i * 2].config(text=stats_text)
                                self.stats_labels[i * 2 + 1].config(text=saldo)
                            else:
                                # Fallback se não tiver label de saldo
                                if i < len(self.stats_labels):
                                    self.stats_labels[i].config(text=f"{stats_text} | {saldo}")

                            # Atualizar progress bar
                            if i < len(self.progress_bars):
                                total = bot_stats.get('intervalo_total', self.intervalo_sorteios_var.get())
                                progresso = bot_stats.get('progresso_intervalo', 0)
                                self.progress_bars[i].config(maximum=total)
                                self.progress_bars[i]['value'] = progresso
                
                time.sleep(2)  # Atualiza a cada 2 segundos
                
            except Exception as e:
                print(f"Erro no update loop: {e}")
                time.sleep(5)
    
    def atualizar_performance(self):
        """Atualiza informações de performance do sistema"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=None)
            self.cpu_label.config(text=f"{cpu_percent:.1f}%")
            
            # Cor do CPU baseada no uso
            if cpu_percent < 50:
                self.cpu_label.config(fg="#43B581")  # Verde
            elif cpu_percent < 80:
                self.cpu_label.config(fg="#FAA61A")  # Amarelo
            else:
                self.cpu_label.config(fg="#F04747")  # Vermelho
            
            # RAM
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            ram_used = ram.used / (1024**3)  # GB
            ram_total = ram.total / (1024**3)  # GB
            
            self.ram_label.config(text=f"{ram_percent:.1f}% ({ram_used:.1f}GB/{ram_total:.1f}GB)")
            
            # Cor da RAM baseada no uso
            if ram_percent < 60:
                self.ram_label.config(fg="#7289DA")  # Azul
            elif ram_percent < 80:
                self.ram_label.config(fg="#FAA61A")  # Amarelo
            else:
                self.ram_label.config(fg="#F04747")  # Vermelho
                
            # Disco
            try:
                # Usar volume C: no Windows e raiz do sistema nos demais
                volume = 'C:' if os.name == 'nt' else '/'
                disk = psutil.disk_usage(volume)
            except Exception:
                disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_used = disk.used / (1024**3)  # GB
            disk_total = disk.total / (1024**3)  # GB
            
            self.disco_label.config(text=f"{disk_percent:.1f}% ({disk_used:.0f}GB/{disk_total:.0f}GB)")
            
            # Cor do disco baseada no uso
            if disk_percent < 70:
                self.disco_label.config(fg="#FAA61A")  # Amarelo
            elif disk_percent < 90:
                self.disco_label.config(fg="#FF6B35")  # Laranja
            else:
                self.disco_label.config(fg="#F04747")  # Vermelho
                
            # Rede
            net = psutil.net_io_counters()
            current_time = time.time()
            
            # Calcular velocidade de rede
            if hasattr(self, 'last_net_check'):
                time_diff = current_time - self.last_net_check
                if time_diff > 0:
                    bytes_sent_diff = net.bytes_sent - self.bytes_sent_prev
                    bytes_recv_diff = net.bytes_recv - self.bytes_recv_prev
                    
                    # Velocidade total (upload + download) em KB/s
                    speed_kbps = (bytes_sent_diff + bytes_recv_diff) / time_diff / 1024
                    
                    # Formatar velocidade
                    if speed_kbps < 1024:
                        speed_text = f"{speed_kbps:.0f} KB/s"
                    else:
                        speed_text = f"{speed_kbps/1024:.1f} MB/s"
                    
                    self.rede_label.config(text=speed_text)
                    
                    # Cor da rede baseada na velocidade
                    if speed_kbps < 100:
                        self.rede_label.config(fg="#9B59B6")  # Roxo
                    elif speed_kbps < 1000:
                        self.rede_label.config(fg="#43B581")  # Verde
                    else:
                        self.rede_label.config(fg="#FAA61A")  # Amarelo
            
            # Atualizar valores anteriores
            self.bytes_sent_prev = net.bytes_sent
            self.bytes_recv_prev = net.bytes_recv
            self.last_net_check = current_time
                
        except Exception as e:
            print(f"Erro ao atualizar performance: {e}")
    
    def reiniciar_guias(self):
        """Reinicia todas as guias dos bots"""
        if not self.bots_rodando:
            messagebox.showwarning("Aviso", "Nenhum bot está rodando!")
            return
        
        try:
            # Mostrar confirmação
            response = messagebox.askyesno(
                "Confirmação",
                "Isso irá reiniciar todas as guias dos bots.\n\n"
                "Os bots serão pausados momentaneamente durante o processo.\n\n"
                "Deseja continuar?"
            )
            
            if not response:
                return
            
            # Desabilitar botão temporariamente
            self.btn_reiniciar.config(state="disabled", text="🔄 Reiniciando...")
            
            # Executar reinicialização em thread separada
            threading.Thread(
                target=self._executar_reinicializacao,
                daemon=True
            ).start()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao reiniciar guias: {str(e)}")
    
    def _executar_reinicializacao(self):
        """Executa o processo de reinicialização"""
        try:
            # Reiniciar bots
            self.manager.reiniciar_guias()
            
            # Atualizar interface
            self.root.after(0, self._finalizar_reinicializacao)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro durante reinicialização: {str(e)}"))
            self.root.after(0, self._finalizar_reinicializacao)
    
    def _finalizar_reinicializacao(self):
        """Finaliza o processo de reinicialização"""
        self.btn_reiniciar.config(state="normal", text="🔄 Reiniciar Guias")
        messagebox.showinfo("Sucesso", "Guias reiniciadas com sucesso!")
    
    def configurar_startup(self):
        """Configura inicialização automática"""
        try:
            from startup_config import verificar_startup_ativo, ativar_inicializacao_automatica, desativar_inicializacao_automatica
            
            ativo = verificar_startup_ativo()
            
            if ativo:
                response = messagebox.askyesno(
                    "Inicialização Automática",
                    "A inicialização automática está ATIVA.\n\n"
                    "Deseja desativar?"
                )
                
                if response:
                    desativar_inicializacao_automatica()
                    messagebox.showinfo("Sucesso", "Inicialização automática desativada!")
                
            else:
                response = messagebox.askyesno(
                    "Inicialização Automática",
                    "A inicialização automática está INATIVA.\n\n"
                    "Deseja ativar?\n\n"
                    "O bot será iniciado automaticamente quando o Windows iniciar."
                )
                
                if response:
                    if ativar_inicializacao_automatica():
                        messagebox.showinfo("Sucesso", "Inicialização automática ativada!")
                    else:
                        messagebox.showerror("Erro", "Falha ao ativar inicialização automática!")
                        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao configurar startup: {str(e)}")
    
    def on_login_mode_change(self):
        """Callback quando modo login é alterado"""
        if self.login_mode_var.get():
            # Se modo login foi ativado, desmarcar headless
            self.headless_var.set(False)
            # Mostrar aviso
            messagebox.showinfo(
                "Modo Login Ativado",
                "Modo headless foi desativado automaticamente.\n\n"
                "O modo login precisa que as janelas sejam visíveis\n"
                "para que você possa fazer login."
            )
    
    def run(self):
        """Inicia a interface"""
        self.root.mainloop()

    def limpar_cache_navegador(self):
        """Limpa cache do navegador de todos os bots"""
        if not self.bots_rodando:
            messagebox.showwarning("Aviso", "Nenhum bot está rodando!")
            return
        
        try:
            # Mostrar confirmação
            response = messagebox.askyesno(
                "Confirmação",
                "Isso irá limpar o cache do navegador de todos os bots.\n\n"
                "⚠️ IMPORTANTE: Seus logins da Steam e KeyDrop serão preservados!\n\n"
                "Esta ação irá:\n"
                "• Limpar cache temporário\n"
                "• Remover dados desnecessários\n"
                "• Melhorar a performance\n"
                "• Manter sessões de login\n\n"
                "Deseja continuar?"
            )
            
            if not response:
                return
            
            # Desabilitar botão temporariamente
            self.btn_limpar_cache.config(state="disabled", text="🧹 Limpando...")
            
            # Executar limpeza em thread separada
            threading.Thread(
                target=self._executar_limpeza_cache,
                daemon=True
            ).start()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao limpar cache: {str(e)}")
    
    def _executar_limpeza_cache(self):
        """Executa o processo de limpeza de cache"""
        try:
            # Limpar cache de todos os bots
            sucesso, falhas = self.manager.limpar_cache_todos_bots()
            
            # Atualizar interface
            self.root.after(0, lambda: self._finalizar_limpeza_cache(sucesso, falhas))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro durante limpeza: {str(e)}"))
            self.root.after(0, lambda: self._finalizar_limpeza_cache(0, 0))
    
    def _finalizar_limpeza_cache(self, sucesso, falhas):
        """Finaliza o processo de limpeza de cache"""
        try:
            # Reabilitar botão
            self.btn_limpar_cache.config(state="normal", text="🧹 Limpar Cache do Navegador")
            
            # Mostrar resultado
            if sucesso > 0:
                messagebox.showinfo(
                    "Limpeza Concluída",
                    f"Cache limpo com sucesso!\n\n"
                    f"✅ Sucessos: {sucesso}\n"
                    f"❌ Falhas: {falhas}\n\n"
                    f"Os bots devem estar mais rápidos agora!"
                )
            else:
                messagebox.showwarning(
                    "Limpeza Falhou",
                    f"Não foi possível limpar o cache.\n\n"
                    f"❌ Falhas: {falhas}\n\n"
                    f"Verifique se os bots estão funcionando corretamente."
                )
                
        except Exception as e:
            print(f"Erro ao finalizar limpeza: {e}")
    
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

    def setup_tray_icon(self):
        """Configura o ícone da bandeja do sistema"""
        if not PYSTRAY_AVAILABLE:
            return
        try:
            from pystray import Icon, Menu, MenuItem
            from PIL import Image

            # Carregar imagem do ícone
            icon_path = None
            for caminho in [
                os.path.join(os.path.dirname(__file__), 'bot-icone.png'),
                os.path.join(os.path.dirname(__file__), 'bot-icone.ico'),
                os.path.join(os.getcwd(), 'bot-icone.png'),
                os.path.join(os.getcwd(), 'bot-icone.ico'),
            ]:
                if os.path.exists(caminho):
                    icon_path = caminho
                    break

            if icon_path:
                image = Image.open(icon_path)
            else:
                image = Image.new('RGB', (64, 64), color=(0, 0, 0))

            menu = Menu(
                MenuItem('Mostrar', self.show_window),
                MenuItem('Sair', self.exit_app)
            )

            self.tray_icon = Icon('KeyDropBot', image, 'KeyDrop Bot', menu)
            threading.Thread(target=self.tray_icon.run, daemon=True).start()

            # Minimizar para bandeja ao fechar
            self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        except Exception as e:
            print(f"⚠️ Falha ao iniciar ícone de bandeja: {e}")

    def show_window(self, *args):
        """Exibe a janela principal"""
        self.root.after(0, self.root.deiconify)

    def hide_window(self, *args):
        """Esconde a janela na bandeja"""
        self.root.withdraw()

    def exit_app(self, *args):
        """Fecha aplicação e ícone da bandeja"""
        try:
            if hasattr(self, 'tray_icon') and self.tray_icon:
                self.tray_icon.stop()
        except Exception:
            pass
        self.root.destroy()
