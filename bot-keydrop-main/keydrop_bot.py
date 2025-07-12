import os
import time
import threading
import json
import subprocess
import signal
import psutil
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Importar sistema de gerenciamento de memória
try:
    from src.memory_manager import ProcessOptimizer
    MEMORY_MANAGER_AVAILABLE = True
except ImportError:
    ProcessOptimizer = None
    MEMORY_MANAGER_AVAILABLE = False

# Importar sistema de relatórios
try:
    from src.report_manager import ReportManager
    REPORT_MANAGER_AVAILABLE = True
except ImportError:
    ReportManager = None
    REPORT_MANAGER_AVAILABLE = False

class KeyDropBot:
    def __init__(self, profile_path, bot_id, headless=False, discord_webhook=None, login_mode=False, contender_mode=False, mini_window=False, max_tentativas=3):
        self.profile_path = profile_path
        self.bot_id = bot_id
        self.headless = headless
        self.login_mode = login_mode
        self.contender_mode = contender_mode
        self.mini_window = mini_window  # Nova opção para janelas pequenas
        self.max_tentativas = max_tentativas  # Máximo de tentativas para join
        self.driver = None
        self.running = False
        self.discord_webhook = discord_webhook
        self.status = "🔄 Inicializando..."
        self.fila_execucao = None  # Será configurado pelo BotManager
        self.chrome_pids = []  # PIDs dos processos Chrome relacionados a este bot
        self.driver_service = None  # Serviço do ChromeDriver
        self.wait_timeout = 30  # Timeout padrão para WebDriverWait
        self.stats = {
            'participacoes': 0,
            'participacoes_contender': 0,
            'erros': 0,
            'inicio': None,
            'ultima_participacao': None,
            'ultima_participacao_contender': None,
            'ultimo_alerta_discord': None,
            'ultima_atividade': 'Iniciando...',
            'saldo_skins': 'R$ 0,00',
            'saldo_inicial': 0.0,
            'saldo_atual': 0.0,
            'ganho_periodo': 0.0,
            'total_ganho': 0.0
        }

    def verificar_sessao(self):
        """Verifica se o driver ainda possui sessão ativa"""
        if not self.driver or not getattr(self.driver, 'session_id', None):
            self.reiniciar_driver()
            return False
        return True
    def checar_alerta_discord(self):
        """Envia alerta para o Discord se ficar 30 minutos sem participar"""
        if not self.discord_webhook:
            return
        agora = datetime.now()
        ultima = self.stats.get('ultima_participacao')
        ultimo_alerta = self.stats.get('ultimo_alerta_discord')
        if ultima is None:
            ultima = self.stats['inicio']
        if ultima is None:
            return
        minutos = (agora - ultima).total_seconds() / 60
        if minutos >= 30:
            # Só alerta se não alertou nos últimos 30 minutos
            if not ultimo_alerta or (agora - ultimo_alerta).total_seconds() > 1800:
                try:
                    from discord_notify import send_discord_notification
                    msg = f"[KeyDrop Bot] Bot {self.bot_id} está há {int(minutos)} minutos sem participar de sorteios. Verifique!"
                    send_discord_notification(self.discord_webhook, msg)
                    self.stats['ultimo_alerta_discord'] = agora
                    print(f"[Bot {self.bot_id}] Alerta enviado para o Discord!")
                except Exception as e:
                    print(f"[Bot {self.bot_id}] Falha ao enviar alerta Discord: {e}")
                    
    def _registrar_processo_chrome(self, processo_pai):
        """Registra PIDs dos processos Chrome relacionados a este bot"""
        try:
            if processo_pai and processo_pai.pid:
                self.chrome_pids.append(processo_pai.pid)
                print(f"[Bot {self.bot_id}] Processo Chrome principal registrado: PID {processo_pai.pid}")
                
                # Registrar processos filhos
                for child in processo_pai.children(recursive=True):
                    if child.pid not in self.chrome_pids:
                        self.chrome_pids.append(child.pid)
                        print(f"[Bot {self.bot_id}] Processo Chrome filho registrado: PID {child.pid}")
        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro ao registrar processos Chrome: {e}")
    
    def _encerrar_processos_chrome(self):
        """Encerra todos os processos Chrome relacionados a este bot de forma mais robusta"""
        print(f"[Bot {self.bot_id}] Iniciando encerramento robusto de processos Chrome...")
        
        # Primeiro, tentar fechar todas as guias abertas
        if self.driver:
            try:
                print(f"[Bot {self.bot_id}] Fechando todas as guias abertas...")
                # Fechar guias de forma ordenada
                self._encerrar_guias_ordenadamente()
                    
                print(f"[Bot {self.bot_id}] Encerrando driver via quit()...")
                self.driver.quit()
                print(f"[Bot {self.bot_id}] Driver encerrado com sucesso")
                
            except Exception as e:
                print(f"[Bot {self.bot_id}] Erro ao encerrar driver: {e}")
        
        # Aguardar um pouco para o encerramento natural
        time.sleep(3)
        
        # Forçar encerramento de processos registrados
        processos_encerrados = 0
        for pid in self.chrome_pids[:]:  # Cópia da lista para modificação segura
            try:
                if psutil.pid_exists(pid):
                    processo = psutil.Process(pid)
                    if processo.is_running():
                        print(f"[Bot {self.bot_id}] Forçando encerramento do processo PID {pid}")
                        # Tentar encerramento gracioso primeiro
                        processo.terminate()
                        
                        # Aguardar encerramento gracioso
                        try:
                            processo.wait(timeout=5)
                        except psutil.TimeoutExpired:
                            print(f"[Bot {self.bot_id}] Processo PID {pid} não respondeu, forçando kill")
                            processo.kill()
                            # Aguardar um pouco após kill
                            time.sleep(1)
                        
                        processos_encerrados += 1
                        
                self.chrome_pids.remove(pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError) as e:
                print(f"[Bot {self.bot_id}] Processo PID {pid} já não existe ou sem acesso: {e}")
                try:
                    self.chrome_pids.remove(pid)
                except ValueError:
                    pass
        
        # Buscar e encerrar processos Chrome órfãos relacionados ao perfil
        self._encerrar_chrome_orfaos()
        
        # Encerramento emergencial de todos os processos Chrome relacionados
        self._encerramento_emergencial()
        
        # Limpar serviço do ChromeDriver
        if self.driver_service:
            try:
                self.driver_service.stop()
                print(f"[Bot {self.bot_id}] Serviço ChromeDriver encerrado")
            except Exception as e:
                print(f"[Bot {self.bot_id}] Erro ao encerrar serviço ChromeDriver: {e}")
        
        self.chrome_pids = []
        self.driver = None
        self.driver_service = None
        
        print(f"[Bot {self.bot_id}] Encerramento robusto concluído - {processos_encerrados} processos encerrados")
    
    def _encerrar_guias_ordenadamente(self):
        """Encerra todas as guias abertas de forma ordenada com delay"""
        if not self.driver:
            return
            
        try:
            print(f"[Bot {self.bot_id}] Fechando guias de forma ordenada...")
            handles = self.driver.window_handles
            
            # Fechar todas as guias exceto a primeira, uma por vez
            for i, handle in enumerate(handles[1:], 1):
                try:
                    print(f"[Bot {self.bot_id}] Fechando guia {i}/{len(handles)-1}...")
                    self.driver.switch_to.window(handle)
                    self.driver.close()
                    
                    # Delay entre fechamentos para evitar sobrecarga
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"[Bot {self.bot_id}] Erro ao fechar guia {handle}: {e}")
                    continue
            
            # Retornar à primeira guia se ainda existir
            if handles:
                try:
                    self.driver.switch_to.window(handles[0])
                    print(f"[Bot {self.bot_id}] Retornado à guia principal")
                except Exception as e:
                    print(f"[Bot {self.bot_id}] Erro ao retornar à guia principal: {e}")
                    
        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro no fechamento ordenado de guias: {e}")

    def _encerramento_emergencial(self):
        """Encerramento emergencial de todos os processos Chrome"""
        try:
            profile_name = f"Profile-{self.bot_id}"
            processos_emergencia = 0
            
            # Primeira passada: terminate
            for processo in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if processo.info['name'] and 'chrome' in processo.info['name'].lower():
                        cmdline = processo.info['cmdline']
                        if cmdline and any(profile_name in arg for arg in cmdline):
                            proc = psutil.Process(processo.info['pid'])
                            proc.terminate()
                            processos_emergencia += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Aguardar um pouco
            time.sleep(2)
            
            # Segunda passada: kill forçado
            for processo in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if processo.info['name'] and 'chrome' in processo.info['name'].lower():
                        cmdline = processo.info['cmdline']
                        if cmdline and any(profile_name in arg for arg in cmdline):
                            proc = psutil.Process(processo.info['pid'])
                            if proc.is_running():
                                proc.kill()
                                print(f"[Bot {self.bot_id}] Processo emergencial morto: PID {processo.info['pid']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if processos_emergencia > 0:
                print(f"[Bot {self.bot_id}] {processos_emergencia} processos em encerramento emergencial")
                
        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro no encerramento emergencial: {e}")
    
    def _encerrar_chrome_orfaos(self):
        """Encerra processos Chrome órfãos relacionados ao perfil deste bot"""
        try:
            profile_name = f"Profile-{self.bot_id}"
            orfaos_encontrados = 0
            
            for processo in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if processo.info['name'] and 'chrome' in processo.info['name'].lower():
                        cmdline = processo.info['cmdline']
                        if cmdline and any(profile_name in arg for arg in cmdline):
                            print(f"[Bot {self.bot_id}] Processo Chrome órfão encontrado: PID {processo.info['pid']}")
                            proc = psutil.Process(processo.info['pid'])
                            proc.terminate()
                            
                            try:
                                proc.wait(timeout=3)
                            except psutil.TimeoutExpired:
                                proc.kill()
                                
                            orfaos_encontrados += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if orfaos_encontrados > 0:
                print(f"[Bot {self.bot_id}] {orfaos_encontrados} processos Chrome órfãos encerrados")
            else:
                print(f"[Bot {self.bot_id}] Nenhum processo Chrome órfão encontrado")
                
        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro ao buscar processos Chrome órfãos: {e}")
        
    def _obter_processo_chrome_pai(self):
        """Obtém o processo Chrome pai relacionado ao driver"""
        try:
            if self.driver and hasattr(self.driver, 'service') and self.driver.service.process:
                # Obter processo do ChromeDriver
                chromedriver_proc = psutil.Process(self.driver.service.process.pid)
                
                # Buscar processo Chrome filho
                for child in chromedriver_proc.children(recursive=True):
                    if 'chrome' in child.name().lower():
                        return child
                        
        except Exception as e:
            print(f"[Bot {self.bot_id}] Erro ao obter processo Chrome pai: {e}")
        
        return None
        
    def criar_driver(self):
        """Cria um driver do Chrome com configurações anti-detecção"""
        try:
            options = Options()
            options.add_argument(f"--user-data-dir={self.profile_path}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            
            # Configurar tamanho da janela baseado no modo
            if self.mini_window:
                options.add_argument("--window-size=200,300")
                options.add_argument("--window-position=0,0")
                print(f"[Bot {self.bot_id}] Modo mini-window ativado (200x300)")
            else:
                options.add_argument("--window-size=1200,800")
            
            # Otimizações para performance e memória
            if MEMORY_MANAGER_AVAILABLE and ProcessOptimizer:
                # Usar argumentos otimizados
                for arg in ProcessOptimizer.optimize_chrome_args():
                    if arg not in [f"--window-size={200 if self.mini_window else 1200},{300 if self.mini_window else 800}"]:
                        options.add_argument(arg)
            else:
                # Fallback para otimizações básicas
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-plugins")
                options.add_argument("--disable-images")
                options.add_argument("--disable-background-timer-throttling")
                options.add_argument("--disable-renderer-backgrounding")
                options.add_argument("--disable-backgrounding-occluded-windows")
                options.add_argument("--memory-pressure-off")
                options.add_argument("--max_old_space_size=4096")
            
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Modo headless (oculto)
            if self.headless:
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                print(f"[Bot {self.bot_id}] Modo headless ativado")
            
            # Configurar ChromeDriver para executável
            try:
                # Primeiro tenta usar o ChromeDriverManager
                self.driver_service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=self.driver_service, options=options)
                print(f"[Bot {self.bot_id}] ChromeDriver carregado via ChromeDriverManager")
            except Exception as e:
                print(f"[Bot {self.bot_id}] Erro com ChromeDriverManager: {e}")
                # Fallback: tenta usar ChromeDriver do PATH
                try:
                    self.driver_service = Service()
                    self.driver = webdriver.Chrome(service=self.driver_service, options=options)
                    print(f"[Bot {self.bot_id}] ChromeDriver carregado do PATH")
                except Exception as e2:
                    print(f"[Bot {self.bot_id}] Erro com ChromeDriver do PATH: {e2}")
                    # Último recurso: caminho absoluto comum
                    try:
                        import shutil
                        chrome_path = shutil.which("chrome") or shutil.which("google-chrome") or shutil.which("chromium")
                        if chrome_path:
                            options.binary_location = chrome_path
                        self.driver_service = Service()
                        self.driver = webdriver.Chrome(service=self.driver_service, options=options)
                        print(f"[Bot {self.bot_id}] ChromeDriver carregado com caminho absoluto")
                    except Exception as e3:
                        print(f"[Bot {self.bot_id}] Erro final: {e3}")
                        raise e3
            
            # Registrar processos Chrome após criação bem-sucedida
            self._registrar_processo_chrome(self._obter_processo_chrome_pai())
            
            # Anti-detecção
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                """
            })
            
            return True
        except Exception:
            return False
    
    def fechar_popups(self):
        """Fecha pop-ups pressionando ESC"""
        return self.fechar_popup_com_esc()
    
    def notificar(self, titulo, mensagem):
        """Log ao invés de toast para evitar spam"""
        print(f"[Bot {self.bot_id}] {titulo}: {mensagem}")
        self.stats['ultima_atividade'] = mensagem
    
    def fechar_popup_com_esc(self):
        """Pressiona ESC para fechar pop-ups"""
        if not self.verificar_sessao():
            return False

        try:
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.action_chains import ActionChains
            
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ESCAPE).perform()
            time.sleep(0.5)
            return True
        except:
            return False

    def participar_sorteio(self):
        """Lógica principal para participar de sorteios com sistema de retry avançado"""
        if not self.verificar_sessao():
            return False

        tentativa = 0
        
        while tentativa < self.max_tentativas and self.running:
            try:
                tentativa += 1
                print(f"[Bot {self.bot_id}] Tentativa {tentativa}/{self.max_tentativas} - Acessando página de sorteios...")
                
                self.driver.get("https://key-drop.com/pt/giveaways/list")
                wait = WebDriverWait(self.driver, self.wait_timeout)
                
                # Aguarda carregar a seção de sorteios
                container = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="div-active-giveaways-list-section"]'))
                )
                
                # Aguarda os cards carregarem
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="div-active-giveaways-list-single-card"]'))
                )
                
                # Encontra todos os sorteios disponíveis
                sorteios = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="div-active-giveaways-list-single-card"]')
                
                if not sorteios:
                    print(f"[Bot {self.bot_id}] Nenhum sorteio encontrado na tentativa {tentativa}")
                    if tentativa < self.max_tentativas:
                        print(f"[Bot {self.bot_id}] Aguardando 10 segundos antes da próxima tentativa...")
                        time.sleep(10)
                        continue
                    else:
                        print(f"[Bot {self.bot_id}] Todas as tentativas falharam - iniciando reinício de guia...")
                        if self._reiniciar_guia_keydrop():
                            print(f"[Bot {self.bot_id}] Guia reiniciada - tentando novamente...")
                            time.sleep(5)
                            return self.participar_sorteio()  # Recomeçar após reiniciar
                        else:
                            self.checar_alerta_discord()
                            return False
                
                # Pega o último sorteio (mais recente)
                ultimo_sorteio = sorteios[-1]
                
                # Procura o botão de participar
                try:
                    link_participar = ultimo_sorteio.find_element(By.CSS_SELECTOR, 'a[data-testid="btn-single-card-giveaway-join"]')
                    self.driver.execute_script("arguments[0].click();", link_participar)
                    print(f"[Bot {self.bot_id}] Clicou no link do sorteio")
                    
                    # Procura o botão final de participação
                    try:
                        botao_participar = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="btn-giveaway-join-the-giveaway"]'))
                        )
                        
                        # Verifica se o botão não está desabilitado
                        if not botao_participar.get_attribute("disabled"):
                            botao_participar.click()
                            
                            # Incrementar contador antes de verificar o resultado
                            self.stats['participacoes'] += 1
                            self.stats['ultima_participacao'] = datetime.now()
                            self.stats['ultima_atividade'] = f'Participou de sorteio AMATEUR ({self.stats["participacoes"]})'
                            
                            print(f"[Bot {self.bot_id}] ✅ Participou do sorteio AMATEUR! Total: {self.stats['participacoes']}")
                            self.notificar("KeyDrop Bot", f"Bot {self.bot_id} participou de um sorteio AMATEUR!")
                            
                            # Pressiona ESC para fechar qualquer pop-up
                            time.sleep(1)
                            self.fechar_popup_com_esc()
                            return True
                        else:
                            # Verifica o texto do botão para saber o status
                            try:
                                texto_botao = botao_participar.find_element(By.TAG_NAME, "span").text
                                if "JÁ ADERIU" in texto_botao:
                                    print(f"[Bot {self.bot_id}] Já participou deste sorteio")
                                    self.stats['ultima_participacao'] = datetime.now()
                                    return True
                                elif ":" in texto_botao:  # Tempo de espera
                                    print(f"[Bot {self.bot_id}] Deve aguardar para participar novamente")
                                    self.checar_alerta_discord()
                                    return False
                            except:
                                pass
                            
                            print(f"[Bot {self.bot_id}] Botão de participar desabilitado na tentativa {tentativa}")
                            if tentativa < self.max_tentativas:
                                print(f"[Bot {self.bot_id}] Aguardando 10 segundos antes da próxima tentativa...")
                                time.sleep(10)
                                continue
                            else:
                                print(f"[Bot {self.bot_id}] Tentativas esgotadas - reiniciando guia...")
                                if self._reiniciar_guia_keydrop():
                                    print(f"[Bot {self.bot_id}] Guia reiniciada - tentando novamente...")
                                    time.sleep(5)
                                    return self.participar_sorteio()  # Recomeçar após reiniciar
                                else:
                                    self.checar_alerta_discord()
                                    return False
                                
                    except Exception as e:
                        print(f"[Bot {self.bot_id}] Erro ao encontrar botão de participar na tentativa {tentativa}: {e}")
                        if tentativa < self.max_tentativas:
                            print(f"[Bot {self.bot_id}] Aguardando 10 segundos antes da próxima tentativa...")
                            time.sleep(10)
                            continue
                        else:
                            print(f"[Bot {self.bot_id}] Tentativas esgotadas - reiniciando guia...")
                            if self._reiniciar_guia_keydrop():
                                print(f"[Bot {self.bot_id}] Guia reiniciada - tentando novamente...")
                                time.sleep(5)
                                return self.participar_sorteio()  # Recomeçar após reiniciar
                            else:
                                self.checar_alerta_discord()
                                return False
                            
                except Exception as e:
                    print(f"[Bot {self.bot_id}] Erro ao encontrar link do sorteio na tentativa {tentativa}: {e}")
                    if tentativa < self.max_tentativas:
                        print(f"[Bot {self.bot_id}] Aguardando 10 segundos antes da próxima tentativa...")
                        time.sleep(10)
                        continue
                    else:
                        print(f"[Bot {self.bot_id}] Tentativas esgotadas - reiniciando guia...")
                        if self._reiniciar_guia_keydrop():
                            print(f"[Bot {self.bot_id}] Guia reiniciada - tentando novamente...")
                            time.sleep(5)
                            return self.participar_sorteio()  # Recomeçar após reiniciar
                        else:
                            self.checar_alerta_discord()
                            return False
                        
            except Exception as e:
                print(f"[Bot {self.bot_id}] Erro geral na tentativa {tentativa}: {e}")
                self.stats['erros'] += 1
                if tentativa < self.max_tentativas:
                    print(f"[Bot {self.bot_id}] Aguardando 10 segundos antes da próxima tentativa...")
                    time.sleep(10)
                    continue
                else:
                    print(f"[Bot {self.bot_id}] Tentativas esgotadas - reiniciando guia...")
                    if self._reiniciar_guia_keydrop():
                        print(f"[Bot {self.bot_id}] Guia reiniciada - tentando novamente...")
                        time.sleep(5)
                        return self.participar_sorteio()  # Recomeçar após reiniciar
                    else:
                        self.checar_alerta_discord()
                        return False
    
    def participar_sorteio_contender(self):
        """Participa de sorteios CONTENDER (1 hora) com sistema de retry avançado"""
        if not self.verificar_sessao():
            return False

        tentativa = 0
        
        while tentativa < self.max_tentativas and self.running:
            try:
                tentativa += 1
                print(f"[Bot {self.bot_id}] Tentativa {tentativa}/{self.max_tentativas} - Procurando sorteios CONTENDER...")
                
                # Verifica se deve participar (1 hora desde a última participação)
                agora = datetime.now()
                ultima_contender = self.stats.get('ultima_participacao_contender')
                
                if ultima_contender:
                    minutos_desde_ultima = (agora - ultima_contender).total_seconds() / 60
                    if minutos_desde_ultima < 60:  # 1 hora
                        print(f"[Bot {self.bot_id}] Aguardando para próximo sorteio CONTENDER (faltam {60 - minutos_desde_ultima:.1f} min)")
                        return False
                
                # Acessa a página de sorteios
                self.driver.get("https://key-drop.com/pt/giveaways/list")
                wait = WebDriverWait(self.driver, self.wait_timeout)
                
                # Aguarda carregar a seção de sorteios
                container = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="div-active-giveaways-list-section"]'))
                )
                
                # Aguarda os cards carregarem
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="div-active-giveaways-list-single-card"]'))
                )
                
                # Encontra todos os sorteios disponíveis
                sorteios = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="div-active-giveaways-list-single-card"]')
                
                if not sorteios:
                    print(f"[Bot {self.bot_id}] Nenhum sorteio encontrado na tentativa {tentativa}")
                    if tentativa < self.max_tentativas:
                        print(f"[Bot {self.bot_id}] Aguardando 10 segundos antes da próxima tentativa...")
                        time.sleep(10)
                        continue
                    else:
                        print(f"[Bot {self.bot_id}] Tentativas esgotadas - reiniciando guia...")
                        if self._reiniciar_guia_keydrop():
                            print(f"[Bot {self.bot_id}] Guia reiniciada - tentando novamente...")
                            time.sleep(5)
                            return self.participar_sorteio_contender()  # Recomeçar após reiniciar
                        else:
                            return False
                
                # Baseado no exemplo-bot: o último item da lista é sempre o mais recente
                ultimo_sorteio = sorteios[-1]
                
                # Verifica se é um sorteio CONTENDER - busca indicadores específicos
                texto_sorteio = ultimo_sorteio.text.upper()
                
                # Indicadores de sorteio CONTENDER: "1h", "1 hora", "CONTENDER", ou duração específica
                contender_indicators = ['1H', '1 HORA', 'CONTENDER', 'HORA', 'HOURLY']
                is_contender = any(indicator in texto_sorteio for indicator in contender_indicators)
                
                if not is_contender:
                    print(f"[Bot {self.bot_id}] Último sorteio não é CONTENDER na tentativa {tentativa}")
                    if tentativa < self.max_tentativas:
                        print(f"[Bot {self.bot_id}] Aguardando 10 segundos antes da próxima tentativa...")
                        time.sleep(10)
                        continue
                    else:
                        print(f"[Bot {self.bot_id}] Tentativas esgotadas - reiniciando guia...")
                        if self._reiniciar_guia_keydrop():
                            print(f"[Bot {self.bot_id}] Guia reiniciada - tentando novamente...")
                            time.sleep(5)
                            return self.participar_sorteio_contender()  # Recomeçar após reiniciar
                        else:
                            return False
                
                print(f"[Bot {self.bot_id}] Sorteio CONTENDER encontrado!")
                
                # Procura o botão de participar
                try:
                    link_participar = ultimo_sorteio.find_element(By.CSS_SELECTOR, 'a[data-testid="btn-single-card-giveaway-join"]')
                    self.driver.execute_script("arguments[0].click();", link_participar)
                    print(f"[Bot {self.bot_id}] Clicou no link do sorteio CONTENDER")
                    
                    # Procura o botão final de participação
                    try:
                        botao_participar = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="btn-giveaway-join-the-giveaway"]'))
                        )
                        
                        # Verifica se o botão não está desabilitado
                        if not botao_participar.get_attribute("disabled"):
                            botao_participar.click()
                            
                            # Incrementar contador
                            self.stats['participacoes_contender'] += 1
                            self.stats['ultima_participacao_contender'] = datetime.now()
                            self.stats['ultima_atividade'] = f'Participou de sorteio CONTENDER ({self.stats["participacoes_contender"]})'
                            
                            print(f"[Bot {self.bot_id}] ✅ Participou do sorteio CONTENDER! Total: {self.stats['participacoes_contender']}")
                            self.notificar("KeyDrop Bot", f"Bot {self.bot_id} participou de um sorteio CONTENDER!")
                            
                            # Pressiona ESC para fechar qualquer pop-up
                            time.sleep(1)
                            self.fechar_popup_com_esc()
                            return True
                        else:
                            # Verifica o texto do botão para saber o status
                            try:
                                texto_botao = botao_participar.find_element(By.TAG_NAME, "span").text
                                if "JÁ ADERIU" in texto_botao:
                                    print(f"[Bot {self.bot_id}] Já participou deste sorteio CONTENDER")
                                    self.stats['ultima_participacao_contender'] = datetime.now()
                                    return True
                                elif ":" in texto_botao:  # Tempo de espera
                                    print(f"[Bot {self.bot_id}] Deve aguardar para participar novamente")
                                    return False
                            except:
                                pass
                            
                            print(f"[Bot {self.bot_id}] Botão de participar desabilitado na tentativa {tentativa}")
                            if tentativa < self.max_tentativas:
                                print(f"[Bot {self.bot_id}] Aguardando 10 segundos antes da próxima tentativa...")
                                time.sleep(10)
                                continue
                            else:
                                print(f"[Bot {self.bot_id}] Tentativas esgotadas - reiniciando guia...")
                                if self._reiniciar_guia_keydrop():
                                    print(f"[Bot {self.bot_id}] Guia reiniciada - tentando novamente...")
                                    time.sleep(5)
                                    return self.participar_sorteio_contender()  # Recomeçar após reiniciar
                                else:
                                    return False
                                
                    except Exception as e:
                        print(f"[Bot {self.bot_id}] Erro ao encontrar botão de participar na tentativa {tentativa}: {e}")
                        if tentativa < self.max_tentativas:
                            print(f"[Bot {self.bot_id}] Aguardando 10 segundos antes da próxima tentativa...")
                            time.sleep(10)
                            continue
                        else:
                            print(f"[Bot {self.bot_id}] Tentativas esgotadas - reiniciando guia...")
                            if self._reiniciar_guia_keydrop():
                                print(f"[Bot {self.bot_id}] Guia reiniciada - tentando novamente...")
                                time.sleep(5)
                                return self.participar_sorteio_contender()  # Recomeçar após reiniciar
                            else:
                                return False
                            
                except Exception as e:
                    print(f"[Bot {self.bot_id}] Erro ao encontrar link do sorteio na tentativa {tentativa}: {e}")
                    if tentativa < self.max_tentativas:
                        print(f"[Bot {self.bot_id}] Aguardando 10 segundos antes da próxima tentativa...")
                        time.sleep(10)
                        continue
                    else:
                        print(f"[Bot {self.bot_id}] Tentativas esgotadas - reiniciando guia...")
                        if self._reiniciar_guia_keydrop():
                            print(f"[Bot {self.bot_id}] Guia reiniciada - tentando novamente...")
                            time.sleep(5)
                            return self.participar_sorteio_contender()  # Recomeçar após reiniciar
                        else:
                            return False
                        
            except Exception as e:
                print(f"[Bot {self.bot_id}] Erro geral na tentativa {tentativa}: {e}")
                self.stats['erros'] += 1
                if tentativa < self.max_tentativas:
                    print(f"[Bot {self.bot_id}] Aguardando 10 segundos antes da próxima tentativa...")
                    time.sleep(10)
                    continue
                else:
                    print(f"[Bot {self.bot_id}] Tentativas esgotadas - reiniciando guia...")
                    if self._reiniciar_guia_keydrop():
                        print(f"[Bot {self.bot_id}] Guia reiniciada - tentando novamente...")
                        time.sleep(5)
                        return self.participar_sorteio_contender()  # Recomeçar após reiniciar
                    else:
                        return False
        
        # Se chegou aqui, todas as tentativas falharam
        print(f"[Bot {self.bot_id}] Todas as {self.max_tentativas} tentativas falharam")
        self.checar_alerta_discord()
        return False
    
    def executar_ciclo(self, intervalo_segundos=180):
        """Executa o ciclo principal do bot usando fila de execução"""
        if not self.criar_driver():
            self.status = "❌ Erro ao criar driver"
            return
        
        try:
            # Decide qual página abrir baseado no modo
            if self.login_mode:
                self.driver.get("https://steamcommunity.com/login/home/")
                self.status = "🔐 Aguardando login..."
                print(f"[Bot {self.bot_id}] Modo login ativado - Aguardando login na Steam...")
            else:
                self.driver.get("https://key-drop.com/pt/giveaways/list")
                self.status = "⏳ Aguardando login..."
                print(f"[Bot {self.bot_id}] Aguardando login manual...")
            
            self.stats['inicio'] = datetime.now()

            while self.running:
                try:
                    if not self.verificar_sessao():
                        continue

                    # No modo login, não executa automação
                    if self.login_mode:
                        self.status = "🔐 Modo login ativo"
                        time.sleep(10)
                        continue
                    
                    # Aguarda sua vez na fila de execução
                    if self.fila_execucao:
                        print(f"[Bot {self.bot_id}] Aguardando vez na fila de execução...")
                        self.status = "⏳ Aguardando vez na fila..."
                        
                        # Tenta adquirir o lock (bloqueia até conseguir)
                        with self.fila_execucao:
                            print(f"[Bot {self.bot_id}] Iniciando execução na fila")
                            self.status = "🔄 Executando na fila..."
                            
                            # Marca o início do ciclo para logs
                            ciclo_inicio = datetime.now()
                            
                            # Prioridade 1: Sorteios normais
                            self.status = "🔄 Participando de sorteios normais..."
                            participou_normal = self.participar_sorteio()
                            
                            # Prioridade 2: Sorteios CONTENDER (se modo ativado)
                            participou_contender = False
                            if self.contender_mode:
                                self.status = "🏆 Verificando sorteios CONTENDER..."
                                participou_contender = self.participar_sorteio_contender()
                            
                            # Atualizar saldo
                            self.atualizar_saldo_periodicamente()
                            
                            # Status baseado nos resultados
                            if participou_normal and participou_contender:
                                self.status = "✅ Participou em sorteios normais e CONTENDER!"
                            elif participou_normal:
                                self.status = "✅ Participou em sorteios normais!"
                            elif participou_contender:
                                self.status = "🏆 Participou em sorteio CONTENDER!"
                            else:
                                self.status = "⏳ Nenhum sorteio disponível"
                            
                            # Log detalhado com tempo de execução
                            tempo_execucao = (datetime.now() - ciclo_inicio).total_seconds()
                            print(f"[Bot {self.bot_id}] Execução concluída em {tempo_execucao:.1f}s - Normal: {participou_normal}, CONTENDER: {participou_contender}")
                            
                            # Atualizar saldo novamente após participação
                            self.atualizar_saldo_periodicamente()
                            
                            print(f"[Bot {self.bot_id}] Liberando fila de execução")
                    
                    else:
                        # Fallback se não há fila (modo antigo)
                        ciclo_inicio = datetime.now()
                        
                        # Prioridade 1: Sorteios normais
                        self.status = "🔄 Participando de sorteios normais..."
                        participou_normal = self.participar_sorteio()
                        
                        # Prioridade 2: Sorteios CONTENDER (se modo ativado)
                        participou_contender = False
                        if self.contender_mode:
                            self.status = "🏆 Verificando sorteios CONTENDER..."
                            participou_contender = self.participar_sorteio_contender()
                        
                        # Atualizar saldo
                        self.atualizar_saldo_periodicamente()
                        
                        # Status e logs
                        if participou_normal and participou_contender:
                            self.status = "✅ Participou em sorteios normais e CONTENDER!"
                        elif participou_normal:
                            self.status = "✅ Participou em sorteios normais!"
                        elif participou_contender:
                            self.status = "🏆 Participou em sorteio CONTENDER!"
                        else:
                            self.status = "⏳ Nenhum sorteio disponível"
                        
                        tempo_execucao = (datetime.now() - ciclo_inicio).total_seconds()
                        print(f"[Bot {self.bot_id}] Ciclo concluído em {tempo_execucao:.1f}s - Normal: {participou_normal}, CONTENDER: {participou_contender}")
                    
                    # Aguarda o intervalo configurado
                    print(f"[Bot {self.bot_id}] Aguardando {intervalo_segundos}s...")
                    self.status = f"⏳ Aguardando {intervalo_segundos}s..."
                    for _ in range(intervalo_segundos):
                        if not self.running:
                            break
                        time.sleep(1)
                        
                except Exception as e:
                    self.stats['erros'] += 1
                    self.status = f"⚠️ Erro: {str(e)[:50]}..."
                    print(f"[Bot {self.bot_id}] Erro: {e}")
                    time.sleep(30)
                    
        except Exception as e:
            self.status = f"❌ Erro crítico: {str(e)[:50]}..."
            print(f"[Bot {self.bot_id}] Erro crítico: {e}")
        finally:
            self.parar()
    
    def iniciar(self, intervalo_segundos=180):
        """Inicia o bot em uma thread separada"""
        self.running = True
        thread = threading.Thread(target=self.executar_ciclo, args=(intervalo_segundos,), daemon=True)
        thread.start()
        return thread
    
    def parar(self):
        """Para o bot e fecha todos os processos Chrome de forma eficiente"""
        print(f"[Bot {self.bot_id}] Iniciando procedimento de parada...")
        self.running = False
        self.status = "⏹️ Parando..."
        
        # Encerrar todos os processos Chrome
        self._encerrar_processos_chrome()
        
        self.status = "⏹️ Parado"
        print(f"[Bot {self.bot_id}] Parado com sucesso")
    
    def reiniciar_driver(self):
        """Reinicia o driver do bot"""
        print(f"[Bot {self.bot_id}] Reiniciando driver...")
        self.status = "🔄 Reiniciando driver..."
        
        # Fecha driver atual com limpeza completa
        self._encerrar_processos_chrome()
        
        # Aguardar um pouco para limpeza completa
        time.sleep(2)
        
        # Cria novo driver
        if self.criar_driver():
            if self.login_mode:
                self.driver.get("https://steamcommunity.com/login/home/")
                self.status = "🔐 Aguardando login..."
            else:
                self.driver.get("https://key-drop.com/pt/giveaways/list")
                self.status = "⏳ Aguardando login..."
            print(f"[Bot {self.bot_id}] Driver reiniciado com sucesso!")
            return True
        else:
            self.status = "❌ Erro ao reiniciar driver"
            print(f"[Bot {self.bot_id}] Erro ao reiniciar driver!")
            return False
    
    def obter_stats(self):
        """Retorna estatísticas do bot formatadas para a interface"""
        stats = self.stats.copy()
        
        # Mapear chaves para compatibilidade com a interface
        stats_formatadas = {
            'amateur': stats.get('participacoes', 0),
            'contender': stats.get('participacoes_contender', 0),
            'erros': stats.get('erros', 0),
            'saldo': stats.get('saldo_atual', 0.0),
            'ganho': stats.get('ganho_periodo', 0.0),
            'tempo_ativo': stats.get('inicio'),
            'ultima_participacao': stats.get('ultima_participacao'),
            'ultima_participacao_contender': stats.get('ultima_participacao_contender'),
            'ultima_atividade': stats.get('ultima_atividade', 'Aguardando...'),
            'saldo_skins': stats.get('saldo_skins', 'R$ 0,00'),
            'status': self.status,
            'pausado': False,  # Por enquanto sempre False, pode ser implementado depois
            'inicio': stats.get('inicio')
        }
        
        # Debug - imprimir estatísticas quando solicitado
        if stats_formatadas['amateur'] > 0 or stats_formatadas['contender'] > 0:
            print(f"[Debug] Bot {self.bot_id} obter_stats() - AMATEUR: {stats_formatadas['amateur']}, CONTENDER: {stats_formatadas['contender']}")
        
        return stats_formatadas

    def fechar_popup_navy_button(self):
        """Método simplificado - apenas pressiona ESC"""
        return self.fechar_popup_com_esc()
    
    def obter_saldo_skins(self):
        """Obtém o saldo de skins da conta"""
        if not self.verificar_sessao():
            return self.stats.get('saldo_skins', 'R$ 0,00')

        try:
            # Procurar pelo elemento do saldo
            saldo_element = self.driver.find_element(
                By.CSS_SELECTOR, 
                '[data-testid="header-quick-sell-account-balance"]'
            )
            
            # Obter o HTML interno para processar corretamente
            saldo_html = saldo_element.get_attribute('innerHTML')
            
            if saldo_html:
                # Extrair apenas o texto, removendo &nbsp; e formatando
                saldo_text = saldo_html.replace('&nbsp;', ' ').strip()
                
                # Extrair valor numérico para cálculos
                valor_numerico = 0.0
                try:
                    # Procurar por números no texto
                    import re
                    match = re.search(r'(\d+[,\.]\d+)', saldo_text)
                    if match:
                        valor_str = match.group(1).replace(',', '.')
                        valor_numerico = float(valor_str)
                except:
                    pass
                
                # Converter para formato brasileiro (R$ X,XX)
                if 'R$' in saldo_text:
                    # Já está no formato correto
                    saldo_formatado = saldo_text
                else:
                    # Assumir que está no formato "X,XX R$" e converter
                    partes = saldo_text.split()
                    if len(partes) >= 2:
                        valor = partes[0]
                        moeda = partes[1]
                        saldo_formatado = f"R$ {valor}"
                    else:
                        saldo_formatado = saldo_text
                
                # Calcular ganho do período
                saldo_anterior = self.stats.get('saldo_atual', 0.0)
                if saldo_anterior > 0:
                    ganho_atual = valor_numerico - saldo_anterior
                    if ganho_atual > 0:
                        self.stats['ganho_periodo'] += ganho_atual
                        self.stats['total_ganho'] += ganho_atual
                
                # Atualizar valores
                self.stats['saldo_skins'] = saldo_formatado
                self.stats['saldo_atual'] = valor_numerico
                
                # Definir saldo inicial se não foi definido
                if self.stats.get('saldo_inicial', 0.0) == 0.0:
                    self.stats['saldo_inicial'] = valor_numerico
                
                print(f"[Bot {self.bot_id}] Saldo atualizado: {saldo_formatado}")
                return saldo_formatado
            else:
                self.stats['saldo_skins'] = 'R$ 0,00'
                return 'R$ 0,00'
                
        except Exception as e:
            # Se não conseguir encontrar o elemento, manter valor atual
            print(f"[Bot {self.bot_id}] Erro ao obter saldo: {e}")
            return self.stats.get('saldo_skins', 'R$ 0,00')
    
    def limpar_cache_navegador(self):
        """Limpa cache do navegador sem perder login"""
        if not self.verificar_sessao():
            return False

        try:
            print(f"[Bot {self.bot_id}] Iniciando limpeza de cache...")
            self.status = "🧹 Limpando cache..."
            
            # Abre nova aba para executar comandos
            self.driver.execute_script("window.open('about:blank', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            # Limpa diferentes tipos de dados via JavaScript
            comandos_limpeza = [
                # Limpa localStorage (exceto dados de login)
                """
                for(let i = localStorage.length - 1; i >= 0; i--) {
                    const key = localStorage.key(i);
                    if(key && !key.includes('login') && !key.includes('auth') && !key.includes('session')) {
                        localStorage.removeItem(key);
                    }
                }
                """,
                
                # Limpa sessionStorage (exceto dados de login)
                """
                for(let i = sessionStorage.length - 1; i >= 0; i--) {
                    const key = sessionStorage.key(i);
                    if(key && !key.includes('login') && !key.includes('auth') && !key.includes('session')) {
                        sessionStorage.removeItem(key);
                    }
                }
                """,
                
                # Limpa cache do navegador via DevTools
                "window.location.reload(true);",
            ]
            
            for comando in comandos_limpeza:
                try:
                    self.driver.execute_script(comando)
                    time.sleep(0.5)
                except Exception as e:
                    print(f"[Bot {self.bot_id}] Erro em comando de limpeza: {e}")
            
            # Fecha a aba temporária
            self.driver.close()
            
            # Volta para a aba original
            if len(self.driver.window_handles) > 0:
                self.driver.switch_to.window(self.driver.window_handles[0])
            
            # Executa comando de limpeza mais profundo via DevTools
            try:
                self.driver.execute_cdp_cmd('Network.clearBrowserCache', {})
                self.driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
                print(f"[Bot {self.bot_id}] Cache do navegador limpo via DevTools")
            except Exception as e:
                print(f"[Bot {self.bot_id}] Limpeza via DevTools falhou: {e}")
            
            # Atualiza a página atual
            self.driver.refresh()
            time.sleep(3)
            
            self.status = "✅ Cache limpo com sucesso!"
            print(f"[Bot {self.bot_id}] Cache limpo com sucesso!")
            return True
            
        except Exception as e:
            self.status = "❌ Erro ao limpar cache"
            print(f"[Bot {self.bot_id}] Erro ao limpar cache: {e}")
            return False

    def atualizar_saldo_periodicamente(self):
        """Atualiza o saldo periodicamente durante a execução"""
        try:
            if not self.login_mode and self.verificar_sessao():
                # Só atualizar se não estiver em modo login
                self.obter_saldo_skins()
        except Exception:
            pass

class BotManager:
    def __init__(self):
        self.bots = []
        self.base_path = os.path.join(os.getcwd(), "profiles")
        self.config_file = "bot_config.json"
        self.discord_webhook = None
        self.report_manager = None
        self.telegram_bot = None
        
    def carregar_config(self):
        """Carrega configurações salvas"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {
            'num_bots': 2,
            'intervalo_sorteios': 180,
            'intervalo_tabs': 2,
            'headless': False,
            'contender_mode': False,
            'mini_window': False,
            'max_tentativas': 3,
            'discord_webhook': '',
            'discord_report_hours': 12,
            'telegram_token': '',
            'velocidade_navegacao': 5
        }
    
    def salvar_config(self, config):
        """Salva configurações"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass
    
    def criar_bots(self, num_bots, headless=False, discord_webhook=None, login_mode=False, contender_mode=False, mini_window=False, max_tentativas=3):
        """Cria os bots necessários"""
        self.discord_webhook = discord_webhook
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        for i in range(num_bots):
            profile_path = os.path.join(self.base_path, f"Profile-{i+1}")
            if not os.path.exists(profile_path):
                os.makedirs(profile_path)
            bot = KeyDropBot(profile_path, i+1, headless, discord_webhook, login_mode, contender_mode, mini_window, max_tentativas)
            self.bots.append(bot)
        
        # Inicializar sistema de relatórios
        self.init_report_system()
    
    def init_report_system(self):
        """Inicializa sistema de relatórios"""
        try:
            config = self.carregar_config()
            
            # Inicializar gerenciador de relatórios
            from src.report_manager import init_report_manager
            self.report_manager = init_report_manager(self)
            
            # Configurar sistema de relatórios
            if self.report_manager:
                self.report_manager.update_config(config)
                self.report_manager.start()
                print("📊 Sistema de relatórios iniciado")
            
            # Inicializar bot do Telegram
            telegram_token = config.get('telegram_token', '').strip()
            if telegram_token:
                from src.telegram_integration import init_telegram_bot
                self.telegram_bot = init_telegram_bot(telegram_token, self)
                print("🤖 Bot do Telegram iniciado")
                
        except Exception as e:
            print(f"❌ Erro ao inicializar sistema de relatórios: {e}")
    
    def stop_report_system(self):
        """Para sistema de relatórios"""
        try:
            if self.report_manager:
                self.report_manager.stop()
                print("📊 Sistema de relatórios parado")
            
            if self.telegram_bot:
                self.telegram_bot.stop()
                print("🤖 Bot do Telegram parado")
                
        except Exception as e:
            print(f"❌ Erro ao parar sistema de relatórios: {e}")
    
    def notify_bot_started(self):
        """Notifica que bots foram iniciados"""
        try:
            if self.telegram_bot:
                self.telegram_bot.notify_bot_started(len(self.bots))
            
            if self.discord_webhook:
                from discord_notify import notify_bot_started
                notify_bot_started(self.discord_webhook, len(self.bots))
                
        except Exception as e:
            print(f"❌ Erro ao notificar início: {e}")
    
    def notify_bot_stopped(self, reason="Manual"):
        """Notifica que bots foram parados"""
        try:
            if self.telegram_bot:
                self.telegram_bot.notify_bot_stopped(reason)
            
            if self.discord_webhook:
                from discord_notify import notify_bot_stopped
                notify_bot_stopped(self.discord_webhook, reason)
                
        except Exception as e:
            print(f"❌ Erro ao notificar parada: {e}")
    
    def notify_error(self, error_msg, bot_id=None):
        """Notifica erro no sistema"""
        try:
            if self.telegram_bot:
                self.telegram_bot.notify_error_occurred(error_msg, bot_id)
            
            if self.discord_webhook:
                from discord_notify import notify_bot_error
                notify_bot_error(self.discord_webhook, error_msg)
                
        except Exception as e:
            print(f"❌ Erro ao notificar erro: {e}")
    
    def start_bot(self, bot_id):
        """Inicia bot específico"""
        try:
            if 0 <= bot_id < len(self.bots):
                bot = self.bots[bot_id]
                if not bot.running:
                    threading.Thread(target=bot.iniciar, daemon=True).start()
                    print(f"🚀 Bot {bot_id + 1} iniciado")
                    return True
        except Exception as e:
            print(f"❌ Erro ao iniciar bot {bot_id + 1}: {e}")
        return False
    
    def stop_bot(self, bot_id):
        """Para bot específico"""
        try:
            if 0 <= bot_id < len(self.bots):
                bot = self.bots[bot_id]
                if bot.running:
                    bot.parar()
                    print(f"⏹️ Bot {bot_id + 1} parado")
                    return True
        except Exception as e:
            print(f"❌ Erro ao parar bot {bot_id + 1}: {e}")
        return False
    
    def restart_bot(self, bot_id):
        """Reinicia bot específico"""
        try:
            if 0 <= bot_id < len(self.bots):
                bot = self.bots[bot_id]
                if bot.running:
                    bot.parar()
                    time.sleep(2)
                threading.Thread(target=bot.iniciar, daemon=True).start()
                print(f"🔄 Bot {bot_id + 1} reiniciado")
                return True
        except Exception as e:
            print(f"❌ Erro ao reiniciar bot {bot_id + 1}: {e}")
        return False
    
    def iniciar_todos(self, intervalo_segundos=180):
        """Inicia todos os bots com execução sequencial usando fila"""
        threads = []
        
        # Obter velocidade de navegação da configuração
        config = self.carregar_config()
        velocidade_navegacao = config.get('velocidade_navegacao', 5)
        
        print(f"🚀 Iniciando {len(self.bots)} bots com fila de execução sequencial...")
        print(f"⚡ Velocidade de navegação: {velocidade_navegacao}s entre cada bot")
        
        # Criar uma fila de execução compartilhada
        import threading
        self.fila_execucao = threading.Lock()
        
        # Iniciar bots sequencialmente com intervalo
        for i, bot in enumerate(self.bots):
            print(f"⏳ Iniciando bot {i+1}/{len(self.bots)}...")
            
            # Configurar bot para usar fila compartilhada
            bot.fila_execucao = self.fila_execucao
            
            thread = bot.iniciar(intervalo_segundos)
            threads.append(thread)
            
            # Aguardar intervalo antes de iniciar próximo bot (exceto no último)
            if i < len(self.bots) - 1:
                print(f"⏳ Aguardando {velocidade_navegacao}s antes do próximo bot...")
                time.sleep(velocidade_navegacao)
        
        # Notificar que bots foram iniciados
        self.notify_bot_started()
        
        print(f"✅ Todos os {len(self.bots)} bots iniciados com sucesso!")
        return threads
    
    def parar_todos(self, reason="Manual"):
        """Para todos os bots com encerramento eficiente de processos"""
        print(f"🛑 Iniciando parada de todos os bots (motivo: {reason})...")
        
        # Notificar que bots foram parados
        self.notify_bot_stopped(reason)
        
        # Parar sistema de relatórios
        self.stop_report_system()
        
        # Parar cada bot com timeout
        bots_parados = 0
        total_bots = len(self.bots)
        
        for i, bot in enumerate(self.bots):
            try:
                print(f"⏳ Parando bot {i+1}/{total_bots} (ID: {bot.bot_id})...")
                bot.parar()
                bots_parados += 1
                print(f"✅ Bot {bot.bot_id} parado com sucesso")
            except Exception as e:
                print(f"❌ Erro ao parar bot {bot.bot_id}: {e}")
        
        # Limpeza final - buscar e encerrar processos Chrome órfãos globais
        self._limpeza_final_chrome()
        
        self.bots = []
        print(f"🛑 Parada concluída: {bots_parados}/{total_bots} bots parados com sucesso")
    
    def parada_emergencial(self):
        """Parada emergencial do sistema"""
        print("� PARADA EMERGENCIAL ATIVADA!")
        
        # Notificar emergência
        self.notify_bot_stopped("Parada Emergencial")
        
        # Parar sistema de relatórios
        self.stop_report_system()
        
        # Encerrar todos os processos Chrome
        self.encerrar_chrome_emergencia()
        
        # Limpar lista de bots
        self.bots = []
        
        print("🚨 PARADA EMERGENCIAL CONCLUÍDA!")
    
    def reiniciar_todos(self):
        """Reinicia todos os bots"""
        print("🔄 Reiniciando todos os bots...")
        
        # Parar todos
        self.parar_todos("Reinicialização")
        
        # Aguardar um pouco
        time.sleep(3)
        
        # Iniciar novamente
        self.iniciar_todos()
        
        print("🔄 Reinicialização concluída!")
    
    def adicionar_bot(self, bot):
        """Adiciona bot ao manager"""
        self.bots.append(bot)
        print(f"➕ Bot {bot.bot_id} adicionado ao manager")
    
    def bot_existe(self, bot_id):
        """Verifica se bot existe"""
        return any(bot.bot_id == bot_id for bot in self.bots)
    
    def bot_rodando(self, bot_id):
        """Verifica se bot está rodando"""
        for bot in self.bots:
            if bot.bot_id == bot_id:
                return bot.running
        return False
    
    def get_bot(self, bot_id):
        """Obtém bot pelo ID"""
        for bot in self.bots:
            if bot.bot_id == bot_id:
                return bot
        return None
    
    def iniciar_bot(self, bot_id):
        """Inicia bot específico"""
        bot = self.get_bot(bot_id)
        if bot and not bot.running:
            threading.Thread(target=bot.iniciar, daemon=True).start()
            return True
        return False
    
    def parar_bot(self, bot_id):
        """Para bot específico"""
        bot = self.get_bot(bot_id)
        if bot and bot.running:
            bot.parar()
            return True
        return False
    
    def reiniciar_bot(self, bot_id):
        """Reinicia bot específico"""
        bot = self.get_bot(bot_id)
        if bot:
            if bot.running:
                bot.parar()
                time.sleep(2)
            threading.Thread(target=bot.iniciar, daemon=True).start()
            return True
        return False
        
    def _limpeza_final_chrome(self):
        """Limpeza final de todos os processos Chrome órfãos relacionados ao bot"""
        try:
            print("🧹 Executando limpeza final de processos Chrome...")
            orfaos_globais = 0
            
            # Buscar processos Chrome relacionados aos perfis do bot
            for processo in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if processo.info['name'] and 'chrome' in processo.info['name'].lower():
                        cmdline = processo.info['cmdline']
                        if cmdline and any('profiles' in arg.lower() and 'profile-' in arg.lower() for arg in cmdline):
                            print(f"🧹 Processo Chrome órfão global encontrado: PID {processo.info['pid']}")
                            proc = psutil.Process(processo.info['pid'])
                            proc.terminate()
                            
                            try:
                                proc.wait(timeout=2)
                            except psutil.TimeoutExpired:
                                proc.kill()
                                
                            orfaos_globais += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            if orfaos_globais > 0:
                print(f"🧹 {orfaos_globais} processos Chrome órfãos globais limpos")
            else:
                print("🧹 Nenhum processo Chrome órfão global encontrado")
                
        except Exception as e:
            print(f"⚠️ Erro durante limpeza final: {e}")
            
    def encerrar_chrome_emergencia(self):
        """Método de emergência para encerrar todos os processos Chrome"""
        print("🚨 Executando encerramento de emergência do Chrome...")
        try:
            # Encerrar todos os processos Chrome do sistema
            processos_encerrados = 0
            for processo in psutil.process_iter(['pid', 'name']):
                try:
                    if processo.info['name'] and 'chrome' in processo.info['name'].lower():
                        proc = psutil.Process(processo.info['pid'])
                        print(f"🚨 Encerrando processo Chrome: PID {processo.info['pid']}")
                        proc.terminate()
                        
                        try:
                            proc.wait(timeout=2)
                        except psutil.TimeoutExpired:
                            proc.kill()
                            
                        processos_encerrados += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            print(f"🚨 Encerramento de emergência concluído: {processos_encerrados} processos Chrome encerrados")
            return processos_encerrados
            
        except Exception as e:
            print(f"❌ Erro durante encerramento de emergência: {e}")
            return 0
    
    def obter_stats_todos(self):
        """Retorna estatísticas de todos os bots"""
        stats = []
        for bot in self.bots:
            stats.append({
                'bot_id': bot.bot_id,
                'stats': bot.obter_stats(),
                'ativo': bot.running
            })
        return stats
    
    def reiniciar_guias(self):
        """Reinicia todas as guias dos bots"""
        print("🔄 Reiniciando guias de todos os bots...")
        sucesso = 0
        falhas = 0
        
        for bot in self.bots:
            try:
                if bot.running and bot.driver:
                    if bot._reiniciar_guia_keydrop():
                        sucesso += 1
                    else:
                        falhas += 1
                        
            except Exception as e:
                print(f"❌ Erro ao reiniciar guia do bot {bot.bot_id}: {e}")
                falhas += 1
        
        print(f"🔄 Reinício de guias concluído: {sucesso} sucessos, {falhas} falhas")
        return sucesso, falhas
    
    def adicionar_bot(self, bot):
        """Adiciona um novo bot ao gerenciador"""
        self.bots.append(bot)
        print(f"➕ Bot {bot.bot_id} adicionado ao gerenciador")
    
    def remover_bot(self, bot_id):
        """Remove um bot do gerenciador"""
        for i, bot in enumerate(self.bots):
            if bot.bot_id == bot_id:
                try:
                    if bot.running:
                        bot.parar()
                    self.bots.pop(i)
                    print(f"❌ Bot {bot_id} removido do gerenciador")
                    return True
                except Exception as e:
                    print(f"❌ Erro ao remover bot {bot_id}: {e}")
                    return False
        return False
    
    def bot_existe(self, bot_id):
        """Verifica se um bot existe"""
        return any(bot.bot_id == bot_id for bot in self.bots)
    
    def bot_rodando(self, bot_id):
        """Verifica se um bot está rodando"""
        for bot in self.bots:
            if bot.bot_id == bot_id:
                return bot.running
        return False
    
    def get_bot(self, bot_id):
        """Retorna um bot pelo ID"""
        for bot in self.bots:
            if bot.bot_id == bot_id:
                return bot
        return None
    
    def iniciar_bot(self, bot_id):
        """Inicia um bot específico"""
        for bot in self.bots:
            if bot.bot_id == bot_id:
                try:
                    if not bot.running:
                        bot.iniciar()
                        print(f"▶️ Bot {bot_id} iniciado")
                        return True
                    else:
                        print(f"⚠️ Bot {bot_id} já está rodando")
                        return False
                except Exception as e:
                    print(f"❌ Erro ao iniciar bot {bot_id}: {e}")
                    return False
        return False
    
    def parar_bot(self, bot_id):
        """Para um bot específico"""
        for bot in self.bots:
            if bot.bot_id == bot_id:
                try:
                    if bot.running:
                        bot.parar()
                        print(f"⏹️ Bot {bot_id} parado")
                        return True
                    else:
                        print(f"⚠️ Bot {bot_id} já está parado")
                        return False
                except Exception as e:
                    print(f"❌ Erro ao parar bot {bot_id}: {e}")
                    return False
        return False
    
    def reiniciar_bot(self, bot_id):
        """Reinicia um bot específico"""
        for bot in self.bots:
            if bot.bot_id == bot_id:
                try:
                    if bot.running:
                        bot.parar()
                        time.sleep(2)
                    bot.iniciar()
                    print(f"🔄 Bot {bot_id} reiniciado")
                    return True
                except Exception as e:
                    print(f"❌ Erro ao reiniciar bot {bot_id}: {e}")
                    return False
        return False
    
    def reiniciar_todos(self):
        """Reinicia todos os bots"""
        print("🔄 Reiniciando todos os bots...")
        for bot in self.bots:
            try:
                if bot.running:
                    bot.parar()
                    time.sleep(1)
                bot.iniciar()
                print(f"🔄 Bot {bot.bot_id} reiniciado")
            except Exception as e:
                print(f"❌ Erro ao reiniciar bot {bot.bot_id}: {e}")
    
    def parada_emergencial(self):
        """Executa parada emergencial de todos os bots"""
        print("🚨 PARADA EMERGENCIAL ATIVADA!")
        
        # Parar todos os bots
        for bot in self.bots:
            try:
                bot.running = False
                bot.status = "🚨 Parada emergencial"
            except:
                pass
        
        # Encerrar Chrome de emergência
        self.encerrar_chrome_emergencia()
        
        # Limpar lista de bots
        self.bots = []
        print("🚨 Parada emergencial concluída!")

class ReportManager:
    """Gerencia relatórios automáticos a cada 12 horas"""
    
    def __init__(self, manager):
        self.manager = manager
        self.ultimo_relatorio = datetime.now()
        self.stats_periodo = {
            'amateur_total': 0,
            'contender_total': 0,
            'erros_total': 0,
            'ganho_total': 0.0,
            'bots_ativos': 0,
            'tempo_ativo': 0
        }
        self.running = False
        self.thread = None
        
    def iniciar(self):
        """Inicia o sistema de relatórios"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._loop_relatorio, daemon=True)
            self.thread.start()
            print("📊 Sistema de relatórios automáticos iniciado")
    
    def parar(self):
        """Para o sistema de relatórios"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        print("📊 Sistema de relatórios automáticos parado")
    
    def _loop_relatorio(self):
        """Loop principal para envio de relatórios"""
        while self.running:
            try:
                agora = datetime.now()
                # Verifica se passou 12 horas desde o último relatório
                if (agora - self.ultimo_relatorio).total_seconds() >= 43200:  # 12 horas = 43200 segundos
                    self._enviar_relatorio()
                    self.ultimo_relatorio = agora
                
                # Verifica a cada 5 minutos
                time.sleep(300)
                
            except Exception as e:
                print(f"Erro no loop de relatórios: {e}")
                time.sleep(300)
    
    def _coletar_stats(self):
        """Coleta estatísticas de todos os bots"""
        stats_totais = {
            'amateur_total': 0,
            'contender_total': 0,
            'erros_total': 0,
            'ganho_total': 0.0,
            'bots_ativos': 0,
            'bots_total': len(self.manager.bots),
            'tempo_ativo_medio': 0,
            'saldo_total_atual': 0.0,
            'melhor_bot': None,
            'pior_bot': None,
            'bot_detalhes': []
        }
        
        if not self.manager.bots:
            return stats_totais
        
        tempo_total = 0
        melhor_performance = 0
        pior_performance = float('inf')
        
        for bot in self.manager.bots:
            try:
                bot_stats = bot.stats
                
                # Debug - imprimir estatísticas do bot
                print(f"[Relatório] Bot {bot.bot_id} - AMATEUR: {bot_stats.get('participacoes', 0)}, CONTENDER: {bot_stats.get('participacoes_contender', 0)}, Erros: {bot_stats.get('erros', 0)}")
                
                # Contabilizar participações
                stats_totais['amateur_total'] += bot_stats.get('participacoes', 0)
                stats_totais['contender_total'] += bot_stats.get('participacoes_contender', 0)
                stats_totais['erros_total'] += bot_stats.get('erros', 0)
                
                # Calcular ganho do período
                ganho_bot = bot_stats.get('ganho_periodo', 0.0)
                stats_totais['ganho_total'] += ganho_bot
                
                # Saldo atual
                saldo_atual = bot_stats.get('saldo_atual', 0.0)
                stats_totais['saldo_total_atual'] += saldo_atual
                
                # Verificar se bot está ativo
                if bot.running:
                    stats_totais['bots_ativos'] += 1
                
                # Calcular tempo ativo
                if bot_stats.get('inicio'):
                    tempo_ativo = (datetime.now() - bot_stats['inicio']).total_seconds()
                    tempo_total += tempo_ativo
                
                # Performance do bot (participações por hora)
                total_participacoes = bot_stats.get('participacoes', 0) + bot_stats.get('participacoes_contender', 0)
                if bot_stats.get('inicio'):
                    horas_ativo = (datetime.now() - bot_stats['inicio']).total_seconds() / 3600
                    if horas_ativo > 0:
                        performance = total_participacoes / horas_ativo
                        
                        if performance > melhor_performance:
                            melhor_performance = performance
                            stats_totais['melhor_bot'] = {
                                'id': bot.bot_id,
                                'participacoes': total_participacoes,
                                'performance': performance,
                                'saldo': saldo_atual
                            }
                        
                        if performance < pior_performance:
                            pior_performance = performance
                            stats_totais['pior_bot'] = {
                                'id': bot.bot_id,
                                'participacoes': total_participacoes,
                                'performance': performance,
                                'saldo': saldo_atual
                            }
                
                # Detalhes do bot
                stats_totais['bot_detalhes'].append({
                    'id': bot.bot_id,
                    'ativo': bot.running,
                    'amateur': bot_stats.get('participacoes', 0),
                    'contender': bot_stats.get('participacoes_contender', 0),
                    'erros': bot_stats.get('erros', 0),
                    'saldo': saldo_atual,
                    'ganho': ganho_bot,
                    'status': bot.status
                })
                
            except Exception as e:
                print(f"Erro ao coletar stats do bot {bot.bot_id}: {e}")
        
        # Calcular tempo ativo médio
        if stats_totais['bots_total'] > 0:
            stats_totais['tempo_ativo_medio'] = tempo_total / stats_totais['bots_total']
        
        return stats_totais
    
    def _enviar_relatorio(self):
        """Envia relatório para o Discord"""
        if not self.manager.discord_webhook:
            return
        
        try:
            stats = self._coletar_stats()
            
            # Calcular tempo do período
            tempo_periodo = datetime.now() - self.ultimo_relatorio
            horas_periodo = tempo_periodo.total_seconds() / 3600
            
            # Preparar dados do relatório
            relatorio = self._gerar_relatorio_completo(stats, horas_periodo)
            
            # Enviar para Discord
            from discord_notify import send_discord_notification
            send_discord_notification(
                self.manager.discord_webhook,
                "📊 **RELATÓRIO AUTOMÁTICO DE 12 HORAS**",
                relatorio
            )
            
            # Resetar stats do período
            self._resetar_stats_periodo()
            
        except Exception as e:
            print(f"Erro ao enviar relatório: {e}")
    
    def _gerar_relatorio_completo(self, stats, horas_periodo):
        """Gera relatório completo com embed"""
        # Calcular métricas de performance
        total_participacoes = stats['amateur_total'] + stats['contender_total']
        performance_hora = total_participacoes / horas_periodo if horas_periodo > 0 else 0
        
        # Status geral do sistema
        if stats['bots_ativos'] == stats['bots_total']:
            status_geral = "🟢 Todos os bots funcionando perfeitamente"
            cor = 3066993  # Verde
        elif stats['bots_ativos'] > stats['bots_total'] * 0.5:
            status_geral = f"🟡 {stats['bots_ativos']}/{stats['bots_total']} bots ativos"
            cor = 16776960  # Amarelo
        else:
            status_geral = f"🔴 Apenas {stats['bots_ativos']}/{stats['bots_total']} bots ativos"
            cor = 15548997  # Vermelho
        
        # Formatação do tempo
        tempo_formatado = self._formatar_tempo(horas_periodo)
        
        # Criar embed
        embed = {
            "title": "📊 RELATÓRIO AUTOMÁTICO - 12 HORAS",
            "description": f"Relatório detalhado do período de **{tempo_formatado}**",
            "color": cor,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "thumbnail": {
                "url": "https://cdn.discordapp.com/emojis/894678089630720010.png"
            },
            "fields": [
                {
                    "name": "🎯 **RESUMO DO PERÍODO**",
                    "value": f"```\n🏆 AMATEUR: {stats['amateur_total']:,} sorteios\n🏆 CONTENDER: {stats['contender_total']:,} sorteios\n📈 Total: {total_participacoes:,} participações\n⚡ Performance: {performance_hora:.1f} sorteios/hora```",
                    "inline": False
                },
                {
                    "name": "💰 **GANHOS E SALDO**",
                    "value": f"```\n💵 Ganho no período: R$ {stats['ganho_total']:.2f}\n🏦 Saldo total atual: R$ {stats['saldo_total_atual']:.2f}\n📊 Média por bot: R$ {stats['saldo_total_atual']/stats['bots_total']:.2f}```",
                    "inline": False
                },
                {
                    "name": "⚠️ **FALHAS E ERROS**",
                    "value": f"```\n❌ Total de erros: {stats['erros_total']:,}\n📊 Taxa de erro: {(stats['erros_total']/max(total_participacoes, 1)*100):.1f}%\n🔧 Média por bot: {stats['erros_total']/stats['bots_total']:.1f}```",
                    "inline": False
                },
                {
                    "name": "🤖 **STATUS DOS BOTS**",
                    "value": f"```\n{status_geral}\n🔢 Total configurado: {stats['bots_total']} bots\n⏱️ Tempo ativo médio: {self._formatar_tempo(stats['tempo_ativo_medio']/3600)}```",
                    "inline": False
                }
            ],
            "footer": {
                "text": "KeyDrop Bot Professional - Relatório Automático",
                "icon_url": "https://cdn.discordapp.com/emojis/894678089630720010.png"
            }
        }
        
        # Adicionar informações do melhor e pior bot
        if stats['melhor_bot'] and stats['pior_bot']:
            embed["fields"].append({
                "name": "🏅 **PERFORMANCE DOS BOTS**",
                "value": f"```\n🥇 Melhor: Bot {stats['melhor_bot']['id']} - {stats['melhor_bot']['participacoes']} sorteios\n🥉 Menor: Bot {stats['pior_bot']['id']} - {stats['pior_bot']['participacoes']} sorteios```",
                "inline": False
            })
        
        # Adicionar detalhes por bot (máximo 10)
        if stats['bot_detalhes']:
            detalhes_text = ""
            for i, bot in enumerate(stats['bot_detalhes'][:10]):
                status_emoji = "🟢" if bot['ativo'] else "🔴"
                detalhes_text += f"{status_emoji} Bot {bot['id']}: {bot['amateur']}A/{bot['contender']}C - R${bot['saldo']:.2f}\n"
            
            embed["fields"].append({
                "name": "📋 **DETALHES POR BOT**",
                "value": f"```\n{detalhes_text}```",
                "inline": False
            })
        
        return embed
    
    def _formatar_tempo(self, horas):
        """Formata tempo em horas para formato legível"""
        if horas < 1:
            return f"{int(horas * 60)}min"
        elif horas < 24:
            return f"{horas:.1f}h"
        else:
            dias = int(horas // 24)
            horas_rest = horas % 24
            return f"{dias}d {horas_rest:.1f}h"
    
    def _resetar_stats_periodo(self):
        """Reseta estatísticas do período"""
        for bot in self.manager.bots:
            bot.stats['ganho_periodo'] = 0.0

if __name__ == "__main__":
    # Teste básico
    manager = BotManager()
    config = manager.carregar_config()
    
    print("=== KeyDrop Bot Manager ===")
    print(f"Configuração atual: {config}")
    print("Iniciando bots...")
    
    manager.criar_bots(config['num_bots'])
    threads = manager.iniciar_todos(config['intervalo_sorteios'])
    
    print("Bots iniciados! Pressione Ctrl+C para parar.")
    
    try:
        while True:
            time.sleep(10)
            stats = manager.obter_stats_todos()
            for stat in stats:
                print(f"Bot {stat['bot_id']}: {stat['stats']['participacoes']} participações, {stat['stats']['erros']} erros")
    except KeyboardInterrupt:
        print("\nParando bots...")
        manager.parar_todos()
        print("Bots parados!")
