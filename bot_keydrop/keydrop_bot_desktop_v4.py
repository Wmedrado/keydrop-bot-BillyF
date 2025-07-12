#!/usr/bin/env python3
"""
Keydrop Bot Professional v4.0.0 - Interface Gráfica Desktop
Aplicativo desktop nativo com automação Chrome integrada para sorteios Keydrop
Desenvolvido por William Medrado (wmedrado)

Este módulo utiliza Selenium com **undetected-chromedriver** para minimizar a
detecção automatizada. Está em nossos planos avaliar a migração para
**Playwright** para maior performance e flexibilidade no futuro.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, TclError
import threading
import os
import types
import json
import requests
import time
import logging
import traceback
from datetime import datetime
from pathlib import Path
import psutil
from PIL import Image

try:
    import pystray  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    pystray = None

# Modo debug via variável de ambiente
DEBUG_MODE = os.getenv("MODO_DEBUG") == "1"

# Configuração de logging
logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO)
logger = logging.getLogger(__name__)


def check_initial_resources() -> None:
    """Warn about missing essential files used by the GUI."""
    missing = []
    if not os.path.exists("config.json"):
        missing.append("config.json")
    if not os.path.exists("bot-icone.ico"):
        missing.append("bot-icone.ico")
    if missing:
        messagebox.showwarning(
            "Arquivos Ausentes",
            "Os seguintes arquivos est\u00e3o faltando:\n" + "\n".join(missing),
        )


# Selenium imports - Suporte Edge + Chrome + Firefox
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.edge.service import Service as EdgeService
    from selenium.webdriver.edge.options import Options as EdgeOptions
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager

    try:
        import undetected_chromedriver as uc

        UNDETECTED_AVAILABLE = True
    except ImportError:
        uc = None
        UNDETECTED_AVAILABLE = False
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from webdriver_manager.firefox import GeckoDriverManager

    SELENIUM_AVAILABLE = True
except ImportError as e:
    SELENIUM_AVAILABLE = False
    ChromeService = None
    ChromeOptions = None
    EdgeService = None
    EdgeOptions = None
    FirefoxService = None
    FirefoxOptions = None
    ChromeDriverManager = None
    EdgeChromiumDriverManager = None
    GeckoDriverManager = None
    webdriver = None
    By = None
    WebDriverWait = None
    EC = None
    print(f"Aviso: Selenium não disponível: {e}")


class KeydropBotManager:
    """Gerenciador principal de bots Keydrop"""

    def __init__(self):
        self.bots = {}  # Dicionário de bots ativos
        self.running = False
        self.config = self.load_default_config()

    def load_default_config(self):
        """Carregar configuração padrão"""
        return {
            "num_tabs": 3,
            "execution_speed": 3.0,
            "retry_attempts": 5,
            "headless_mode": False,
            "mini_window_mode": False,
            "enable_login_tabs": False,
            "discord_webhook_url": "",
            "discord_notifications": False,
            "amateur_wait_time": 180,  # 3 minutos
            "contender_wait_time": 300,  # 5 minutos
            "proxy_enabled": False,
            "proxy_host": "",
            "proxy_port": 0,
            "proxy_username": "",
            "proxy_password": "",
            "captcha_service": "",
            "captcha_api_key": "",
            "monitor_twitter": False,
            "twitter_bearer_token": "",
            "telegram_enabled": False,
            "telegram_bot_token": "",
            "telegram_chat_id": "",
            "auto_open_golden_cases": False,
            "golden_case_price": 0,
            "dom_change_timeout": 5,  # tempo máximo para aguardar mudança na página
        }

    def create_bot(self, bot_id, config):
        """Criar um novo bot"""
        bot = KeydropBot(bot_id, config)
        self.bots[bot_id] = bot
        return bot

    def start_all_bots(self):
        """Iniciar todos os bots"""
        self.running = True
        for bot in self.bots.values():
            if not bot.running:
                threading.Thread(target=bot.start, daemon=True).start()

    def stop_all_bots(self):
        """Parar todos os bots"""
        self.running = False
        for bot in self.bots.values():
            bot.stop()

    def emergency_stop(self):
        """Parada de emergência - mata todos os processos Chrome"""
        try:
            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    if "chrome" in proc.info["name"].lower():
                        psutil.Process(proc.info["pid"]).terminate()
                except Exception:
                    continue
            self.bots.clear()
        except Exception as e:
            print(f"Erro na parada de emergência: {e}")


class KeydropBot:
    """Bot individual para automação Keydrop"""

    def __init__(self, bot_id, config):
        self.bot_id = bot_id
        self.config = config
        self.logger = logger
        self.driver = None
        self.running = False
        self.stats = {
            "participacoes": 0,
            "participacoes_contender": 0,
            "erros": 0,
            "inicio": None,
            "ultima_participacao": None,
            "ultima_atividade": "Iniciando...",
        }

    def start(self):
        """Iniciar bot"""
        if not SELENIUM_AVAILABLE:
            print(f"[Bot {self.bot_id}] Selenium não disponível!")
            return

        try:
            self.running = True
            self.stats["inicio"] = datetime.now()
            self.setup_driver()
            self.run_automation_loop()
        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro ao iniciar: {e}")
            self.stats["erros"] += 1

    def setup_driver(self):
        """Configurar driver com suporte a Edge, Chrome e Firefox (ordem de prioridade)"""
        if not SELENIUM_AVAILABLE:
            raise Exception(
                "Selenium não está disponível ou não foi importado corretamente"
            )

        # Prioridade: Edge (mais leve) > Chrome > Firefox
        browser_attempts = []

        # Adicionar Edge se disponível
        if EdgeOptions and EdgeService and EdgeChromiumDriverManager and webdriver:
            try:
                browser_attempts.append(
                    (
                        "edge",
                        "Microsoft Edge",
                        EdgeOptions,
                        EdgeService,
                        EdgeChromiumDriverManager,
                        webdriver.Edge,
                    )
                )
            except AttributeError:
                pass

        # Adicionar Chrome se disponível
        if ChromeOptions and ChromeService and ChromeDriverManager and webdriver:
            try:
                chrome_driver = uc.Chrome if UNDETECTED_AVAILABLE else webdriver.Chrome
                browser_attempts.append(
                    (
                        "chrome",
                        "Google Chrome",
                        ChromeOptions,
                        ChromeService,
                        ChromeDriverManager,
                        chrome_driver,
                    )
                )
            except AttributeError:
                pass

        # Adicionar Firefox se disponível
        if FirefoxOptions and FirefoxService and GeckoDriverManager and webdriver:
            try:
                browser_attempts.append(
                    (
                        "firefox",
                        "Mozilla Firefox",
                        FirefoxOptions,
                        FirefoxService,
                        GeckoDriverManager,
                        webdriver.Firefox,
                    )
                )
            except AttributeError:
                pass

        if not browser_attempts:
            raise Exception(
                "Nenhum navegador disponível! Instale selenium e webdriver-manager"
            )

        last_errors = []

        for (
            browser_type,
            browser_name,
            OptionsClass,
            ServiceClass,
            DriverManager,
            WebDriverClass,
        ) in browser_attempts:
            try:
                print(f"[Bot {self.bot_id}] 🔄 Tentando configurar {browser_name}...")

                if not all([OptionsClass, ServiceClass, DriverManager, WebDriverClass]):
                    print(
                        f"[Bot {self.bot_id}] ⚠️ {browser_name} não disponível (imports faltando)"
                    )
                    continue

                # Configurar opções específicas do navegador
                options = OptionsClass()
                self._configure_browser_options(options, browser_type)

                # Tentar múltiplas abordagens para cada navegador
                driver_created = False

                # Abordagem 1: webdriver-manager
                try:
                    print(
                        f"[Bot {self.bot_id}] Tentando {browser_name} com webdriver-manager..."
                    )
                    if (
                        browser_type == "chrome"
                        and UNDETECTED_AVAILABLE
                        and WebDriverClass is uc.Chrome
                    ):
                        self.driver = WebDriverClass(options=options)
                    else:
                        service = ServiceClass(DriverManager().install())
                        self.driver = WebDriverClass(service=service, options=options)
                    driver_created = True
                    print(
                        f"[Bot {self.bot_id}] ✅ {browser_name} configurado com webdriver-manager"
                    )
                except Exception as e1:
                    print(f"[Bot {self.bot_id}] ❌ webdriver-manager falhou: {e1}")

                    # Abordagem 2: Driver do PATH do sistema
                    try:
                        print(
                            f"[Bot {self.bot_id}] Tentando {browser_name} do PATH do sistema..."
                        )
                        self.driver = WebDriverClass(options=options)
                        driver_created = True
                        print(
                            f"[Bot {self.bot_id}] ✅ {browser_name} configurado do PATH"
                        )
                    except Exception as e2:
                        print(f"[Bot {self.bot_id}] ❌ PATH falhou: {e2}")
                        last_errors.append(
                            f"{browser_name}: [webdriver-manager: {e1}] [PATH: {e2}]"
                        )
                        continue

                if driver_created:
                    self.browser_used = browser_name
                    print(
                        f"[Bot {self.bot_id}] 🎉 SUCESSO: {browser_name} está funcionando!"
                    )

                    # Verificar se o driver realmente funciona
                    try:
                        self.driver.get("about:blank")
                        print(f"[Bot {self.bot_id}] ✅ Teste de conectividade passou")
                        return  # Sucesso total, sair do loop
                    except Exception as e:
                        print(
                            f"[Bot {self.bot_id}] ❌ Teste de conectividade falhou: {e}"
                        )
                        self.driver.quit()
                        continue

            except Exception as e:
                print(f"[Bot {self.bot_id}] ❌ Erro geral com {browser_name}: {e}")
                last_errors.append(f"{browser_name}: {e}")
                continue

        # Se chegou aqui, todos os navegadores falharam
        error_summary = "; ".join(last_errors)
        raise Exception(
            f"❌ NENHUM NAVEGADOR FUNCIONAL ENCONTRADO!\n\nErros detalhados:\n{error_summary}\n\n💡 Soluções:\n1. Instale Microsoft Edge (recomendado)\n2. Instale Google Chrome\n3. Execute: pip install --upgrade selenium webdriver-manager"
        )

    def _configure_browser_options(self, options, browser_type):
        """Configurar opções otimizadas para cada navegador"""
        print(f"[Bot {self.bot_id}] ⚙️ Configurando opções para {browser_type}...")

        # Configurações básicas otimizadas para performance
        if browser_type in ["edge", "chrome"]:
            # Configurações específicas para navegadores baseados em Chromium
            performance_args = [
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor,TranslateUI",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-gpu-sandbox",
                "--disable-software-rasterizer",
                "--disable-background-networking",
                "--disable-default-apps",
                "--disable-extensions",
                "--disable-sync",
                "--disable-translate",
                "--disable-notifications",
                "--disable-popup-blocking",
                "--disable-prompt-on-repost",
            ]

            # Edge específico - otimizações extras
            if browser_type == "edge":
                performance_args.extend(
                    [
                        "--disable-edge-split-screen",
                        "--disable-edge-shopping-assistant",
                        "--disable-edge-enhancement",
                    ]
                )

            for arg in performance_args:
                options.add_argument(arg)

        elif browser_type == "firefox":
            # Firefox configurações básicas
            firefox_prefs = {
                "dom.webdriver.enabled": False,
                "useAutomationExtension": False,
                "general.useragent.override": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }
            for pref, value in firefox_prefs.items():
                options.set_preference(pref, value)

        # Configurar modo headless se ativado
        if self.config.get("headless_mode", False):
            options.add_argument("--headless")
            print(f"[Bot {self.bot_id}] 🔇 Modo headless ativado")

        # Configurar tamanho da janela
        window_size = (
            "400,300" if self.config.get("mini_window_mode", False) else "1024,768"
        )

        if browser_type == "firefox":
            if self.config.get("mini_window_mode", False):
                options.add_argument("--width=400")
                options.add_argument("--height=300")
            else:
                options.add_argument("--width=1024")
                options.add_argument("--height=768")
        else:
            options.add_argument(f"--window-size={window_size}")

        print(f"[Bot {self.bot_id}] 📐 Tamanho da janela: {window_size}")

        # Posicionamento da janela (só para Chromium)
        if browser_type in ["edge", "chrome"]:
            x_pos = 100 + (self.bot_id * 70)  # Espaçamento maior
            y_pos = 100 + (self.bot_id * 70)
            options.add_argument(f"--window-position={x_pos},{y_pos}")
            print(f"[Bot {self.bot_id}] 📍 Posição da janela: {x_pos},{y_pos}")

        # Configurar perfil persistente
        if browser_type in ["edge", "chrome"]:
            profile_path = f"profiles/bot_{self.bot_id}_{browser_type}"
            if not os.path.exists("profiles"):
                os.makedirs("profiles", exist_ok=True)
            options.add_argument(f"--user-data-dir={profile_path}")
            print(f"[Bot {self.bot_id}] 📁 Perfil persistente: {profile_path}")

        # Proxy configuration
        if self.config.get("proxy_enabled"):
            proxy = self._build_proxy_string()
            if proxy:
                options.add_argument(f"--proxy-server={proxy}")
                print(f"[Bot {self.bot_id}] 🔌 Proxy configurado: {proxy}")

        print(f"[Bot {self.bot_id}] ✅ Configurações aplicadas para {browser_type}")

    def run_automation_loop(self):
        """Loop principal de automação"""
        try:
            # Navegar para Keydrop
            if self.driver:
                self.driver.get("https://key-drop.com/pt/")
                if WebDriverWait:
                    try:
                        WebDriverWait(self.driver, 10).until(
                            lambda d: d.execute_script("return document.readyState")
                            == "complete"
                        )
                    except Exception:
                        pass
                else:
                    time.sleep(3)

            while self.running:
                try:
                    self.stats["ultima_atividade"] = "Procurando sorteios..."

                    # Verificar códigos no Twitter
                    codes = self.check_twitter_codes()
                    for code in codes:
                        self.send_telegram(f"Novo código encontrado: {code}")

                    # Procurar sorteios AMATEUR
                    if self.participate_in_giveaways("AMATEUR"):
                        self.stats["participacoes"] += 1
                        self.stats["ultima_participacao"] = datetime.now()
                        wait_time = self.config.get("amateur_wait_time", 180)
                        self.stats["ultima_atividade"] = (
                            f"Aguardando {wait_time}s (AMATEUR)"
                        )
                        time.sleep(wait_time)

                    # Procurar sorteios CONTENDER (se configurado)
                    if self.config.get("enable_contender", False):
                        if self.participate_in_giveaways("CONTENDER"):
                            self.stats["participacoes_contender"] += 1
                            wait_time = self.config.get("contender_wait_time", 300)
                            self.stats["ultima_atividade"] = (
                                f"Aguardando {wait_time}s (CONTENDER)"
                            )
                            time.sleep(wait_time)

                    # Abrir golden case se configurado
                    self.open_golden_case()

                    # Pequena pausa entre ciclos
                    time.sleep(self.config.get("execution_speed", 3.0))

                except Exception as e:
                    print(f"[Bot {self.bot_id}] Erro no loop: {e}")
                    self.stats["erros"] += 1
                    self.handle_error(e)

        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro crítico: {e}")
            self.stats["erros"] += 1

    def participate_in_giveaways(self, giveaway_type="AMATEUR"):
        """Participar de sorteios específicos - lógica baseada no projeto Keydrop"""
        try:
            if not self.driver:
                print(f"[Bot {self.bot_id}] Driver não disponível")
                return False

            self.stats["ultima_atividade"] = f"Procurando sorteios {giveaway_type}..."

            # Navegar para página de sorteios se não estiver
            current_url = self.driver.current_url
            if "key-drop.com" not in current_url or "/giveaways" not in current_url:
                self.driver.get("https://key-drop.com/pt/giveaways")
                if WebDriverWait:
                    try:
                        WebDriverWait(self.driver, 10).until(
                            lambda d: d.execute_script("return document.readyState")
                            == "complete"
                        )
                    except Exception:
                        pass
                else:
                    time.sleep(3)

            # Atualizar página apenas se não houver alterações recentes na DOM
            if not self.wait_for_dom_change():
                self.driver.refresh()
                if WebDriverWait:
                    try:
                        WebDriverWait(self.driver, 10).until(
                            lambda d: d.execute_script("return document.readyState")
                            == "complete"
                        )
                    except Exception:
                        pass
                else:
                    time.sleep(2)

            # Fechar possíveis popups
            self.close_popups()

            # Procurar sorteios específicos baseado no tipo
            if giveaway_type == "AMATEUR":
                return self.join_amateur_giveaways()
            elif giveaway_type == "CONTENDER":
                return self.join_contender_giveaways()

            return False

        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro ao procurar sorteios: {e}")
            self.stats["ultima_atividade"] = f"Erro: {str(e)[:50]}..."
            return False

    def join_amateur_giveaways(self):
        """Participar de sorteios AMATEUR"""
        try:
            if not self.driver or not By:
                return False

            # Seletores específicos para sorteios AMATEUR
            selectors = [
                "//button[contains(text(), 'PARTICIPAR') and ancestor::*[contains(@class, 'amateur') or contains(text(), 'AMATEUR')]]",
                "//button[contains(text(), 'JOIN') and ancestor::*[contains(@class, 'amateur') or contains(text(), 'AMATEUR')]]",
                "//div[contains(@class, 'giveaway') and contains(text(), 'AMATEUR')]//button[contains(text(), 'PARTICIPAR')]",
                "//div[contains(@class, 'giveaway') and contains(text(), 'AMATEUR')]//button[contains(text(), 'JOIN')]",
                "//button[@class='btn btn-success' and contains(text(), 'PARTICIPAR')]",
                "//button[contains(@class, 'join-btn') or contains(@class, 'participate-btn')]",
            ]

            participated = False

            for selector in selectors:
                try:
                    buttons = self.driver.find_elements(By.XPATH, selector)

                    for button in buttons:
                        try:
                            # Verificar se o botão está visível e clicável
                            if button.is_displayed() and button.is_enabled():
                                # Scroll até o elemento
                                self.driver.execute_script(
                                    "arguments[0].scrollIntoView(true);", button
                                )
                                if WebDriverWait and EC:
                                    try:
                                        WebDriverWait(self.driver, 5).until(
                                            EC.element_to_be_clickable(button)
                                        )
                                    except Exception:
                                        pass
                                else:
                                    time.sleep(0.5)

                                self.driver.execute_script(
                                    "arguments[0].click();", button
                                )
                                if WebDriverWait:
                                    try:
                                        WebDriverWait(self.driver, 5).until_not(
                                            lambda d: button.is_displayed()
                                        )
                                    except Exception:
                                        pass
                                else:
                                    time.sleep(1)

                                print(
                                    f"[Bot {self.bot_id}] ✅ Participou de sorteio AMATEUR"
                                )
                                self.stats["ultima_atividade"] = (
                                    "Participou de sorteio AMATEUR"
                                )
                                participated = True
                                break

                        except Exception as e:
                            print(
                                f"[Bot {self.bot_id}] Erro ao clicar em botão AMATEUR: {e}"
                            )
                            continue

                    if participated:
                        break

                except Exception as e:
                    print(f"[Bot {self.bot_id}] Erro com seletor AMATEUR: {e}")
                    continue

            return participated

        except Exception as e:
            traceback.print_exc()
            self.logger.error(f"[join_amateur_giveaways] Erro: {str(e)}")
            return False

    def join_contender_giveaways(self):
        """Participar de sorteios CONTENDER"""
        try:
            if not self.driver or not By:
                return False

            # Seletores específicos para sorteios CONTENDER
            selectors = [
                "//button[contains(text(), 'PARTICIPAR') and ancestor::*[contains(@class, 'contender') or contains(text(), 'CONTENDER')]]",
                "//button[contains(text(), 'JOIN') and ancestor::*[contains(@class, 'contender') or contains(text(), 'CONTENDER')]]",
                "//div[contains(@class, 'giveaway') and contains(text(), 'CONTENDER')]//button[contains(text(), 'PARTICIPAR')]",
                "//div[contains(@class, 'giveaway') and contains(text(), 'CONTENDER')]//button[contains(text(), 'JOIN')]",
            ]

            participated = False

            for selector in selectors:
                try:
                    buttons = self.driver.find_elements(By.XPATH, selector)

                    for button in buttons:
                        try:
                            if button.is_displayed() and button.is_enabled():
                                self.driver.execute_script(
                                    "arguments[0].scrollIntoView(true);", button
                                )
                                if WebDriverWait and EC:
                                    try:
                                        WebDriverWait(self.driver, 5).until(
                                            EC.element_to_be_clickable(button)
                                        )
                                    except Exception:
                                        pass
                                else:
                                    time.sleep(0.5)

                                self.driver.execute_script(
                                    "arguments[0].click();", button
                                )
                                if WebDriverWait:
                                    try:
                                        WebDriverWait(self.driver, 5).until_not(
                                            lambda d: button.is_displayed()
                                        )
                                    except Exception:
                                        pass
                                else:
                                    time.sleep(1)

                                print(
                                    f"[Bot {self.bot_id}] ✅ Participou de sorteio CONTENDER"
                                )
                                self.stats["ultima_atividade"] = (
                                    "Participou de sorteio CONTENDER"
                                )
                                participated = True
                                break

                        except Exception as e:
                            print(
                                f"[Bot {self.bot_id}] Erro ao clicar em botão CONTENDER: {e}"
                            )
                            continue

                    if participated:
                        break

                except Exception as e:
                    print(f"[Bot {self.bot_id}] Erro com seletor CONTENDER: {e}")
                    continue

            return participated

        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro em join_contender_giveaways: {e}")
            return False

    def close_popups(self):
        """Fechar popups que podem aparecer"""
        try:
            if not self.driver or not By:
                return

            # Pressionar ESC para fechar popups
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.action_chains import ActionChains

            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ESCAPE).perform()
            if WebDriverWait:
                try:
                    WebDriverWait(self.driver, 2).until(lambda d: True)
                except Exception:
                    pass
            else:
                time.sleep(0.5)

            # Procurar e fechar modais específicos
            close_selectors = [
                "//button[contains(@class, 'close')]",
                "//button[contains(@class, 'modal-close')]",
                "//span[contains(@class, 'close')]",
                "//div[contains(@class, 'modal')]//button[contains(text(), '×')]",
                "//button[@aria-label='Close']",
            ]

            for selector in close_selectors:
                try:
                    close_buttons = self.driver.find_elements(By.XPATH, selector)
                    for btn in close_buttons:
                        if btn.is_displayed():
                            btn.click()
                            if WebDriverWait:
                                try:
                                    WebDriverWait(self.driver, 2).until_not(
                                        lambda d: btn.is_displayed()
                                    )
                                except Exception:
                                    pass
                            else:
                                time.sleep(0.5)
                except Exception:
                    continue

        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro ao fechar popups: {e}")

    def wait_for_dom_change(self, selector="body", timeout=None):
        """Aguardar alterações na DOM antes de atualizar a página"""
        try:
            if not self.driver:
                return False

            if timeout is None:
                timeout = self.config.get("dom_change_timeout", 5)

            script = "return document.querySelector(arguments[0]).innerHTML"
            initial = self.driver.execute_script(script, selector)
            end_time = time.time() + timeout
            while time.time() < end_time:
                time.sleep(1)
                current = self.driver.execute_script(script, selector)
                if current != initial:
                    return True
            return False
        except Exception:
            return False

    def handle_error(self, error):
        """Lidar com erros e implementar retry"""
        try:
            if not self.driver:
                return False

            retry_count = 0
            max_retries = self.config.get("retry_attempts", 5)

            while retry_count < max_retries and self.running:
                try:
                    retry_count += 1
                    self.stats["ultima_atividade"] = (
                        f"Tentativa {retry_count}/{max_retries}"
                    )

                    # Tentar recarregar a página
                    self.driver.refresh()
                    if WebDriverWait:
                        try:
                            WebDriverWait(self.driver, 10).until(
                                lambda d: d.execute_script("return document.readyState")
                                == "complete"
                            )
                        except Exception:
                            pass
                    else:
                        time.sleep(3)

                    # Se chegou aqui, deu certo
                    self.stats["ultima_atividade"] = "Recuperado de erro"
                    return

                except Exception as e:
                    print(f"[Bot {self.bot_id}] Tentativa {retry_count} falhou: {e}")
                    if WebDriverWait:
                        try:
                            WebDriverWait(self.driver, 5).until(lambda d: True)
                        except Exception:
                            pass
                    else:
                        time.sleep(5)

            # Se esgotou tentativas, reiniciar driver
            if retry_count >= max_retries:
                print(
                    f"[Bot {self.bot_id}] Reiniciando driver após {max_retries} tentativas"
                )
                self.restart_driver()

        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro no tratamento de erro: {e}")

    def restart_driver(self):
        """Reiniciar driver Chrome"""
        try:
            if self.driver:
                self.driver.quit()
            time.sleep(2)
            self.setup_driver()
            if self.driver:
                self.driver.get("https://key-drop.com/pt/")
                self.stats["ultima_atividade"] = "Driver reiniciado"
        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro ao reiniciar driver: {e}")

    def stop(self):
        """Parar bot"""
        self.running = False
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"[Bot {self.bot_id}] Erro ao fechar driver: {e}")

    def _build_proxy_string(self):
        host = self.config.get("proxy_host")
        port = self.config.get("proxy_port")
        if not host or not port:
            return ""
        user = self.config.get("proxy_username")
        pwd = self.config.get("proxy_password")
        if user and pwd:
            return f"{user}:{pwd}@{host}:{port}"
        return f"{host}:{port}"

    def solve_captcha(self, image_path):
        service = self.config.get("captcha_service")
        api_key = self.config.get("captcha_api_key")
        if not service or not api_key:
            return None
        # Placeholder for integration with captcha solving services
        print(f"[Bot {self.bot_id}] Enviando captcha para {service}")
        return None

    def send_telegram(self, message):
        if not self.config.get("telegram_enabled"):
            return
        token = self.config.get("telegram_bot_token")
        chat_id = self.config.get("telegram_chat_id")
        if not token or not chat_id:
            return
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=60)
        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro ao enviar Telegram: {e}")

    def check_twitter_codes(self):
        if not self.config.get("monitor_twitter"):
            return []
        bearer = self.config.get("twitter_bearer_token")
        if not bearer:
            return []
        # Placeholder for Twitter API polling
        print(f"[Bot {self.bot_id}] Verificando códigos no Twitter")
        return []

    def open_golden_case(self):
        if not self.config.get("auto_open_golden_cases"):
            return
        price = self.config.get("golden_case_price", 0)
        # Placeholder for automation to open golden case
        print(f"[Bot {self.bot_id}] Abrindo golden case quando ouro >= {price}")


class KeydropBotGUI:
    """Interface gráfica principal"""

    def __init__(self):
        self.headless = False
        self.tray_icon = None
        self.setup_window()
        if os.environ.get("MOCK_TK") == "1":
            self.bot_manager = None
            self.config = None
            return
        self.bot_manager = KeydropBotManager()
        self.config = self.bot_manager.config
        if not self.headless:
            self.setup_interface()
        self.start_monitoring()
        if DEBUG_MODE:
            self.enable_debug_mode()

    def setup_window(self):
        """Configurar janela principal"""

        try:
            self.root = tk.Tk()
        except TclError:

            class DummyTk:
                def title(self, *a, **k):
                    pass

                def geometry(self, *a, **k):
                    pass

                def protocol(self, *a, **k):
                    pass

                def iconbitmap(self, *a, **k):
                    pass

                def update_idletasks(self):
                    pass

                def winfo_screenwidth(self):
                    return 1000

                def winfo_screenheight(self):
                    return 800

                def winfo_exists(self):
                    return True

                def destroy(self):
                    pass

            self.root = DummyTk()
            self.headless = True
            return

        if os.environ.get("MOCK_TK") == "1":
            self.root = types.SimpleNamespace(
                winfo_exists=lambda: True,
                protocol=lambda *a, **k: None,
                title=lambda *a, **k: None,
                geometry=lambda *a, **k: None,
                destroy=lambda: None,
                tk=None,
            )
            return
        self.root = tk.Tk()
        self.root.title("Keydrop Bot Professional v4.0.0")
        self.root.geometry("1000x800")

        self.root.bind("<Unmap>", self.on_minimize)

        # Exportar logs quando a janela for fechada
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Configurar ícone
        self.setup_icon()
        self.setup_tray_icon()

        # Centralizar janela
        self.center_window()

    def setup_icon(self):
        """Configurar ícone da aplicação"""
        try:
            icon_paths = [
                "bot-icone.ico",
                "resources/bot-icone.ico",
                "../bot-icone.ico",
            ]

            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
                    break
        except Exception as e:
            print(f"Erro ao configurar ícone: {e}")

    def center_window(self):
        """Centralizar janela na tela"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"1000x800+{x}+{y}")

    def setup_interface(self):
        """Configurar interface principal"""
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_label = tk.Label(
            header,
            text="🤖 Keydrop Bot Professional v4.0.0",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50",
        )
        title_label.pack(pady=10)

        subtitle_label = tk.Label(
            header,
            text="Desenvolvido por William Medrado (wmedrado)",
            font=("Arial", 10),
            fg="#bdc3c7",
            bg="#2c3e50",
        )
        subtitle_label.pack()

        # Notebook principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Criar abas
        self.create_control_tab()
        self.create_config_tab()
        self.create_stats_tab()
        self.create_logs_tab()
        self.create_store_tab()

        # Carregar configurações
        self.load_config()

    def create_control_tab(self):
        """Criar aba de controle"""
        control_frame = ttk.Frame(self.notebook)
        self.notebook.add(control_frame, text="🎮 Controle")

        # Frame principal de controle
        main_control = ttk.LabelFrame(
            control_frame, text="Controle Principal", padding=15
        )
        main_control.pack(fill="x", padx=10, pady=5)

        # Botões principais
        button_frame = tk.Frame(main_control)
        button_frame.pack(fill="x", pady=10)

        tk.Button(
            button_frame,
            text="🚀 Iniciar Bots",
            command=self.start_bots,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=15,
            height=2,
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="⏹️ Parar Bots",
            command=self.stop_bots,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=15,
            height=2,
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="🚨 EMERGÊNCIA",
            command=self.emergency_stop,
            font=("Arial", 12, "bold"),
            bg="#c0392b",
            fg="white",
            width=15,
            height=2,
        ).pack(side="left", padx=5)

        # Status dos bots
        status_frame = ttk.LabelFrame(control_frame, text="Status dos Bots", padding=10)
        status_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.status_tree = ttk.Treeview(
            status_frame,
            columns=("Status", "Participações", "Erros", "Última Atividade"),
            show="tree headings",
        )
        self.status_tree.heading("#0", text="Bot")
        self.status_tree.heading("Status", text="Status")
        self.status_tree.heading("Participações", text="Participações")
        self.status_tree.heading("Erros", text="Erros")
        self.status_tree.heading("Última Atividade", text="Última Atividade")

        # Scrollbar para a árvore
        scrollbar = ttk.Scrollbar(
            status_frame, orient="vertical", command=self.status_tree.yview
        )
        self.status_tree.configure(yscrollcommand=scrollbar.set)

        self.status_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_config_tab(self):
        """Criar aba de configurações"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configurações")

        # Configurações básicas
        basic_frame = ttk.LabelFrame(
            config_frame, text="Configurações Básicas", padding=10
        )
        basic_frame.pack(fill="x", padx=10, pady=5)

        # Grid para configurações
        tk.Label(basic_frame, text="Número de Guias (1-100):").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.num_tabs_var = tk.StringVar(value=str(self.config["num_tabs"]))
        tk.Entry(basic_frame, textvariable=self.num_tabs_var, width=10).grid(
            row=0, column=1, padx=5, pady=5
        )

        tk.Label(basic_frame, text="Velocidade de Execução (seg):").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.speed_var = tk.StringVar(value=str(self.config["execution_speed"]))
        tk.Entry(basic_frame, textvariable=self.speed_var, width=10).grid(
            row=1, column=1, padx=5, pady=5
        )

        tk.Label(basic_frame, text="Tentativas de Retry:").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.retry_var = tk.StringVar(value=str(self.config["retry_attempts"]))
        tk.Entry(basic_frame, textvariable=self.retry_var, width=10).grid(
            row=2, column=1, padx=5, pady=5
        )

        # Opções avançadas
        advanced_frame = ttk.LabelFrame(
            config_frame, text="Opções Avançadas", padding=10
        )
        advanced_frame.pack(fill="x", padx=10, pady=5)

        self.headless_var = tk.BooleanVar(value=self.config["headless_mode"])
        tk.Checkbutton(
            advanced_frame, text="Modo Headless (invisível)", variable=self.headless_var
        ).pack(anchor="w", pady=2)

        self.mini_window_var = tk.BooleanVar(value=self.config["mini_window_mode"])
        tk.Checkbutton(
            advanced_frame, text="Modo Mini (400x300px)", variable=self.mini_window_var
        ).pack(anchor="w", pady=2)

        self.login_tabs_var = tk.BooleanVar(value=self.config["enable_login_tabs"])
        tk.Checkbutton(
            advanced_frame,
            text="Abas de Login (Keydrop/Steam)",
            variable=self.login_tabs_var,
        ).pack(anchor="w", pady=2)

        # Discord
        discord_frame = ttk.LabelFrame(
            config_frame, text="Integração Discord", padding=10
        )
        discord_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(discord_frame, text="Webhook URL:").pack(anchor="w")
        self.discord_webhook_var = tk.StringVar(
            value=self.config["discord_webhook_url"]
        )
        tk.Entry(discord_frame, textvariable=self.discord_webhook_var, width=60).pack(
            fill="x", pady=2
        )

        self.discord_enabled_var = tk.BooleanVar(
            value=self.config["discord_notifications"]
        )
        tk.Checkbutton(
            discord_frame,
            text="Habilitar Notificações Discord",
            variable=self.discord_enabled_var,
        ).pack(anchor="w", pady=2)

        # Proxy
        proxy_frame = ttk.LabelFrame(config_frame, text="Proxy", padding=10)
        proxy_frame.pack(fill="x", padx=10, pady=5)

        self.proxy_enabled_var = tk.BooleanVar(
            value=self.config.get("proxy_enabled", False)
        )
        tk.Checkbutton(
            proxy_frame, text="Usar Proxy", variable=self.proxy_enabled_var
        ).pack(anchor="w", pady=2)

        tk.Label(proxy_frame, text="Host:").pack(anchor="w")
        self.proxy_host_var = tk.StringVar(value=self.config.get("proxy_host", ""))
        tk.Entry(proxy_frame, textvariable=self.proxy_host_var, width=40).pack(
            fill="x", pady=2
        )

        tk.Label(proxy_frame, text="Porta:").pack(anchor="w")
        self.proxy_port_var = tk.StringVar(value=str(self.config.get("proxy_port", 0)))
        tk.Entry(proxy_frame, textvariable=self.proxy_port_var, width=10).pack(
            anchor="w", pady=2
        )

        tk.Label(proxy_frame, text="Usuário:").pack(anchor="w")
        self.proxy_user_var = tk.StringVar(value=self.config.get("proxy_username", ""))
        tk.Entry(proxy_frame, textvariable=self.proxy_user_var, width=30).pack(
            fill="x", pady=2
        )

        tk.Label(proxy_frame, text="Senha:").pack(anchor="w")
        self.proxy_pass_var = tk.StringVar(value=self.config.get("proxy_password", ""))
        tk.Entry(
            proxy_frame, textvariable=self.proxy_pass_var, width=30, show="*"
        ).pack(fill="x", pady=2)

        # Captcha
        captcha_frame = ttk.LabelFrame(
            config_frame, text="Serviço de Captcha", padding=10
        )
        captcha_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(captcha_frame, text="Serviço:").pack(anchor="w")
        self.captcha_service_var = tk.StringVar(
            value=self.config.get("captcha_service", "")
        )
        tk.Entry(captcha_frame, textvariable=self.captcha_service_var, width=30).pack(
            fill="x", pady=2
        )

        tk.Label(captcha_frame, text="API Key:").pack(anchor="w")
        self.captcha_key_var = tk.StringVar(
            value=self.config.get("captcha_api_key", "")
        )
        tk.Entry(captcha_frame, textvariable=self.captcha_key_var, width=60).pack(
            fill="x", pady=2
        )

        # Telegram
        telegram_frame = ttk.LabelFrame(config_frame, text="Telegram", padding=10)
        telegram_frame.pack(fill="x", padx=10, pady=5)

        self.telegram_enabled_var = tk.BooleanVar(
            value=self.config.get("telegram_enabled", False)
        )
        tk.Checkbutton(
            telegram_frame,
            text="Enviar notificações",
            variable=self.telegram_enabled_var,
        ).pack(anchor="w", pady=2)

        tk.Label(telegram_frame, text="Bot Token:").pack(anchor="w")
        self.telegram_token_var = tk.StringVar(
            value=self.config.get("telegram_bot_token", "")
        )
        tk.Entry(telegram_frame, textvariable=self.telegram_token_var, width=60).pack(
            fill="x", pady=2
        )

        tk.Label(telegram_frame, text="Chat ID:").pack(anchor="w")
        self.telegram_chat_var = tk.StringVar(
            value=self.config.get("telegram_chat_id", "")
        )
        tk.Entry(telegram_frame, textvariable=self.telegram_chat_var, width=30).pack(
            fill="x", pady=2
        )

        # Golden Case
        golden_frame = ttk.LabelFrame(
            config_frame, text="Abertura de Golden Case", padding=10
        )
        golden_frame.pack(fill="x", padx=10, pady=5)

        self.auto_golden_var = tk.BooleanVar(
            value=self.config.get("auto_open_golden_cases", False)
        )
        tk.Checkbutton(
            golden_frame, text="Abrir automaticamente", variable=self.auto_golden_var
        ).pack(anchor="w", pady=2)

        tk.Label(golden_frame, text="Preço alvo:").pack(anchor="w")
        self.golden_price_var = tk.StringVar(
            value=str(self.config.get("golden_case_price", 0))
        )
        tk.Entry(golden_frame, textvariable=self.golden_price_var, width=10).pack(
            anchor="w", pady=2
        )

        # Twitter Codes
        twitter_frame = ttk.LabelFrame(
            config_frame, text="Monitorar Twitter", padding=10
        )
        twitter_frame.pack(fill="x", padx=10, pady=5)

        self.twitter_monitor_var = tk.BooleanVar(
            value=self.config.get("monitor_twitter", False)
        )
        tk.Checkbutton(
            twitter_frame,
            text="Obter códigos dourados",
            variable=self.twitter_monitor_var,
        ).pack(anchor="w", pady=2)

        tk.Label(twitter_frame, text="Bearer Token:").pack(anchor="w")
        self.twitter_token_var = tk.StringVar(
            value=self.config.get("twitter_bearer_token", "")
        )
        tk.Entry(twitter_frame, textvariable=self.twitter_token_var, width=60).pack(
            fill="x", pady=2
        )

        # Botões de configuração
        buttons_frame = tk.Frame(config_frame)
        buttons_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(
            buttons_frame,
            text="💾 Salvar Configurações",
            command=self.save_config,
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
        ).pack(side="left", padx=5)

        tk.Button(
            buttons_frame,
            text="🔄 Recarregar",
            command=self.load_config,
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
        ).pack(side="left", padx=5)

        tk.Button(
            buttons_frame,
            text="🧹 Limpar Cache",
            command=self.clear_cache,
            font=("Arial", 11),
            bg="#f39c12",
            fg="white",
        ).pack(side="left", padx=5)

    def create_stats_tab(self):
        """Criar aba de estatísticas"""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="📊 Estatísticas")

        # Sistema
        system_frame = ttk.LabelFrame(
            stats_frame, text="Performance do Sistema", padding=10
        )
        system_frame.pack(fill="x", padx=10, pady=5)

        self.cpu_label = tk.Label(system_frame, text="CPU: 0%", font=("Arial", 11))
        self.cpu_label.pack(anchor="w", pady=2)

        self.ram_label = tk.Label(system_frame, text="RAM: 0 MB", font=("Arial", 11))
        self.ram_label.pack(anchor="w", pady=2)

        self.disk_label = tk.Label(system_frame, text="Disco: 0 GB", font=("Arial", 11))
        self.disk_label.pack(anchor="w", pady=2)

        # Estatísticas dos bots
        bot_stats_frame = ttk.LabelFrame(
            stats_frame, text="Estatísticas dos Bots", padding=10
        )
        bot_stats_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.stats_text = scrolledtext.ScrolledText(
            bot_stats_frame, height=20, state="disabled"
        )
        self.stats_text.pack(fill="both", expand=True)

    def create_logs_tab(self):
        """Criar aba de logs"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="📝 Logs")

        # Controles
        controls_frame = tk.Frame(logs_frame)
        controls_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(
            controls_frame,
            text="🗑️ Limpar Logs",
            command=self.clear_logs,
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
        ).pack(side="left", padx=5)

        tk.Button(
            controls_frame,
            text="💾 Salvar Logs",
            command=self.save_logs,
            font=("Arial", 10),
            bg="#27ae60",
            fg="white",
        ).pack(side="left", padx=5)

        # Área de logs
        self.logs_text = scrolledtext.ScrolledText(
            logs_frame, height=25, state="disabled"
        )
        self.logs_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Configurar cores para níveis de log
        self.setup_log_tags()

    def create_store_tab(self):
        """Criar aba da loja de itens premium."""
        store_frame = ttk.Frame(self.notebook)
        self.notebook.add(store_frame, text="🛒 Loja")
        from bot_keydrop.gui.store_frame import StoreFrame

        self.store = StoreFrame(store_frame)
        self.store.pack(fill="both", expand=True, padx=5, pady=5)

    def setup_log_tags(self):
        """Configurar tags de cor para cada nível de log"""
        try:
            self.logs_text.tag_config("INFO", foreground="#3498db")
            self.logs_text.tag_config("DEBUG", foreground="#95a5a6")
            self.logs_text.tag_config("ERROR", foreground="#e74c3c")
            self.logs_text.tag_config("WARNING", foreground="#f39c12")
            self.logs_text.tag_config("SUCCESS", foreground="#27ae60")
        except Exception:
            pass

    def start_bots(self):
        """Iniciar bots"""
        try:
            if not SELENIUM_AVAILABLE:
                messagebox.showerror(
                    "Erro",
                    "Selenium não está disponível!\nInstale as dependências: pip install selenium webdriver-manager",
                )
                return

            # Salvar configurações antes de iniciar
            self.save_config()

            num_tabs = int(self.num_tabs_var.get())

            # Criar bots
            for i in range(num_tabs):
                self.bot_manager.create_bot(i, self.config)

            # Iniciar todos os bots
            self.bot_manager.start_all_bots()

            self.log_message("🚀 Bots iniciados com sucesso!", "SUCCESS")

        except Exception as e:
            self.log_message(f"❌ Erro ao iniciar bots: {e}", "ERROR")
            messagebox.showerror("Erro", f"Erro ao iniciar bots:\n{e}")

    def stop_bots(self):
        """Parar bots"""
        try:
            self.bot_manager.stop_all_bots()
            self.log_message("⏹️ Bots parados", "INFO")
        except Exception as e:
            self.log_message(f"❌ Erro ao parar bots: {e}", "ERROR")

    def emergency_stop(self):
        """Parada de emergência"""
        result = messagebox.askyesno(
            "Parada de Emergência",
            "⚠️ ATENÇÃO!\n\nIsso fechará TODAS as janelas do Chrome no sistema!\n\nContinuar?",
        )
        if result:
            try:
                self.bot_manager.emergency_stop()
                self.log_message("🚨 PARADA DE EMERGÊNCIA EXECUTADA!", "WARNING")
            except Exception as e:
                self.log_message(f"❌ Erro na parada de emergência: {e}", "ERROR")

    def save_config(self):
        """Salvar configurações"""
        try:
            self.config.update(
                {
                    "num_tabs": int(self.num_tabs_var.get()),
                    "execution_speed": float(self.speed_var.get()),
                    "retry_attempts": int(self.retry_var.get()),
                    "headless_mode": self.headless_var.get(),
                    "mini_window_mode": self.mini_window_var.get(),
                    "enable_login_tabs": self.login_tabs_var.get(),
                    "discord_webhook_url": self.discord_webhook_var.get(),
                    "discord_notifications": self.discord_enabled_var.get(),
                    "proxy_enabled": self.proxy_enabled_var.get(),
                    "proxy_host": self.proxy_host_var.get(),
                    "proxy_port": int(self.proxy_port_var.get() or 0),
                    "proxy_username": self.proxy_user_var.get(),
                    "proxy_password": self.proxy_pass_var.get(),
                    "captcha_service": self.captcha_service_var.get(),
                    "captcha_api_key": self.captcha_key_var.get(),
                    "telegram_enabled": self.telegram_enabled_var.get(),
                    "telegram_bot_token": self.telegram_token_var.get(),
                    "telegram_chat_id": self.telegram_chat_var.get(),
                    "auto_open_golden_cases": self.auto_golden_var.get(),
                    "golden_case_price": float(self.golden_price_var.get() or 0),
                    "monitor_twitter": self.twitter_monitor_var.get(),
                    "twitter_bearer_token": self.twitter_token_var.get(),
                }
            )

            # Salvar em arquivo
            with open("config.json", "w") as f:
                json.dump(self.config, f, indent=2)

            self.log_message("✅ Configurações salvas!", "SUCCESS")

        except Exception as e:
            self.log_message(f"❌ Erro ao salvar configurações: {e}", "ERROR")

    def load_config(self):
        """Carregar configurações"""
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    saved_config = json.load(f)
                if isinstance(saved_config, dict):
                    self.config.update(saved_config)
                else:
                    raise ValueError("config.json invalid format")

                # Atualizar interface
                self.num_tabs_var.set(str(self.config["num_tabs"]))
                self.speed_var.set(str(self.config["execution_speed"]))
                self.retry_var.set(str(self.config["retry_attempts"]))
                self.headless_var.set(self.config["headless_mode"])
                self.mini_window_var.set(self.config["mini_window_mode"])
                self.login_tabs_var.set(self.config["enable_login_tabs"])
                self.discord_webhook_var.set(self.config["discord_webhook_url"])
                self.discord_enabled_var.set(self.config["discord_notifications"])
                self.proxy_enabled_var.set(self.config.get("proxy_enabled", False))
                self.proxy_host_var.set(self.config.get("proxy_host", ""))
                self.proxy_port_var.set(str(self.config.get("proxy_port", 0)))
                self.proxy_user_var.set(self.config.get("proxy_username", ""))
                self.proxy_pass_var.set(self.config.get("proxy_password", ""))
                self.captcha_service_var.set(self.config.get("captcha_service", ""))
                self.captcha_key_var.set(self.config.get("captcha_api_key", ""))
                self.telegram_enabled_var.set(
                    self.config.get("telegram_enabled", False)
                )
                self.telegram_token_var.set(self.config.get("telegram_bot_token", ""))
                self.telegram_chat_var.set(self.config.get("telegram_chat_id", ""))
                self.auto_golden_var.set(
                    self.config.get("auto_open_golden_cases", False)
                )
                self.golden_price_var.set(str(self.config.get("golden_case_price", 0)))
                self.twitter_monitor_var.set(self.config.get("monitor_twitter", False))
                self.twitter_token_var.set(self.config.get("twitter_bearer_token", ""))

                self.log_message("✅ Configurações carregadas!", "SUCCESS")
            else:
                self.log_message("ℹ️ Usando configurações padrão", "INFO")

        except json.JSONDecodeError:
            self.log_message("⚠️ config.json corrompido. Usando padrão", "WARNING")
        except Exception as e:
            self.log_message(f"❌ Erro ao carregar configurações: {e}", "ERROR")

    def clear_cache(self):
        """Limpar cache"""
        try:
            # Limpar profiles dos bots
            if os.path.exists("profiles"):
                import shutil

                shutil.rmtree("profiles")
                os.makedirs("profiles")

            self.log_message("🧹 Cache limpo!", "SUCCESS")

        except Exception as e:
            self.log_message(f"❌ Erro ao limpar cache: {e}", "ERROR")

    def clear_logs(self):
        """Limpar logs"""
        self.logs_text.config(state="normal")
        self.logs_text.delete(1.0, "end")
        self.logs_text.config(state="disabled")

    def save_logs(self):
        """Salvar logs"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            )
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.logs_text.get(1.0, "end"))
                self.log_message(f"📄 Logs salvos: {filename}", "SUCCESS")
        except Exception as e:
            self.log_message(f"❌ Erro ao salvar logs: {e}", "ERROR")

    def salvar_logs_em_arquivo(self):
        """Salvar logs automaticamente ao encerrar a aplicação"""
        try:
            logs_dir = Path("logs")
            logs_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = logs_dir / f"logs_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.logs_text.get(1.0, "end"))
            self.log_message(f"📄 Logs exportados para {filename}", "SUCCESS")
        except Exception as e:
            self.log_message(f"❌ Erro ao exportar logs: {e}", "ERROR")

    def on_close(self):
        """Exportar logs e fechar a aplicação"""
        self.salvar_logs_em_arquivo()
        self.root.destroy()

    def append_log(self, text, level="INFO"):
        """Inserir texto nos logs com cores por nível"""
        try:
            self.logs_text.config(state="normal")
            self.logs_text.insert("end", text, level)
            self.logs_text.see("end")
            self.logs_text.config(state="disabled")
        except Exception:
            pass

    def log_message(self, message, level="INFO"):
        """Adicionar mensagem aos logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"

        # Console
        print(log_entry.strip())

        # Interface
        self.append_log(log_entry, level)

    # --- System tray helpers ---
    def setup_tray_icon(self):
        """Criar ícone na bandeja do sistema"""
        try:
            icon_path = "bot-icone.ico"
            if not os.path.exists(icon_path):
                icon_path = Path(__file__).resolve().parent / "bot-icone.ico"
            image = Image.open(icon_path)
        except Exception:
            image = Image.new("RGB", (64, 64), "black")

        if pystray:
            menu = pystray.Menu(
                pystray.MenuItem("Abrir Interface", self.show_window),
                pystray.MenuItem("Pausar todos os bots", self.pause_all_bots),
                pystray.MenuItem("Sair", self.exit_app),
            )
            self.tray_icon = pystray.Icon("keydropbot", image, "Keydrop Bot", menu)
        else:  # pragma: no cover - no tray in headless tests
            self.tray_icon = None

    def show_window(self, _icon=None, _item=None):
        """Restaurar janela principal"""
        if self.tray_icon:
            self.tray_icon.stop()
        if self.root.state() == "withdrawn":
            self.root.deiconify()
            self.root.after(0, self.root.focus_force)

    def hide_window(self):
        """Ocultar janela e mostrar ícone"""
        if self.tray_icon and not self.tray_icon.visible:
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
        self.root.withdraw()

    def on_minimize(self, _event=None):
        if self.root.state() == "iconic":
            self.hide_window()

    def pause_all_bots(self, _icon=None, _item=None):
        """Placeholder para pausar todos os bots"""
        self.log_message("⏸️ Pausar bots ainda não implementado", "INFO")

    def exit_app(self, _icon=None, _item=None):
        if self.tray_icon:
            self.tray_icon.stop()
        self.on_close()

    def update_system_stats(self):
        """Atualizar estatísticas do sistema"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_label.config(
                text=f"🖥️ CPU: {cpu_percent:.1f}% ({psutil.cpu_count()} núcleos)"
            )

            # RAM
            memory = psutil.virtual_memory()
            self.ram_label.config(
                text=f"💾 RAM: {memory.used // (1024*1024)} MB / {memory.total // (1024*1024)} MB ({memory.percent:.1f}%)"
            )

            # Disco
            disk = psutil.disk_usage("C:\\")
            self.disk_label.config(
                text=f"💿 Disco C: {disk.used // (1024*1024*1024)} GB / {disk.total // (1024*1024*1024)} GB ({disk.percent:.1f}%)"
            )

            # Estatísticas dos bots
            self.update_bot_stats()

        except Exception as e:
            print(f"Erro ao atualizar estatísticas: {e}")

    def update_bot_stats(self):
        """Atualizar estatísticas dos bots"""
        try:
            # Limpar árvore de status
            for item in self.status_tree.get_children():
                self.status_tree.delete(item)

            stats_info = f"""
