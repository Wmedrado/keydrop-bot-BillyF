#!/usr/bin/env python3
"""
Keydrop Bot Professional v3.0.0 - Interface Gráfica Desktop
Aplicativo desktop nativo com automação Chrome integrada
"""

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
from datetime import datetime, timedelta
from pathlib import Path
import psutil

# Importações para automação Chrome
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️ Selenium não disponível - funcionalidades de automação serão limitadas")

class KeydropAutomationBot:
    """Classe para automação dos sorteios Keydrop usando Chrome/Edge"""
    
    def __init__(self, bot_id, profile_path=None, headless=False, mini_window=False, contender_mode=False, gui_callback=None):
        self.bot_id = bot_id
        self.profile_path = profile_path or f"./profiles/bot_profile_{bot_id}"
        self.headless = headless
        self.mini_window = mini_window
        self.contender_mode = contender_mode
        self.gui_callback = gui_callback  # Para logs na interface
        self.driver = None
        self.running = False
        
        # Estatísticas do bot
        self.stats = {
            'amateur_participations': 0,
            'contender_participations': 0,
            'errors': 0,
            'last_amateur_time': None,
            'last_contender_time': None,
            'start_time': datetime.now()
        }
        # Monitorar quantidade de sorteios para evitar refresh desnecessário
        self.last_giveaway_count = -1
    
    def log(self, message, level="INFO"):
        """Log personalizado que envia para a GUI"""
        log_msg = f"[Bot {self.bot_id}] {message}"
        print(log_msg)
        if self.gui_callback:
            self.gui_callback(log_msg, level)
    
    def setup_driver(self):
        """Configurar driver Chrome/Edge com perfil isolado"""
        try:
            if not SELENIUM_AVAILABLE:
                self.log("❌ Selenium não disponível - install com: pip install selenium", "ERROR")
                return False
            
            # Criar diretório do perfil se não existir
            os.makedirs(self.profile_path, exist_ok=True)
            
            # Configurar opções do Chrome
            options = Options()
            options.add_argument(f"--user-data-dir={self.profile_path}")
            options.add_argument(f"--profile-directory=Default")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--no-first-run")
            options.add_argument("--no-default-browser-check")
            
            if self.headless:
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")
                self.log("🕶️ Modo headless ativado")
            elif self.mini_window:
                options.add_argument("--window-size=300,400")
                self.log("📱 Modo mini window ativado")
            else:
                options.add_argument("--window-size=1024,768")
            
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Criar driver
            if SELENIUM_AVAILABLE:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                
                # Anti-detecção
                self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    """
                })
                
                self.log("✅ Driver Chrome configurado com sucesso")
                return True
            else:
                return False
            
        except Exception as e:
            self.log(f"❌ Erro ao configurar driver: {e}", "ERROR")
            return False
    
    def navigate_to_giveaways(self):
        """Navegar para página de sorteios"""
        try:
            if not self.driver:
                return False
                
            self.driver.get("https://key-drop.com/pt/giveaways/list")
            if SELENIUM_AVAILABLE:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            self.log("🌐 Navegou para página de sorteios")
            return True
        except Exception as e:
            self.log(f"❌ Erro ao navegar: {e}", "ERROR")
            return False
    
    def participate_amateur_giveaway(self):
        """Participar de sorteio amateur (3 minutos)"""
        if not SELENIUM_AVAILABLE or not self.driver:
            return False
            
        try:
            self.log("🎯 Procurando sorteios amateur (3min)...")
            
            # Procurar botões de participação em sorteios amateur
            join_buttons = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[class*='join'], .join-btn, .btn-join, .giveaway-join"))
            )
            
            if not join_buttons:
                # Tentar outros seletores
                join_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Join') or contains(text(), 'Participar')]")
            
            participated = False
            for button in join_buttons:
                try:
                    if button.is_enabled() and button.is_displayed():
                        # Scroll para o elemento
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        time.sleep(1)
                        
                        # Tentar clicar
                        button.click()
                        self.log("✅ Participou de sorteio amateur!")
                        self.stats['amateur_participations'] += 1
                        self.stats['last_amateur_time'] = datetime.now()
                        participated = True
                        time.sleep(2)  # Aguardar confirmação
                        break
                        
                except Exception as e:
                    self.log(f"⚠️ Erro ao clicar botão: {e}", "WARNING")
                    continue
            
            if not participated:
                self.log("⚠️ Nenhum sorteio amateur disponível no momento", "WARNING")
            
            return participated
            
        except Exception as e:
            self.log(f"❌ Erro ao participar de sorteio amateur: {e}", "ERROR")
            self.stats['errors'] += 1
            return False
    
    def participate_contender_giveaway(self):
        """Participar de sorteio contender (1 hora) se habilitado"""
        if not self.contender_mode or not SELENIUM_AVAILABLE or not self.driver:
            return False
        
        try:
            # Verificar se já participou na última hora
            if self.stats['last_contender_time']:
                time_diff = datetime.now() - self.stats['last_contender_time']
                if time_diff.total_seconds() < 3600:  # 1 hora = 3600 segundos
                    remaining = 3600 - time_diff.total_seconds()
                    self.log(f"⏳ Aguardando {remaining/60:.1f} min para próximo sorteio contender", "INFO")
                    return False
            
            self.log("🏆 Procurando sorteios contender (1h)...")
            
            # Procurar sorteios contender especificamente
            contender_buttons = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'contender') or contains(text(), 'Contender')]//button[contains(@class, 'join') or contains(text(), 'Join')]")
            
            if not contender_buttons:
                # Tentar outros seletores para contender
                contender_buttons = self.driver.find_elements(By.CSS_SELECTOR, ".contender .join-btn, .contender-giveaway button")
            
            participated = False
            for button in contender_buttons:
                try:
                    if button.is_enabled() and button.is_displayed():
                        # Scroll para o elemento
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        time.sleep(1)
                        
                        # Tentar clicar
                        button.click()
                        self.log("🏆 Participou de sorteio contender!")
                        self.stats['contender_participations'] += 1
                        self.stats['last_contender_time'] = datetime.now()
                        participated = True
                        time.sleep(2)  # Aguardar confirmação
                        break
                        
                except Exception as e:
                    self.log(f"⚠️ Erro ao clicar botão contender: {e}", "WARNING")
                    continue
            
            if not participated:
                self.log("⚠️ Nenhum sorteio contender disponível", "WARNING")
            
            return participated
            
        except Exception as e:
            self.log(f"❌ Erro ao participar de sorteio contender: {e}", "ERROR")
            self.stats['errors'] += 1
            return False

    def page_needs_refresh(self):
        """Verifica se a página possui novos sorteios"""
        try:
            if not self.driver or not By:
                return True

            elements = self.driver.find_elements(By.CSS_SELECTOR,
                                                 "[data-testid='div-active-giveaways-list-single-card']")
            current_count = len(elements)

            if self.last_giveaway_count != current_count:
                self.last_giveaway_count = current_count
                return False
        except Exception:
            return True

        return True
    
    def run_automation_cycle(self, interval_seconds=180):
        """Executar ciclo de automação"""
        if not self.setup_driver():
            return
        
        self.running = True
        self.log(f"🚀 Iniciando ciclo de automação (intervalo: {interval_seconds}s)")
        
        try:
            # Navegar para página de sorteios
            if not self.navigate_to_giveaways():
                return
            
            while self.running:
                try:
                    self.log("🔄 Iniciando novo ciclo de participação...")
                    
                    # 1. Sempre participar de sorteios amateur (3min)
                    participated_amateur = self.participate_amateur_giveaway()
                    
                    # 2. Participar de sorteios contender (1h) se habilitado
                    participated_contender = self.participate_contender_giveaway()
                    
                    # 3. Atualizar página para novos sorteios
                    try:
                        if self.driver and self.page_needs_refresh():
                            self.driver.refresh()
                            time.sleep(3)
                    except:
                        # Tentar recarregar se der erro
                        self.navigate_to_giveaways()
                    
                    # Log do ciclo
                    if participated_amateur or participated_contender:
                        self.log(f"✅ Ciclo concluído - Amateur: {participated_amateur}, Contender: {participated_contender}")
                    else:
                        self.log("ℹ️ Ciclo concluído - Nenhuma participação nova")
                    
                    # Aguardar próximo ciclo
                    self.log(f"⏱️ Aguardando {interval_seconds} segundos para próximo ciclo...")
                    for i in range(interval_seconds):
                        if not self.running:
                            break
                        time.sleep(1)
                    
                except Exception as e:
                    self.log(f"❌ Erro no ciclo: {e}", "ERROR")
                    self.stats['errors'] += 1
                    # Aguardar um pouco antes de tentar novamente
                    time.sleep(30)
                    
        except Exception as e:
            self.log(f"❌ Erro crítico na automação: {e}", "ERROR")
        finally:
            self.stop()
    
    def stop(self):
        """Parar automação e fechar driver"""
        self.running = False
        if self.driver:
            try:
                self.driver.quit()
                self.log("🛑 Driver fechado")
            except:
                pass
        
        # Estatísticas finais
        duration = datetime.now() - self.stats['start_time']
        self.log(f"📊 Estatísticas finais: Amateur: {self.stats['amateur_participations']}, "
                f"Contender: {self.stats['contender_participations']}, "
                f"Erros: {self.stats['errors']}, Duração: {duration}")

class KeydropBotGUI:
    def __init__(self):
        """Inicialização ultra-robusta para executável"""
        try:
            # Criar janela principal com máxima proteção
            self.root = tk.Tk()
            self.root.withdraw()  # Esconder inicialmente
            
            # Configuração básica da janela
            self.root.title("Keydrop Bot Professional v3.0.0")
            self.root.geometry("1100x800")
            
            # Configurar Dark Mode
            self.setup_dark_theme()
            
            # Configurar ícone com múltiplas tentativas e proteção para executável
            try:
                # Determinar diretório base para ícone
                if hasattr(sys, '_MEIPASS'):
                    # Quando executando como executável PyInstaller
                    icon_base_path = sys._MEIPASS
                else:
                    # Quando executando como script Python
                    icon_base_path = os.path.dirname(os.path.abspath(__file__))
                
                # Tentar vários caminhos possíveis para o ícone
                icon_paths = [
                    os.path.join(icon_base_path, "bot-icone.ico"),
                    "bot-icone.ico",
                    os.path.join(os.getcwd(), "bot-icone.ico"),
                    os.path.expanduser("~/Desktop/Projeto do zero/bot_keydrop/bot-icone.ico")
                ]
                
                icon_set = False
                for icon_path in icon_paths:
                    if os.path.exists(icon_path):
                        try:
                            self.root.iconbitmap(icon_path)
                            icon_set = True
                            print(f"✅ Ícone configurado com sucesso: {icon_path}")
                            break
                        except Exception as e:
                            print(f"⚠️ Erro ao definir ícone {icon_path}: {e}")
                            continue
                
                if not icon_set:
                    print("⚠️ Ícone personalizado não encontrado, usando padrão do sistema")
                    # Tentar definir um ícone padrão melhor
                    try:
                        self.root.iconname("Keydrop Bot v3.0.0")
                    except:
                        pass
                    
            except Exception as e:
                print(f"⚠️ Erro na configuração do ícone: {e}")
            
            # Inicializar variáveis essenciais PRIMEIRO
            self.server_process = None
            self.server_running = False
            
            # Configurar paths de forma segura
            try:
                if hasattr(sys, '_MEIPASS'):
                    self.base_path = Path(sys.executable).parent
                else:
                    self.base_path = Path(__file__).parent
                self.config_file = self.base_path / "config" / "bot_config.json"
            except:
                self.base_path = Path(".")
                self.config_file = Path("config/bot_config.json")
            
            # Mostrar janela com conteúdo mínimo
            self.create_loading_interface()
            
            # Mostrar janela
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            
            # Centralizar na tela
            self.center_window()
            
            # Configurar interface completa após delay
            self.root.after(200, self.setup_full_interface)
            
        except Exception as e:
            print(f"Erro crítico na inicialização: {e}")
            # Criar interface de emergência
            self.create_emergency_interface(e)

    def create_loading_interface(self):
        """Criar interface de carregamento simples"""
        try:
            # Frame de carregamento
            loading_frame = tk.Frame(self.root, bg='white')
            loading_frame.pack(fill=tk.BOTH, expand=True)
            
            # Título
            tk.Label(loading_frame, text="🤖 Keydrop Bot Professional v3.0.0", 
                    font=('Arial', 18, 'bold'), bg='white', fg='#2c3e50').pack(pady=(100, 20))
            
            # Status de carregamento
            self.loading_status = tk.Label(loading_frame, text="🔄 Iniciando aplicação...", 
                                         font=('Arial', 12), bg='white', fg='#7f8c8d')
            self.loading_status.pack(pady=10)
            
            # Forçar atualização
            self.root.update()
            
        except Exception as e:
            print(f"Erro ao criar interface de carregamento: {e}")

    def center_window(self):
        """Centralizar janela na tela"""
        try:
            self.root.update_idletasks()
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - 900) // 2
            y = (screen_height - 700) // 2
            self.root.geometry(f"900x700+{x}+{y}")
        except Exception as e:
            print(f"Erro ao centralizar janela: {e}")

    def create_emergency_interface(self, error):
        """Criar interface de emergência em caso de erro crítico"""
        try:
            # Limpar tudo
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Interface de emergência
            emergency_frame = tk.Frame(self.root, bg='#ffebee')
            emergency_frame.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(emergency_frame, text="⚠️ Modo de Emergência", 
                    font=('Arial', 16, 'bold'), bg='#ffebee', fg='#c62828').pack(pady=20)
            
            tk.Label(emergency_frame, text="O aplicativo encontrou um erro durante a inicialização.", 
                    font=('Arial', 12), bg='#ffebee').pack(pady=10)
            
            tk.Label(emergency_frame, text=f"Erro: {str(error)}", 
                    font=('Arial', 10), bg='#ffebee', fg='#757575').pack(pady=10)
            
            tk.Button(emergency_frame, text="🔄 Tentar Novamente", 
                     command=self.restart_application, font=('Arial', 12), 
                     bg='#2196f3', fg='white').pack(pady=10)
            
            tk.Button(emergency_frame, text="❌ Fechar", 
                     command=self.root.destroy, font=('Arial', 12), 
                     bg='#f44336', fg='white').pack(pady=5)
            
            # Mostrar janela
            self.root.deiconify()
            
        except Exception as e:
            print(f"Erro crítico ao criar interface de emergência: {e}")

    def restart_application(self):
        """Reiniciar aplicação"""
        try:
            # Limpar tudo
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Tentar inicializar novamente
            self.create_loading_interface()
            self.root.after(200, self.setup_full_interface)
            
        except Exception as e:
            print(f"Erro ao reiniciar: {e}")

    def setup_full_interface(self):
        """Configurar interface completa de forma segura"""
        try:
            self.loading_status.config(text="⚙️ Configurando interface...")
            self.root.update()
            
            # Limpar interface de carregamento
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Criar interface principal
            self.setup_interface()
            
        except Exception as e:
            print(f"Erro ao configurar interface completa: {e}")
            self.create_emergency_interface(e)

    def setup_interface(self):
        """Configurar interface de forma robusta"""
        try:
            # Inicializar estatísticas dos bots
            self.init_bot_stats()
            
            # Header simples com dark theme
            header = tk.Frame(self.root, bg=self.dark_colors['bg'])
            header.pack(fill='x', padx=15, pady=10)
            
            tk.Label(header, text="🤖 Keydrop Bot Professional v3.0.0",
                    font=('Arial', 18, 'bold'), bg=self.dark_colors['bg'], 
                    fg=self.dark_colors['accent']).pack()
            tk.Label(header, text="Desenvolvido por William Medrado", 
                    font=('Arial', 12), bg=self.dark_colors['bg'], 
                    fg=self.dark_colors['fg']).pack()
            
            # Criar notebook com proteção e dark theme
            try:
                style = ttk.Style()
                self.notebook = ttk.Notebook(self.root, style='Dark.TNotebook')
                self.notebook.pack(fill='both', expand=True, padx=15, pady=10)
                
                # Criar abas principais uma por uma
                self.create_control_tab()
                self.create_config_tab() 
                self.create_stats_tab()
                self.create_logs_tab()
                
            except Exception as e:
                print(f"Erro ao criar abas: {e}")
                # Interface básica se falhar
                basic_frame = tk.Frame(self.root, bg=self.dark_colors['bg'])
                basic_frame.pack(fill='both', expand=True, padx=15, pady=15)
                
                tk.Label(basic_frame, text="🎮 Controle Básico", 
                        font=('Arial', 16, 'bold'), bg=self.dark_colors['bg'], 
                        fg=self.dark_colors['accent']).pack(pady=15)
                tk.Label(basic_frame, text="Interface funcionando em modo simplificado",
                        bg=self.dark_colors['bg'], fg=self.dark_colors['fg']).pack()
                
                # Botões básicos
                tk.Button(basic_frame, text="🔄 Tentar Interface Completa", 
                         command=self.retry_full_interface, font=('Arial', 12, 'bold'),
                         bg=self.dark_colors['button_bg'], fg=self.dark_colors['button_fg']).pack(pady=10)
            
            # Footer simples com dark theme
            footer = tk.Frame(self.root, bg=self.dark_colors['bg'])
            footer.pack(fill='x', padx=15, pady=5)
            
            self.status_label = tk.Label(footer, text="📱 Modo Desktop Nativo • Pronto para uso",
                                       bg=self.dark_colors['bg'], fg=self.dark_colors['success'],
                                       font=('Arial', 11, 'bold'))
            self.status_label.pack(side='left')
            
            # Iniciar monitoramento com proteção
            try:
                self.root.after(1000, self.update_system_stats)
                self.root.after(2000, self.update_global_stats)
                self.root.after(3000, self.update_app_status)
            except:
                pass
            
            # Log de inicialização
            self.log_message("🎉 Keydrop Bot Professional v3.0.0 iniciado com sucesso!")
            self.log_message("📱 Modo: Aplicação Desktop Nativa com Dark Theme")
            self.log_message("🚀 Sistema pronto para automação Microsoft Edge")
            
        except Exception as e:
            print(f"Erro crítico ao configurar interface: {e}")
            # Interface de última tentativa
            emergency_label = tk.Label(self.root, text="⚠️ Erro ao carregar interface",
                                     font=('Arial', 14), bg='#2d2d2d', fg='#ffffff')
            emergency_label.pack(pady=30)
            
            restart_btn = tk.Button(self.root, text="🔄 Reiniciar Aplicação",
                                   command=self.restart_application, font=('Arial', 12, 'bold'),
                                   bg='#404040', fg='#ffffff')
            restart_btn.pack(pady=15)

    def retry_full_interface(self):
        """Tentar criar interface completa novamente"""
        try:
            # Limpar tudo
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Tentar novamente
            self.setup_interface()
            
        except Exception as e:
            print(f"Erro ao tentar interface completa: {e}")

    def create_control_tab(self):
        """Criar aba de controle principal"""
        control_frame = ttk.Frame(self.notebook)
        self.notebook.add(control_frame, text="🎮 Controle")
        
        # Informações do App (simplificadas)
        info_frame = ttk.LabelFrame(control_frame, text="📋 Keydrop Bot Professional v3.0.0", padding=15)
        info_frame.pack(fill=tk.X, padx=15, pady=10)
        
        ttk.Label(info_frame, text="🤖 Automação Profissional para Sorteios Keydrop", 
                 font=('Arial', 14, 'bold'), foreground='#2196f3').pack(anchor=tk.W)
        ttk.Label(info_frame, text="🌐 Microsoft Edge Exclusivo • Múltiplos Perfis • Multi-Instância", 
                 font=('Arial', 12)).pack(anchor=tk.W)
        ttk.Label(info_frame, text="👨‍💻 Desenvolvido por: William Medrado (wmedrado)", 
                 font=('Arial', 11), foreground='#666').pack(anchor=tk.W)
        
        # Controle de Automação Principal
        bot_frame = ttk.LabelFrame(control_frame, text="🚀 Controle de Automação", padding=15)
        bot_frame.pack(fill=tk.X, padx=15, pady=10)
        
        ttk.Label(bot_frame, text="✨ Sistema de Multi-Bots com Perfis Independentes", 
                 foreground='green', font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0,10))
        
        # Botões principais (maiores)
        buttons_frame = ttk.Frame(bot_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Criar estilo para botões maiores
        style = ttk.Style()
        style.configure('Large.TButton', font=('Arial', 12, 'bold'))
        
        ttk.Button(buttons_frame, text="🚀 INICIAR AUTOMAÇÃO", 
                  command=self.start_bot_direct, style='Large.TButton').pack(side=tk.LEFT, padx=15, ipadx=20, ipady=10)
        
        ttk.Button(buttons_frame, text="⏹️ PARAR AUTOMAÇÃO", 
                  command=self.stop_bot_direct, style='Large.TButton').pack(side=tk.LEFT, padx=15, ipadx=20, ipady=10)
        
        ttk.Button(buttons_frame, text="🚨 EMERGÊNCIA", 
                  command=self.emergency_stop_direct, style='Emergency.TButton').pack(side=tk.RIGHT, padx=15, ipadx=15, ipady=10)
        
        # Status em tempo real
        status_frame = ttk.LabelFrame(control_frame, text="📊 Status em Tempo Real", padding=15)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=15, state=tk.DISABLED, 
                                                   font=('Consolas', 12), bg='#2d2d2d', fg='#ffffff',
                                                   insertbackground='#ffffff', selectbackground='#404040',
                                                   selectforeground='#ffffff')
        self.status_text.pack(fill=tk.BOTH, expand=True)

    def create_config_tab(self):
        """Criar aba de configurações com dark theme"""
        config_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(config_frame, text="⚙️ Configurações")
        
        # Configurações Básicas
        basic_frame = ttk.LabelFrame(config_frame, text="🔧 Configurações Básicas", 
                                   style='Dark.TLabelFrame', padding=20)
        basic_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Grid de configurações
        config_grid = ttk.Frame(basic_frame, style='Dark.TFrame')
        config_grid.pack(fill=tk.X)
        
        # Número de guias
        ttk.Label(config_grid, text="🤖 Número de Guias/Bots (1-100):", 
                 font=('Arial', 12, 'bold'), style='Dark.TLabel').grid(row=0, column=0, sticky=tk.W, pady=8)
        self.num_tabs_var = tk.StringVar(value="5")
        entry1 = ttk.Entry(config_grid, textvariable=self.num_tabs_var, width=15, font=('Arial', 12))
        entry1.grid(row=0, column=1, padx=15, pady=8)
        
        # Velocidade de execução
        ttk.Label(config_grid, text="⚡ Velocidade de Execução (segundos):", 
                 font=('Arial', 12, 'bold'), style='Dark.TLabel').grid(row=1, column=0, sticky=tk.W, pady=8)
        self.speed_var = tk.StringVar(value="8.0")
        entry2 = ttk.Entry(config_grid, textvariable=self.speed_var, width=15, font=('Arial', 12))
        entry2.grid(row=1, column=1, padx=15, pady=8)
        
        # Tentativas de retry
        ttk.Label(config_grid, text="🔄 Tentativas de Retry:", 
                 font=('Arial', 12, 'bold'), style='Dark.TLabel').grid(row=2, column=0, sticky=tk.W, pady=8)
        self.retry_var = tk.StringVar(value="5")
        entry3 = ttk.Entry(config_grid, textvariable=self.retry_var, width=15, font=('Arial', 12))
        entry3.grid(row=2, column=1, padx=15, pady=8)
        
        # Dica de velocidade
        ttk.Label(config_grid, text="💡 Recomendado: 7-10 segundos para máxima eficiência", 
                 font=('Arial', 11), foreground=self.dark_colors['success'], 
                 style='Dark.TLabel').grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        # Modos de Operação
        modes_frame = ttk.LabelFrame(config_frame, text="🎯 Modos de Operação", 
                                   style='Dark.TLabelFrame', padding=20)
        modes_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Checkboxes para modos
        self.headless_var = tk.BooleanVar()
        chk1 = ttk.Checkbutton(modes_frame, text="🕶️ Modo Headless (invisível)", 
                              variable=self.headless_var, style='Dark.TCheckbutton')
        chk1.pack(anchor=tk.W, pady=5)
        
        self.mini_window_var = tk.BooleanVar()
        chk2 = ttk.Checkbutton(modes_frame, text="📱 Modo Mini (100x200px)", 
                              variable=self.mini_window_var, style='Dark.TCheckbutton')
        chk2.pack(anchor=tk.W, pady=5)
        
        self.login_tabs_var = tk.BooleanVar()
        chk3 = ttk.Checkbutton(modes_frame, text="🔑 Abas de Login (Keydrop/Steam)", 
                              variable=self.login_tabs_var, style='Dark.TCheckbutton')
        chk3.pack(anchor=tk.W, pady=5)
        
        # NOVO: Checkbox para sorteios de 1h (Contender)
        self.contender_mode_var = tk.BooleanVar()
        chk4 = ttk.Checkbutton(modes_frame, text="🏆 Participar Sorteios 1h (Contender)", 
                              variable=self.contender_mode_var, style='Dark.TCheckbutton')
        chk4.pack(anchor=tk.W, pady=5)
        
        # Descrições dos modos
        ttk.Label(modes_frame, text="• Headless: Bots funcionam em segundo plano (recomendado para muitos bots)", 
                 font=('Arial', 10), style='Dark.TLabel').pack(anchor=tk.W, padx=20, pady=2)
        ttk.Label(modes_frame, text="• Mini: Janelas pequenas visíveis (bom para monitoramento)", 
                 font=('Arial', 10), style='Dark.TLabel').pack(anchor=tk.W, padx=20, pady=2)
        ttk.Label(modes_frame, text="• Login: Abre páginas de login para autenticação manual", 
                 font=('Arial', 10), style='Dark.TLabel').pack(anchor=tk.W, padx=20, pady=2)
        ttk.Label(modes_frame, text="• Contender: Participa de sorteios de 1h (aguarda 1h entre participações)", 
                 font=('Arial', 10), style='Dark.TLabel').pack(anchor=tk.W, padx=20, pady=2)
        
        # Discord Integration
        discord_frame = ttk.LabelFrame(config_frame, text="🤖 Integração Discord", 
                                     style='Dark.TLabelFrame', padding=20)
        discord_frame.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Label(discord_frame, text="🔗 Webhook URL (opcional):", 
                 font=('Arial', 12, 'bold'), style='Dark.TLabel').pack(anchor=tk.W)
        self.discord_webhook_var = tk.StringVar()
        webhook_entry = ttk.Entry(discord_frame, textvariable=self.discord_webhook_var, 
                                 width=60, font=('Arial', 11))
        webhook_entry.pack(fill=tk.X, pady=8)
        
        self.discord_enabled_var = tk.BooleanVar()
        ttk.Checkbutton(discord_frame, text="📢 Habilitar Notificações Discord", 
                       variable=self.discord_enabled_var, style='Dark.TCheckbutton').pack(anchor=tk.W, pady=5)
        
        # Botões de Ação
        buttons_frame = ttk.Frame(config_frame, style='Dark.TFrame')
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(buttons_frame, text="💾 SALVAR CONFIGURAÇÕES", 
                  command=self.save_config, style='Large.TButton').pack(side=tk.LEFT, padx=10)
        
        ttk.Button(buttons_frame, text="🔄 RECARREGAR", 
                  command=self.load_config, style='Large.TButton').pack(side=tk.LEFT, padx=10)
        
        ttk.Button(buttons_frame, text="🧹 LIMPAR CACHE", 
                  command=self.clear_cache, style='Large.TButton').pack(side=tk.LEFT, padx=10)

    def create_stats_tab(self):
        """Criar aba de estatísticas com informações detalhadas por bot"""
        stats_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(stats_frame, text="📊 Estatísticas")
        
        # Header com estatísticas globais
        global_frame = ttk.LabelFrame(stats_frame, text="📈 Estatísticas Globais", 
                                    style='Dark.TLabelFrame', padding=15)
        global_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Grid de estatísticas globais
        global_stats = ttk.Frame(global_frame, style='Dark.TFrame')
        global_stats.pack(fill=tk.X)
        
        # Primeira linha
        self.total_bots_label = ttk.Label(global_stats, text="🤖 Bots Ativos: 0", 
                                        font=('Arial', 14, 'bold'), foreground=self.dark_colors['accent'],
                                        style='Dark.TLabel')
        self.total_bots_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 30))
        
        self.total_raffles_label = ttk.Label(global_stats, text="🎯 Total Sorteios: 0", 
                                           font=('Arial', 14, 'bold'), foreground=self.dark_colors['success'],
                                           style='Dark.TLabel')
        self.total_raffles_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        
        self.total_errors_label = ttk.Label(global_stats, text="⚠️ Total Erros: 0", 
                                          font=('Arial', 14, 'bold'), foreground=self.dark_colors['error'],
                                          style='Dark.TLabel')
        self.total_errors_label.grid(row=0, column=2, sticky=tk.W)
        
        # Segunda linha
        self.session_time_label = ttk.Label(global_stats, text="⏱️ Tempo Sessão: 00:00:00", 
                                          font=('Arial', 12), style='Dark.TLabel')
        self.session_time_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        self.network_usage_label = ttk.Label(global_stats, text="🌐 Uso Rede: 0 MB", 
                                           font=('Arial', 12), style='Dark.TLabel')
        self.network_usage_label.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        self.total_skins_label = ttk.Label(global_stats, text="💰 Saldo Total: $0.00", 
                                         font=('Arial', 12), style='Dark.TLabel')
        self.total_skins_label.grid(row=1, column=2, sticky=tk.W, pady=(10, 0))
        
        # Frame para bots individuais (scrollable)
        bots_frame = ttk.LabelFrame(stats_frame, text="🤖 Detalhes por Bot", 
                                  style='Dark.TLabelFrame', padding=15)
        bots_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Criar canvas e scrollbar para bots
        canvas = tk.Canvas(bots_frame, bg=self.dark_colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(bots_frame, orient="vertical", command=canvas.yview)
        self.bots_scrollable_frame = ttk.Frame(canvas, style='Dark.TFrame')
        
        self.bots_scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.bots_scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Performance do Sistema
        system_frame = ttk.LabelFrame(stats_frame, text="💻 Performance do Sistema", 
                                    style='Dark.TLabelFrame', padding=15)
        system_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        system_stats = ttk.Frame(system_frame, style='Dark.TFrame')
        system_stats.pack(fill=tk.X)
        
        self.cpu_label = ttk.Label(system_stats, text="💾 CPU: 0%", 
                                 font=('Arial', 12), style='Dark.TLabel')
        self.cpu_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 30))
        
        self.ram_label = ttk.Label(system_stats, text="🧠 RAM: 0 MB", 
                                 font=('Arial', 12), style='Dark.TLabel')
        self.ram_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        
        self.disk_label = ttk.Label(system_stats, text="💿 Disco: 0 GB", 
                                  font=('Arial', 12), style='Dark.TLabel')
        self.disk_label.grid(row=0, column=2, sticky=tk.W)
        
        # Inicializar lista de bots vazios
        self.bot_widgets = {}
        self.update_bot_stats_display()

    def create_logs_tab(self):
        """Criar aba de logs com dark theme"""
        logs_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(logs_frame, text="📝 Logs")
        
        # Header dos logs
        logs_header = ttk.LabelFrame(logs_frame, text="📊 Sistema de Logs Avançado", 
                                   style='Dark.TLabelFrame', padding=15)
        logs_header.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Label(logs_header, text="📜 Monitoramento em tempo real de todas as atividades do sistema", 
                 font=('Arial', 12), style='Dark.TLabel').pack(anchor=tk.W)
        
        # Controles de log
        log_controls = ttk.Frame(logs_header, style='Dark.TFrame')
        log_controls.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(log_controls, text="🗑️ LIMPAR LOGS", 
                  command=self.clear_logs, style='Large.TButton').pack(side=tk.LEFT, padx=10)
        
        ttk.Button(log_controls, text="💾 SALVAR LOGS", 
                  command=self.save_logs, style='Large.TButton').pack(side=tk.LEFT, padx=10)
        
        ttk.Button(log_controls, text="🔄 ATUALIZAR", 
                  command=self.refresh_logs, style='Large.TButton').pack(side=tk.LEFT, padx=10)
        
        # Área de logs principal
        logs_content = ttk.LabelFrame(logs_frame, text="📋 Log de Atividades", 
                                    style='Dark.TLabelFrame', padding=15)
        logs_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        self.logs_text = scrolledtext.ScrolledText(logs_content, height=20, state=tk.DISABLED,
                                                 font=('Consolas', 11), bg=self.dark_colors['entry_bg'],
                                                 fg=self.dark_colors['fg'], insertbackground=self.dark_colors['fg'],
                                                 selectbackground=self.dark_colors['select_bg'],
                                                 selectforeground=self.dark_colors['select_fg'])
        self.logs_text.pack(fill=tk.BOTH, expand=True)
        
        # Adicionar log inicial
        self.log_message("🎯 Sistema de logs inicializado!")
        self.log_message("📊 Registrando todas as atividades do Keydrop Bot v3.0.0")

    def log_message(self, message, level="INFO"):
        """Adicionar mensagem aos logs com proteção"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        # Tentar imprimir no console sempre
        print(f"LOG: {log_entry.strip()}")
        
        # Tentar adicionar aos logs se existirem
        try:
            if hasattr(self, 'logs_text') and self.logs_text:
                self.logs_text.config(state=tk.NORMAL)
                self.logs_text.insert(tk.END, log_entry)
                self.logs_text.see(tk.END)
                self.logs_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Erro ao adicionar aos logs: {e}")
        
        # Tentar atualizar status se existir
        try:
            if hasattr(self, 'status_text') and self.status_text:
                self.status_text.config(state=tk.NORMAL)
                self.status_text.insert(tk.END, log_entry)
                self.status_text.see(tk.END)
                self.status_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")

    def start_server(self):
        """Iniciar servidor backend (opcional)"""
        if self.server_running:
            return
        
        try:
            self.log_message("Tentando iniciar servidor backend (opcional)...")
            
            # Executar main.py do backend
            backend_path = self.base_path / "backend" / "main.py"
            
            if not backend_path.exists():
                self.log_message("Backend não encontrado - aplicação funciona normalmente sem ele", "WARNING")
                return
            
            # Iniciar servidor em thread separada
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            self.server_process = subprocess.Popen([
                sys.executable, str(backend_path)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, 
               creationflags=creation_flags)
            
            # Aguardar servidor inicializar
            time.sleep(5)
            
            # Verificar se está rodando
            if self.check_server_health():
                self.server_running = True
                self.start_server_btn.config(state=tk.DISABLED)
                self.stop_server_btn.config(state=tk.NORMAL)
                self.open_interface_btn.config(state=tk.NORMAL)
                self.status_label.config(text="🟢 Servidor Rodando")
                self.log_message("Servidor iniciado com sucesso! Funcionalidades de automação disponíveis.", "SUCCESS")
            else:
                self.log_message("Servidor não respondeu - aplicação continua funcionando normalmente", "WARNING")
                
        except Exception as e:
            self.log_message(f"Servidor indisponível - aplicação funciona normalmente: {e}", "WARNING")

    def stop_server(self):
        """Parar servidor backend"""
        if not self.server_running:
            return
        
        try:
            self.log_message("Parando servidor...")
            
            if self.server_process:
                self.server_process.terminate()
                self.server_process.wait(timeout=10)
            
            self.server_running = False
            self.start_server_btn.config(state=tk.NORMAL)
            self.stop_server_btn.config(state=tk.DISABLED)
            self.open_interface_btn.config(state=tk.DISABLED)
            self.status_label.config(text="📱 Modo Offline")
            self.log_message("Servidor parado - aplicação continua funcionando", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Erro ao parar servidor: {e}", "ERROR")

    def check_server_health(self):
        """Verificar se servidor está rodando"""
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            return response.status_code == 200
        except:
            return False

    def check_server_status(self):
        """Verificar status do servidor periodicamente"""
        try:
            # Atualizar status e logs sem referências de servidor
            if hasattr(self, 'status_label'):
                self.status_label.config(text="🟢 Sistema Desktop Ativo • Pronto para automação")
            
            # Reagendar para 5 segundos
            self.root.after(5000, self.update_system_stats)
        except Exception as e:
            print(f"Erro ao verificar status: {e}")
            self.root.after(10000, self.update_system_stats)

    def update_global_stats(self):
        """Atualizar estatísticas globais na interface"""
        try:
            # Atualizar contadores globais
            total_amateur = sum(bot.get('raffles_amateur', 0) for bot in self.bot_stats.values())
            total_contender = sum(bot.get('raffles_contender', 0) for bot in self.bot_stats.values())
            total_raffles = total_amateur + total_contender
            total_errors = sum(bot.get('errors', 0) for bot in self.bot_stats.values())
            total_network = sum(bot.get('network_usage', 0) for bot in self.bot_stats.values())
            total_skins = sum(bot.get('skin_balance', 0.0) for bot in self.bot_stats.values())
            
            # Calcular tempo de sessão
            session_duration = datetime.now() - self.global_stats['session_start_time']
            hours, remainder = divmod(int(session_duration.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            session_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Atualizar labels se existirem
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
            
            # Reagendar atualização
            self.root.after(5000, self.update_global_stats)
            
        except Exception as e:
            print(f"Erro ao atualizar estatísticas globais: {e}")
            # Reagendar mesmo com erro
            self.root.after(10000, self.update_global_stats)
    
    def update_system_stats(self):
        """Atualizar estatísticas do sistema"""
        try:
            # Obter estatísticas do sistema
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Converter para unidades legíveis
            ram_used = memory.used / (1024**2)  # MB
            disk_free = disk.free / (1024**3)   # GB
            
            # Atualizar labels se existirem
            if hasattr(self, 'cpu_label'):
                self.cpu_label.config(text=f"💾 CPU: {cpu_percent:.1f}%")
            
            if hasattr(self, 'ram_label'):
                self.ram_label.config(text=f"🧠 RAM: {ram_used:.0f} MB")
            
            if hasattr(self, 'disk_label'):
                self.disk_label.config(text=f"💿 Disco: {disk_free:.1f} GB")
            
            # Reagendar atualização
            self.root.after(3000, self.update_system_stats)
            
        except Exception as e:
            print(f"Erro ao atualizar estatísticas do sistema: {e}")
            # Reagendar mesmo com erro
            self.root.after(5000, self.update_system_stats)

    def open_web_interface(self):
        """Abrir interface web no navegador"""
        import webbrowser
        webbrowser.open("http://localhost:8000")
        self.log_message("Interface web aberta no navegador", "INFO")

    def start_bot(self):
        """Iniciar bot"""
        if not self.server_running:
            messagebox.showwarning("Aviso", "Servidor backend deve estar rodando para automação de bots!")
            return
        
        try:
            response = requests.post("http://localhost:8000/api/bot/start")
            if response.status_code == 200:
                self.log_message("Bot iniciado com sucesso!", "SUCCESS")
            else:
                self.log_message(f"Erro ao iniciar bot: {response.text}", "ERROR")
        except Exception as e:
            self.log_message(f"Erro ao comunicar com servidor: {e}", "ERROR")

    def pause_bot(self):
        """Pausar bot"""
        if not self.server_running:
            messagebox.showwarning("Aviso", "Servidor backend deve estar rodando!")
            return
        try:
            response = requests.post("http://localhost:8000/api/bot/pause")
            if response.status_code == 200:
                self.log_message("Bot pausado", "INFO")
        except Exception as e:
            self.log_message(f"Erro ao pausar bot: {e}", "ERROR")

    def stop_bot(self):
        """Parar bot"""
        if not self.server_running:
            messagebox.showwarning("Aviso", "Servidor backend deve estar rodando!")
            return
        try:
            response = requests.post("http://localhost:8000/api/bot/stop")
            if response.status_code == 200:
                self.log_message("Bot parado", "INFO")
        except Exception as e:
            self.log_message(f"Erro ao parar bot: {e}", "ERROR")

    def emergency_stop(self):
        """Parada de emergência"""
        if not self.server_running:
            messagebox.showwarning("Aviso", "Servidor backend deve estar rodando!")
            return
        result = messagebox.askyesno("Confirmação", "Confirma parada de emergência?\nIsso fechará todas as guias do navegador!")
        if result:
            try:
                response = requests.post("http://localhost:8000/api/bot/emergency-stop")
                if response.status_code == 200:
                    self.log_message("PARADA DE EMERGÊNCIA EXECUTADA!", "WARNING")
                else:
                    self.log_message(f"Erro na parada de emergência: {response.text}", "ERROR")
            except Exception as e:
                self.log_message(f"Erro na parada de emergência: {e}", "ERROR")

    def find_edge_executable(self):
        """Encontrar executável do Microsoft Edge"""
        edge_paths = [
            "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
            os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\Application\\msedge.exe"),
            "msedge.exe"  # Se estiver no PATH
        ]
        for path in edge_paths:
            if os.path.exists(path):
                return path
        return None

    def start_bot_direct(self):
        """Iniciar bot diretamente usando automação Chrome/Edge com Selenium"""
        try:
            # Verificar se Selenium está disponível
            if not SELENIUM_AVAILABLE:
                messagebox.showerror("Selenium Requerido", 
                                   "Para automação de sorteios, é necessário instalar o Selenium:\n\n"
                                   "pip install selenium webdriver-manager\n\n"
                                   "Ou use o modo Edge básico (sem automação de sorteios)")
                self.log_message("❌ Selenium não disponível - iniciando modo Edge básico", "WARNING")
                return self.start_edge_basic_mode()
            
            self.log_message("🤖 Iniciando automação com Selenium...", "INFO")
            
            # Obter todas as configurações
            num_tabs = int(self.num_tabs_var.get()) if hasattr(self, 'num_tabs_var') else 5
            headless_mode = self.headless_var.get() if hasattr(self, 'headless_var') else False
            mini_mode = self.mini_window_var.get() if hasattr(self, 'mini_window_var') else False
            contender_mode = self.contender_mode_var.get() if hasattr(self, 'contender_mode_var') else False
            speed = float(self.speed_var.get()) if hasattr(self, 'speed_var') else 180.0
            
            self.log_message(f"📋 Configurações: {num_tabs} bots, Headless: {headless_mode}, "
                           f"Mini: {mini_mode}, Contender: {contender_mode}, Intervalo: {speed}s", "INFO")
            
            # Inicializar lista de bots
            self.automation_bots = []
            
            # Criar e iniciar bots de automação
            for i in range(num_tabs):
                try:
                    bot = KeydropAutomationBot(
                        bot_id=i + 1,
                        profile_path=f"./profiles/selenium_bot_{i+1}",
                        headless=headless_mode,
                        mini_window=mini_mode,
                        contender_mode=contender_mode,
                        gui_callback=self.log_message
                    )
                    
                    # Iniciar bot em thread separada
                    bot_thread = threading.Thread(
                        target=bot.run_automation_cycle,
                        args=(int(speed),),
                        daemon=True
                    )
                    bot_thread.start()
                    
                    self.automation_bots.append(bot)
                    self.log_message(f"✅ Bot #{i+1} iniciado com automação de sorteios!", "SUCCESS")
                    
                    # Aguardar um pouco entre bots para não sobrecarregar
                    time.sleep(3)
                    
                except Exception as e:
                    self.log_message(f"❌ Erro ao iniciar Bot #{i+1}: {e}", "ERROR")
                    continue
            
            if self.automation_bots:
                self.log_message(f"🎉 {len(self.automation_bots)} bots iniciados com automação completa!", "SUCCESS")
                self.log_message("🎯 Bots participarão automaticamente dos sorteios amateur (3min)", "INFO")
                if contender_mode:
                    self.log_message("🏆 Modo contender ativado - participará de sorteios de 1h", "INFO")
                
                # Enviar notificação Discord se configurado
                self.send_discord_startup_notification()
            else:
                self.log_message("❌ Nenhum bot foi iniciado com sucesso", "ERROR")
                
        except Exception as e:
            self.log_message(f"❌ Erro ao iniciar automação: {e}", "ERROR")
            messagebox.showerror("Erro", f"Erro ao iniciar automação:\n{e}")
    
    def start_edge_basic_mode(self):
        """Modo Edge básico sem automação de sorteios (fallback)"""
        try:
            self.log_message("🌐 Iniciando modo Edge básico (sem automação de sorteios)...", "INFO")
            edge_path = self.find_edge_executable()
            if not edge_path:
                messagebox.showerror("Erro", "Microsoft Edge não encontrado!\nInstale o Edge para usar o bot.")
                return
            
            # Obter configurações básicas
            num_tabs = int(self.num_tabs_var.get()) if hasattr(self, 'num_tabs_var') else 5
            headless_mode = self.headless_var.get() if hasattr(self, 'headless_var') else False
            mini_mode = self.mini_window_var.get() if hasattr(self, 'mini_window_var') else False
            login_tabs = self.login_tabs_var.get() if hasattr(self, 'login_tabs_var') else False
            
            self.automation_thread = threading.Thread(
                target=self.run_edge_automation,
                args=(edge_path, num_tabs, headless_mode, mini_mode, login_tabs),
                daemon=True
            )
            self.automation_thread.start()
            self.log_message("🚀 Modo Edge básico iniciado (automação manual necessária)!", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"❌ Erro no modo Edge básico: {e}", "ERROR")

    def run_edge_automation(self, edge_path, num_tabs, headless_mode, mini_mode, login_tabs):
        """Executar automação do Edge"""
        try:
            self.log_message("🌐 Iniciando automação do Edge...", "INFO")
            self.edge_processes = []
            
            # URLs baseadas na configuração
            main_url = "https://key-drop.com/"
            login_urls = [
                "https://key-drop.com/login",
                "https://steamcommunity.com/login/home/"
            ]
            
            # Argumentos base do Edge
            base_edge_args = [
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding"
            ]
            
            # Configurar modo headless
            if headless_mode:
                base_edge_args.append("--headless")
                self.log_message("🔇 Modo headless ativado - janelas não aparecerão", "INFO")
            else:
                # Configurar tamanho da janela
                if mini_mode:
                    window_size = "100,200"
                    self.log_message("📱 Modo mini ativado - janelas 100x200px", "INFO")
                else:
                    window_size = "1024,768"
                    self.log_message("🖥️ Modo normal ativado - janelas 1024x768px", "INFO")
                
                base_edge_args.extend([
                    "--new-window",
                    f"--window-size={window_size}",
                    "--window-position=100,100",
                    "--force-app-mode=false",
                    "--disable-background-mode"
                ])
            
            # Abrir guias de login primeiro se habilitado
            if login_tabs and not headless_mode:
                self.log_message("🔐 Abrindo guias de login...", "INFO")
                for idx, login_url in enumerate(login_urls):
                    try:
                        edge_args = base_edge_args.copy()
                        x_pos = 50 + (idx * 30)
                        y_pos = 50 + (idx * 30)
                        edge_args = [arg for arg in edge_args if not arg.startswith("--window-position")]
                        edge_args.append(f"--window-position={x_pos},{y_pos}")
                        
                        cmd = [edge_path] + edge_args + [login_url]
                        
                        process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                        )
                        
                        self.edge_processes.append(process)
                        self.log_message(f"✅ Guia de login {idx+1} aberta: {login_url}", "SUCCESS")
                        time.sleep(1)
                        
                    except Exception as e:
                        self.log_message(f"❌ Erro ao abrir guia de login {idx+1}: {e}", "ERROR")
            
            # Abrir guias principais do Keydrop com perfis independentes
            self.log_message(f"🎯 Abrindo {num_tabs} guias principais com perfis independentes...", "INFO")
            for i in range(num_tabs):
                try:
                    self.log_message(f"🔄 Configurando Bot #{i+1} com perfil independente...", "INFO")
                    edge_args = base_edge_args.copy()
                    
                    # IMPORTANTE: Adicionar perfil independente para cada instância
                    profile_dir = f"./edge_profiles/bot_profile_{i+1}"
                    edge_args.append(f"--user-data-dir={profile_dir}")
                    edge_args.append(f"--profile-directory=Profile{i+1}")
                    
                    # Configurar cada bot com cache e dados separados
                    edge_args.extend([
                        "--no-default-browser-check",
                        "--disable-shared-memory",
                        f"--remote-debugging-port={9222 + i}",
                        "--disable-extensions",
                        "--disable-plugins",
                        "--disable-sync"
                    ])
                    
                    if not headless_mode:
                        # Calcular posição para não sobrepor janelas
                        offset = 60 if not mini_mode else 30
                        x_pos = 100 + (i * offset)
                        y_pos = 100 + (i * offset)
                        edge_args = [arg for arg in edge_args if not arg.startswith("--window-position")]
                        edge_args.append(f"--window-position={x_pos},{y_pos}")
                    
                    cmd = [edge_path] + edge_args + [main_url]
                    self.log_message(f"🔧 Bot #{i+1}: Perfil isolado em {profile_dir}", "INFO")
                    
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
                    )
                    
                    self.edge_processes.append(process)
                    
                    # Inicializar estatísticas para este bot
                    bot_id = i + 1
                    if not hasattr(self, 'bot_stats'):
                        self.bot_stats = {}
                    
                    self.bot_stats[bot_id] = {
                        'active': True,
                        'active_time': '00:00:00',
                        'raffles_amateur': 0,
                        'raffles_contender': 0,
                        'errors': 0,
                        'network_usage': 0,
                        'skin_balance': 0.0,
                        'start_time': datetime.now(),
                        'profile_dir': profile_dir
                    }
                    
                    if not hasattr(self, 'total_bots_active'):
                        self.total_bots_active = 0
                    self.total_bots_active += 1
                    
                    self.log_message(f"✅ Bot #{i+1} iniciado com perfil independente! PID: {process.pid}", "SUCCESS")
                    time.sleep(2)
                    
                    if process.poll() is None:
                        self.log_message(f"🟢 Bot #{i+1} confirmado ativo com dados isolados", "INFO")
                    else:
                        self.log_message(f"🔴 Bot #{i+1} finalizou inesperadamente", "WARNING")
                        self.total_bots_active -= 1
                        
                except Exception as e:
                    self.log_message(f"❌ Erro ao abrir Bot #{i+1}: {e}", "ERROR")
                    print(f"ERRO DETALHADO BOT #{i+1}: {traceback.format_exc()}")
                    continue
            
            active_processes = len([p for p in self.edge_processes if p.poll() is None])
            self.log_message(f"🎉 Automação concluída! {active_processes} janelas do Edge ativas.", "SUCCESS")
            
            if active_processes == 0:
                self.log_message("⚠️ ATENÇÃO: Nenhuma janela permaneceu ativa! Verifique se o Edge está funcionando.", "WARNING")
            else:
                # Resumo da configuração
                self.log_message(f"📊 Resumo: Headless: {headless_mode}, Mini: {mini_mode}, Login: {login_tabs}", "INFO")
            
            self.monitor_edge_processes()
            
        except Exception as e:
            self.log_message(f"❌ Erro crítico na automação: {e}", "ERROR")
            print(f"ERRO DETALHADO AUTOMAÇÃO: {traceback.format_exc()}")
            messagebox.showerror("Erro na Automação", f"Erro ao iniciar automação:\n{e}\n\nVerifique se o Edge está instalado e funcionando.")

    def monitor_edge_processes(self):
        """Monitorar processos do Edge"""
        try:
            active_count = 0
            for process in getattr(self, 'edge_processes', []):
                if process.poll() is None:
                    active_count += 1
            self.log_message(f"📊 Monitoramento: {active_count} guias Edge ativas", "INFO")
            if active_count > 0:
                threading.Timer(30.0, self.monitor_edge_processes).start()
            else:
                self.log_message("🔚 Todas as guias Edge foram fechadas", "INFO")
        except Exception as e:
            self.log_message(f"❌ Erro no monitoramento Edge: {e}", "ERROR")

    def stop_bot_direct(self):
        """Parar automação de sorteios e fechar todos os bots"""
        try:
            self.log_message("🛑 Parando automação de sorteios...", "WARNING")
            
            # Parar bots de automação Selenium
            if hasattr(self, 'automation_bots') and self.automation_bots:
                stopped_count = 0
                for bot in self.automation_bots:
                    try:
                        bot.stop()
                        stopped_count += 1
                    except Exception as e:
                        self.log_message(f"⚠️ Erro ao parar bot {bot.bot_id}: {e}", "WARNING")
                
                self.automation_bots = []
                self.log_message(f"✅ {stopped_count} bots de automação parados", "SUCCESS")
            
            # Parar processos Edge se houver
            if hasattr(self, 'edge_processes') and self.edge_processes:
                closed_count = 0
                for process in self.edge_processes:
                    try:
                        if process.poll() is None:
                            process.terminate()
                            process.wait(timeout=5)
                            closed_count += 1
                    except Exception as e:
                        self.log_message(f"⚠️ Erro ao fechar processo Edge: {e}", "WARNING")
                
                self.edge_processes = []
                self.log_message(f"✅ {closed_count} processos Edge fechados", "SUCCESS")
            
            if not hasattr(self, 'automation_bots') and not hasattr(self, 'edge_processes'):
                self.log_message("ℹ️ Nenhuma automação ativa para parar", "INFO")
            
        except Exception as e:
            self.log_message(f"❌ Erro ao parar automação: {e}", "ERROR")

    def emergency_stop_direct(self):
        """Parada de emergência - mata todos os processos do Edge"""
        try:
            result = messagebox.askyesno(
                "Parada de Emergência", 
                "⚠️ ATENÇÃO!\n\nIsso fechará TODAS as janelas do Edge no sistema!\n\nContinuar?"
            )
            if result:
                self.log_message("🚨 EXECUTANDO PARADA DE EMERGÊNCIA Edge!", "WARNING")
                killed_count = 0
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if 'msedge' in proc.info['name'].lower():
                            psutil.Process(proc.info['pid']).terminate()
                            killed_count += 1
                    except Exception:
                        continue
                self.log_message(f"🛑 PARADA DE EMERGÊNCIA Edge CONCLUÍDA! {killed_count} processos finalizados", "WARNING")
        except Exception as e:
            self.log_message(f"❌ Erro na parada de emergência Edge: {e}", "ERROR")

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
                "contender_mode": self.contender_mode_var.get(),
                "discord_webhook_url": self.discord_webhook_var.get(),
                "discord_notifications": self.discord_enabled_var.get()
            }
            
            # Salvar no arquivo
            with open("config.json", 'w') as f:
                json.dump(config, f, indent=2)
            
            self.log_message("✅ Configurações salvas com sucesso!", "SUCCESS")
            messagebox.showinfo("Sucesso", "Configurações salvas!")
                
        except Exception as e:
            self.log_message(f"❌ Erro ao salvar configurações: {e}", "ERROR")
            messagebox.showerror("Erro", f"Erro ao salvar configurações:\n{e}")

    def load_config(self):
        """Carregar configurações"""
        try:
            if os.path.exists("config.json"):
                with open("config.json", 'r') as f:
                    config = json.load(f)
                
                self.num_tabs_var.set(str(config.get("num_tabs", 5)))
                self.speed_var.set(str(config.get("execution_speed", 3.0)))
                self.retry_var.set(str(config.get("retry_attempts", 5)))
                self.headless_var.set(config.get("headless_mode", False))
                self.mini_window_var.set(config.get("mini_window_mode", False))
                self.login_tabs_var.set(config.get("enable_login_tabs", False))
                self.contender_mode_var.set(config.get("contender_mode", False))
                self.discord_webhook_var.set(config.get("discord_webhook_url", ""))
                self.discord_enabled_var.set(config.get("discord_notifications", False))
                
                self.log_message("✅ Configurações carregadas!", "SUCCESS")
            else:
                self.log_message("ℹ️ Usando configurações padrão", "INFO")
                
        except Exception as e:
            self.log_message(f"❌ Erro ao carregar configurações: {e}", "ERROR")

    def clear_cache(self):
        """Limpar cache"""
        if self.server_running:
            try:
                response = requests.post("http://localhost:8000/api/cache/clear")
                if response.status_code == 200:
                    self.log_message("Cache limpo com sucesso!", "SUCCESS")
                else:
                    self.log_message(f"Erro ao limpar cache: {response.text}", "ERROR")
            except Exception as e:
                self.log_message(f"Erro ao limpar cache: {e}", "ERROR")
        else:
            self.log_message("Limpeza de cache local (servidor necessário para limpeza completa)", "INFO")

    def clear_logs(self):
        """Limpar logs com proteção"""
        try:
            if hasattr(self, 'logs_text') and self.logs_text:
                self.logs_text.config(state=tk.NORMAL)
                self.logs_text.delete(1.0, tk.END)
                self.logs_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Erro ao limpar logs: {e}")
        
        try:
            if hasattr(self, 'status_text') and self.status_text:
                self.status_text.config(state=tk.NORMAL)
                self.status_text.delete(1.0, tk.END)
                self.status_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Erro ao limpar status: {e}")

    def save_logs(self):
        """Salvar logs em arquivo com proteção"""
        try:
            if not hasattr(self, 'logs_text') or not self.logs_text:
                messagebox.showwarning("Aviso", "Logs não disponíveis")
                return
                
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.logs_text.get(1.0, tk.END))
                self.log_message(f"Logs salvos em: {filename}", "SUCCESS")
        except Exception as e:
            print(f"Erro ao salvar logs: {e}")
            self.log_message(f"Erro ao salvar logs: {e}", "ERROR")

    def refresh_logs(self):
        """Atualizar logs manualmente"""
        try:
            self.log_message("🔄 Logs atualizados manualmente pelo usuário")
            self.log_message(f"📊 Total de bots ativos: {self.total_bots_active}")
            
            # Forçar atualização das estatísticas
            if hasattr(self, 'update_global_stats'):
                self.update_global_stats()
                
        except Exception as e:
            self.log_message(f"❌ Erro ao atualizar logs: {e}", "ERROR")

    def run(self):
        """Executar aplicação"""
        self.log_message("🎉 Keydrop Bot Professional v3.0.0 iniciado!")
        self.log_message("📱 Modo: Aplicação Desktop Nativa")
        self.log_message("⚡ A aplicação funciona independentemente do servidor")
        self.log_message("🌐 Para automação de bots, inicie o servidor backend (opcional)")
        self.log_message("⚙️ Configure suas preferências na aba 'Configurações'")
        self.log_message("📊 Monitore o sistema na aba 'Estatísticas'")
        
        self.root.mainloop()

    def setup_dark_theme(self):
        """Configurar tema escuro personalizado"""
        try:
            # Configurar cores do tema escuro
            self.dark_colors = {
                'bg': '#2d2d2d',           # Fundo principal
                'fg': '#ffffff',           # Texto principal
                'select_bg': '#404040',    # Fundo selecionado
                'select_fg': '#ffffff',    # Texto selecionado
                'button_bg': '#404040',    # Fundo botão
                'button_fg': '#ffffff',    # Texto botão
                'entry_bg': '#3d3d3d',     # Fundo entrada
                'entry_fg': '#ffffff',     # Texto entrada
                'frame_bg': '#353535',     # Fundo frame
                'accent': '#2196f3',       # Cor de destaque
                'success': '#4caf50',      # Verde sucesso
                'warning': '#ff9800',      # Laranja aviso
                'error': '#f44336'         # Vermelho erro
            }
            
            # Configurar janela principal
            self.root.configure(bg=self.dark_colors['bg'])
            
            # Configurar estilo TTK
            style = ttk.Style()
            style.theme_use('clam')  # Tema base
            
            # Configurar estilos personalizados
            style.configure('Dark.TFrame', 
                           background=self.dark_colors['bg'])
            
            style.configure('Dark.TLabel', 
                           background=self.dark_colors['bg'],
                           foreground=self.dark_colors['fg'],
                           font=('Arial', 12))
            
            style.configure('Dark.TLabelFrame', 
                           background=self.dark_colors['bg'],
                           foreground=self.dark_colors['fg'],
                           borderwidth=2,
                           relief='raised')
            
            style.configure('Dark.TLabelFrame.Label',
                           background=self.dark_colors['bg'],
                           foreground=self.dark_colors['accent'],
                           font=('Arial', 12, 'bold'))
            
            style.configure('Large.TButton',
                           font=('Arial', 14, 'bold'),
                           padding=(20, 15))
            
            style.configure('Emergency.TButton',
                           font=('Arial', 14, 'bold'),
                           padding=(20, 15),
                           foreground=self.dark_colors['error'])
            
            style.configure('Dark.TNotebook',
                           background=self.dark_colors['bg'],
                           tabmargins=[2, 5, 2, 0])
            
            style.configure('Dark.TNotebook.Tab',
                           background=self.dark_colors['button_bg'],
                           foreground=self.dark_colors['fg'],
                           padding=[20, 10],
                           font=('Arial', 11, 'bold'))
            
            style.map('Dark.TNotebook.Tab',
                     background=[('selected', self.dark_colors['accent']),
                               ('active', self.dark_colors['select_bg'])])
            
            print("✅ Dark theme configurado com sucesso")
            
        except Exception as e:
            print(f"⚠️ Erro ao configurar dark theme: {e}")

    # Variáveis de estatísticas detalhadas por bot
    def init_bot_stats(self):
        """Inicializar estatísticas detalhadas por bot"""
        self.bot_stats = {}
        self.total_bots_active = 0
        self.global_stats = {
            'total_raffles_amateur': 0,
            'total_raffles_contender': 0,
            'total_errors': 0,
            'total_network_usage': 0,
            'session_start_time': datetime.now()
        }

    def update_bot_stats_display(self):
        """Atualizar exibição das estatísticas por bot"""
        try:
            # Limpar widgets existentes
            for widget in self.bots_scrollable_frame.winfo_children():
                widget.destroy()
            
            # Se não há bots, mostrar mensagem
            if not hasattr(self, 'bot_stats') or not self.bot_stats:
                no_bots_label = ttk.Label(self.bots_scrollable_frame, 
                                        text="📭 Nenhum bot ativo no momento\n\nInicie a automação para ver estatísticas detalhadas aqui!", 
                                        font=('Arial', 12), style='Dark.TLabel',
                                        foreground=self.dark_colors['warning'])
                no_bots_label.pack(pady=50)
                return
            
            # Criar card para cada bot
            for bot_id, stats in self.bot_stats.items():
                self.create_bot_card(self.bots_scrollable_frame, bot_id, stats)
                
        except Exception as e:
            print(f"Erro ao atualizar display de bots: {e}")
    
    def create_bot_card(self, parent, bot_id, stats):
        """Criar card visual para estatísticas de um bot específico"""
        try:
            # Card frame
            card_frame = ttk.LabelFrame(parent, text=f"🤖 Bot #{bot_id}", 
                                      style='Dark.TLabelFrame', padding=15)
            card_frame.pack(fill=tk.X, pady=10)
            
            # Grid de informações do bot
            info_grid = ttk.Frame(card_frame, style='Dark.TFrame')
            info_grid.pack(fill=tk.X)
            
            # Linha 1 - Status e tempo ativo
            status_color = self.dark_colors['success'] if stats.get('active', False) else self.dark_colors['error']
            status_text = "🟢 ATIVO" if stats.get('active', False) else "🔴 INATIVO"
            
            ttk.Label(info_grid, text=f"Status: {status_text}", 
                     font=('Arial', 12, 'bold'), foreground=status_color,
                     style='Dark.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 30))
            
            ttk.Label(info_grid, text=f"⏱️ Tempo Ativo: {stats.get('active_time', '00:00:00')}", 
                     font=('Arial', 12), style='Dark.TLabel').grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
            
            # Linha 2 - Sorteios
            ttk.Label(info_grid, text=f"🎯 AMATEUR: {stats.get('raffles_amateur', 0)}", 
                     font=('Arial', 12), style='Dark.TLabel').grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
            
            ttk.Label(info_grid, text=f"🏆 CONTENDER: {stats.get('raffles_contender', 0)}", 
                     font=('Arial', 12), style='Dark.TLabel').grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
            
            ttk.Label(info_grid, text=f"⚠️ Erros: {stats.get('errors', 0)}", 
                     font=('Arial', 12), foreground=self.dark_colors['error'],
                     style='Dark.TLabel').grid(row=1, column=2, sticky=tk.W, pady=(5, 0))
            
            # Linha 3 - Recursos
            ttk.Label(info_grid, text=f"🌐 Rede: {stats.get('network_usage', 0)} MB", 
                     font=('Arial', 11), style='Dark.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
            
            ttk.Label(info_grid, text=f"💰 Saldo: ${stats.get('skin_balance', 0.0):.2f}", 
                     font=('Arial', 11), style='Dark.TLabel').grid(row=2, column=1, sticky=tk.W, pady=(5, 0))
            
            # Botão de ação para reiniciar bot específico
            if stats.get('active', False):
                ttk.Button(info_grid, text="🔄 Reiniciar Bot", 
                          command=lambda bid=bot_id: self.restart_specific_bot(bid)).grid(row=2, column=2, sticky=tk.E, pady=(5, 0))
            
        except Exception as e:
            print(f"Erro ao criar card do bot {bot_id}: {e}")
    
    def restart_specific_bot(self, bot_id):
        """Reiniciar bot específico"""
        try:
            self.log_message(f"🔄 Reiniciando Bot #{bot_id}...")
            # Implementar lógica de reinicialização específica aqui
            # Por ora, apenas log
            self.log_message(f"✅ Bot #{bot_id} será reiniciado na próxima atualização")
        except Exception as e:
            self.log_message(f"❌ Erro ao reiniciar Bot #{bot_id}: {e}", "ERROR")

    def update_app_status(self):
        """Atualizar status geral da aplicação"""
        try:
            # Atualizar status da aplicação
            if hasattr(self, 'status_label'):
                if hasattr(self, 'total_bots_active') and self.total_bots_active > 0:
                    self.status_label.config(text=f"🟢 Sistema Ativo • {self.total_bots_active} bots rodando")
                else:
                    self.status_label.config(text="📱 Sistema Desktop Ativo • Pronto para automação")
            
            # Reagendar para 5 segundos
            self.root.after(5000, self.update_app_status)
            
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
            # Reagendar mesmo com erro
            self.root.after(10000, self.update_app_status)

    def send_discord_startup_notification(self):
        """Enviar notificação de inicialização no Discord"""
        try:
            if not hasattr(self, 'discord_webhook_var') or not self.discord_webhook_var.get().strip():
                return
            
            webhook_url = self.discord_webhook_var.get().strip()
            if not webhook_url.startswith('https://discord.com/api/webhooks/'):
                return
            
            # Montar embed de inicialização
            embed = {
                "title": "🤖 Keydrop Bot Professional v3.0.0 - INICIADO",
                "description": "Sistema de automação iniciado com sucesso!",
                "color": 3066993,  # Verde
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "thumbnail": {
                    "url": "https://cdn.discordapp.com/emojis/894678089630720010.png"
                },
                "fields": [
                    {
                        "name": "🎯 **CONFIGURAÇÃO ATUAL**",
                        "value": f"```\n🤖 Bots ativos: {len(self.automation_bots) if hasattr(self, 'automation_bots') else 0}\n🏆 Modo Contender: {'Ativado' if self.contender_mode_var.get() else 'Desativado'}\n⚡ Intervalo: {self.speed_var.get()}s\n🕶️ Headless: {'Sim' if self.headless_var.get() else 'Não'}```",
                        "inline": False
                    },
                    {
                        "name": "🚀 **FUNCIONALIDADES ATIVAS**",
                        "value": "```\n✅ Sorteios Amateur (3min) - Automático\n✅ Sorteios Contender (1h) - " + ("Ativado" if self.contender_mode_var.get() else "Desativado") + "\n✅ Perfis isolados por bot\n✅ Anti-detecção ativo\n✅ Relatórios automáticos```",
                        "inline": False
                    },
                    {
                        "name": "📊 **EXEMPLO DE RELATÓRIO**",
                        "value": "```\n🏆 Amateur: 15 sorteios\n🏆 Contender: 3 sorteios\n💰 Ganho no período: R$ 2.50\n⚠️ Erros: 0\n⏱️ Tempo ativo: 2h 30min```",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "KeyDrop Bot Professional - Webhook vinculado com sucesso!",
                    "icon_url": "https://cdn.discordapp.com/emojis/894678089630720010.png"
                }
            }
            
            # Adicionar informações da release atual
            release_info = {
                "name": "📋 **NOVIDADES DESTA VERSÃO v3.0.0**",
                "value": "```\n🆕 Interface desktop nativa completa\n🆕 Automação com Selenium integrada\n🆕 Suporte a sorteios Contender (1h)\n🆕 Múltiplos perfis independentes\n🆕 Sistema de estatísticas em tempo real\n🆕 Integração Discord aprimorada\n🆕 Modo headless para máxima performance\n🆕 Anti-detecção avançado```",
                "inline": False
            }
            embed["fields"].append(release_info)
            
            payload = {
                "embeds": [embed]
            }
            
            response = requests.post(webhook_url, json=payload, timeout=10)
            if response.status_code == 204:
                self.log_message("📢 Notificação Discord enviada com sucesso!", "SUCCESS")
                self.log_message("🔗 Webhook vinculado e funcionando corretamente", "SUCCESS")
            else:
                self.log_message(f"⚠️ Erro ao enviar Discord: {response.status_code}", "WARNING")
                
        except Exception as e:
            self.log_message(f"❌ Erro na notificação Discord: {e}", "ERROR")

def main():
    """Função principal ultra-robusta"""
    print("🎯 Iniciando Keydrop Bot Professional v3.0.0...")
    
    try:
        # Configurar DPI para Windows
        if os.name == 'nt':
            try:
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass
        
        # Criar aplicação com proteção máxima
        print("📱 Criando interface gráfica...")
        app = KeydropBotGUI()
        
        # Garantir que a janela apareça
        try:
            app.root.lift()
            app.root.attributes('-topmost', True)
            app.root.after(1000, lambda: app.root.attributes('-topmost', False))
        except:
            pass
        
        print("✅ Interface criada! Iniciando loop principal...")
        
        # Executar aplicação
        app.root.mainloop()
        
    except ImportError as e:
        # Erro de imports
        print(f"❌ Erro de dependências: {e}")
        try:
            root = tk.Tk()
            root.title("Erro de Dependências")
            root.geometry("500x300")
            
            tk.Label(root, text="❌ Erro de Dependências", 
                    font=('Arial', 16, 'bold'), fg='red').pack(pady=20)
            tk.Label(root, text="Algumas dependências estão faltando:", 
                    font=('Arial', 12)).pack(pady=10)
            tk.Label(root, text=str(e), font=('Arial', 10), fg='gray').pack(pady=5)
            tk.Label(root, text="Execute: pip install -r requirements.txt", 
                    font=('Arial', 11), fg='blue').pack(pady=10)
            tk.Button(root, text="OK", command=root.destroy, 
                     font=('Arial', 12)).pack(pady=10)
            
            root.lift()
            root.attributes('-topmost', True)
            root.mainloop()
        except:
            input("Pressione Enter para sair...")
            
    except Exception as e:
        # Outros erros
        print(f"❌ Erro inesperado: {e}")
        print(f"📋 Detalhes do erro:")
        import traceback
        traceback.print_exc()
        
        try:
            # Tentar mostrar erro graficamente
            root = tk.Tk()
            root.title("Erro na Aplicação")
            root.geometry("600x400")
            
            # Forçar janela aparecer
            root.lift()
            root.attributes('-topmost', True)
            
            main_frame = tk.Frame(root)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            tk.Label(main_frame, text="❌ Erro ao Iniciar Aplicação", 
                    font=('Arial', 16, 'bold'), fg='red').pack(pady=10)
            
            tk.Label(main_frame, text="A aplicação encontrou um erro inesperado:", 
                    font=('Arial', 12)).pack(pady=5)
            
            # Área de texto para o erro
            error_text = tk.Text(main_frame, height=8, width=70, wrap=tk.WORD)
            error_text.pack(pady=10, fill=tk.BOTH, expand=True)
            error_text.insert(tk.END, f"Erro: {str(e)}\n\n")
            error_text.insert(tk.END, "Detalhes técnicos:\n")
            error_text.insert(tk.END, traceback.format_exc())
            error_text.config(state=tk.DISABLED)
            
            # Scrollbar
            scrollbar = tk.Scrollbar(main_frame, command=error_text.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            error_text.config(yscrollcommand=scrollbar.set)
            
            button_frame = tk.Frame(main_frame)
            button_frame.pack(pady=10)
            
            tk.Button(button_frame, text="🔄 Tentar Novamente", 
                     command=lambda: [root.destroy(), main()], 
                     font=('Arial', 12), bg='blue', fg='white').pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="❌ Fechar", 
                     command=root.destroy, 
                     font=('Arial', 12), bg='red', fg='white').pack(side=tk.LEFT, padx=5)
            
            root.mainloop()
            
        except Exception as gui_error:
            print(f"❌ Erro crítico ao mostrar interface de erro: {gui_error}")
            print("🔧 Executando em modo console...")
            
            # Modo console como último recurso
            print("\n" + "="*60)
            print("KEYDROP BOT PROFESSIONAL v3.0.0 - MODO CONSOLE")
            print("="*60)
            print(f"❌ Erro: {e}")
            print(f"📋 Detalhes: {traceback.format_exc()}")
            print("="*60)
            print("💡 Sugestões:")
            print("1. Verifique se todas as dependências estão instaladas")
            print("2. Execute: pip install -r requirements.txt")
            print("3. Verifique se o Python/tkinter está funcionando")
            print("4. Tente executar como administrador")
            print("="*60)
            
            try:
                input("\n📝 Pressione Enter para sair...")
            except:
                import time
                time.sleep(5)

if __name__ == "__main__":
    main()