🤖 ESTATÍSTICAS GERAIS

Total de Bots: {len(self.bot_manager.bots)}
Bots Ativos: {len([bot for bot in self.bot_manager.bots.values() if bot.running])}

"""

            # Adicionar estatísticas de cada bot
            for bot_id, bot in self.bot_manager.bots.items():
                status = "🟢 Ativo" if bot.running else "🔴 Parado"

                # Adicionar à árvore
                self.status_tree.insert(
                    "",
                    "end",
                    text=f"Bot {bot_id}",
                    values=(
                        status,
                        bot.stats["participacoes"],
                        bot.stats["erros"],
                        bot.stats["ultima_atividade"],
                    ),
                )

                # Adicionar ao texto de estatísticas
                stats_info += f"""
Bot {bot_id}:
  Status: {status}
  Participações AMATEUR: {bot.stats['participacoes']}
  Participações CONTENDER: {bot.stats.get('participacoes_contender', 0)}
  Erros: {bot.stats['erros']}
  Início: {bot.stats['inicio'].strftime('%H:%M:%S') if bot.stats['inicio'] else 'N/A'}
  Última Participação: {bot.stats['ultima_participacao'].strftime('%H:%M:%S') if bot.stats['ultima_participacao'] else 'N/A'}
  Última Atividade: {bot.stats['ultima_atividade']}
"""

            # Atualizar texto de estatísticas
            self.stats_text.config(state="normal")
            self.stats_text.delete(1.0, "end")
            self.stats_text.insert("end", stats_info)
            self.stats_text.config(state="disabled")

        except Exception as e:
            print(f"Erro ao atualizar estatísticas dos bots: {e}")

    def start_monitoring(self):
        """Iniciar monitoramento em tempo real"""

        def monitor():
            while True:
                try:
                    self.root.after(0, self.update_system_stats)
                    time.sleep(5)
                except Exception as e:
                    print(f"Erro no monitoramento: {e}")
                    time.sleep(10)

        threading.Thread(target=monitor, daemon=True).start()

    def enable_debug_mode(self):
        """Ajustar interface e falhas controladas."""
        self.root.configure(bg="#550000")
        tk.Label(
            self.root,
            text="MODO DEBUG ATIVO",
            bg="#550000",
            fg="white",
            font=("Arial", 12, "bold"),
        ).pack(fill="x")
        self.root.after(5000, self._simulate_failure)

    def _simulate_failure(self):
        logger.debug("Falha simulada em modo debug")
        raise RuntimeError("Falha simulada para testes")

    def run(self):
        """Executar aplicação"""
        self.log_message("🎉 Keydrop Bot Professional v4.0.0 iniciado!", "SUCCESS")
        self.log_message("📱 Aplicação desktop nativa funcionando", "INFO")
        self.log_message("⚙️ Configure os parâmetros na aba 'Configurações'", "INFO")
        self.log_message("🚀 Clique em 'Iniciar Bots' para começar a automação", "INFO")

        if not SELENIUM_AVAILABLE:
            self.log_message(
                "⚠️ ATENÇÃO: Selenium não disponível. Instale as dependências.",
                "WARNING",
            )

        self.root.mainloop()


def main():
    """Função principal"""
    try:
        check_initial_resources()
        # Configurar DPI para Windows
        if os.name == "nt":
            try:
                import ctypes

                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass

        # Criar e executar aplicação
        app = KeydropBotGUI()
        app.run()

    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        print(f"📋 Detalhes: {traceback.format_exc()}")

        # Interface de erro
        try:
            root = tk.Tk()
            root.title("Erro na Aplicação")
            root.geometry("600x400")

            tk.Label(
                root,
                text="❌ Erro ao Iniciar Aplicação",
                font=("Arial", 16, "bold"),
                fg="red",
            ).pack(pady=20)

            tk.Label(
                root, text="A aplicação encontrou um erro:", font=("Arial", 12)
            ).pack(pady=10)

            error_text = tk.Text(root, height=15, width=70)
            error_text.pack(pady=10, fill="both", expand=True)
            error_text.insert("end", f"Erro: {str(e)}\n\n")
            error_text.insert("end", "Detalhes técnicos:\n")
            error_text.insert("end", traceback.format_exc())

            tk.Button(
                root,
                text="❌ Fechar",
                command=root.destroy,
                font=("Arial", 12),
                bg="red",
                fg="white",
            ).pack(pady=10)

            root.mainloop()

        except Exception:
            input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
