#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Correção do Chrome e implementação do modo CONTENDER
👨‍💻 Desenvolvido por: Billy Franck (wmedrado)
📞 Discord: wmedrado
"""

import sys
import os
import time
import shutil
import tempfile
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class ChromeFixer:
    """Classe para corrigir problemas do Chrome"""
    
    def __init__(self):
        self.temp_dir = None
        
    def criar_perfil_temporario(self, profile_original):
        """Cria um perfil temporário para evitar conflitos"""
        try:
            # Criar diretório temporário
            self.temp_dir = tempfile.mkdtemp(prefix='keydrop_chrome_')
            
            # Caminho do perfil original
            profile_path = Path(profile_original)
            
            if profile_path.exists():
                # Copiar apenas arquivos essenciais do perfil
                arquivos_essenciais = [
                    'Preferences',
                    'Local State',
                    'Cookies',
                    'Login Data',
                    'Web Data'
                ]
                
                for arquivo in arquivos_essenciais:
                    origem = profile_path / arquivo
                    if origem.exists():
                        destino = Path(self.temp_dir) / arquivo
                        if origem.is_file():
                            shutil.copy2(origem, destino)
                        else:
                            shutil.copytree(origem, destino, dirs_exist_ok=True)
            
            print(f"✅ Perfil temporário criado: {self.temp_dir}")
            return self.temp_dir
            
        except Exception as e:
            print(f"⚠️ Erro ao criar perfil temporário: {e}")
            return profile_original
    
    def configurar_chrome_options(self, profile_path):
        """Configura opções robustas do Chrome"""
        try:
            from selenium.webdriver.chrome.options import Options
            
            options = Options()
            
            # Usar perfil temporário se disponível
            if self.temp_dir:
                options.add_argument(f'--user-data-dir={self.temp_dir}')
            else:
                options.add_argument(f'--user-data-dir={profile_path}')
            
            # Opções para evitar crashes
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-web-security')
            options.add_argument('--disable-features=VizDisplayCompositor')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')
            options.add_argument('--disable-javascript')
            options.add_argument('--disable-background-timer-throttling')
            options.add_argument('--disable-backgrounding-occluded-windows')
            options.add_argument('--disable-renderer-backgrounding')
            options.add_argument('--disable-features=TranslateUI')
            options.add_argument('--disable-ipc-flooding-protection')
            options.add_argument('--disable-component-extensions-with-background-pages')
            options.add_argument('--disable-default-apps')
            options.add_argument('--mute-audio')
            options.add_argument('--no-first-run')
            options.add_argument('--no-default-browser-check')
            options.add_argument('--disable-background-networking')
            options.add_argument('--disable-sync')
            options.add_argument('--metrics-recording-only')
            options.add_argument('--disable-prompt-on-repost')
            options.add_argument('--disable-client-side-phishing-detection')
            options.add_argument('--disable-component-update')
            options.add_argument('--disable-domain-reliability')
            
            # Configurações de performance
            options.add_argument('--memory-pressure-off')
            options.add_argument('--max_old_space_size=4096')
            
            # Configurações experimentais para estabilidade
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('detach', True)
            
            # Configurações de log mínimas
            options.add_argument('--log-level=3')
            options.add_argument('--silent')
            
            print("✅ Opções do Chrome configuradas")
            return options
            
        except Exception as e:
            print(f"❌ Erro ao configurar opções: {e}")
            return None
    
    def iniciar_chrome_seguro(self, profile_path):
        """Inicia o Chrome com configurações seguras"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            
            # Criar perfil temporário
            self.criar_perfil_temporario(profile_path)
            
            # Configurar opções
            options = self.configurar_chrome_options(profile_path)
            
            # Configurar service do ChromeDriver
            service = Service()
            service.creation_flags = 0x08000000  # CREATE_NO_WINDOW
            
            # Tentar iniciar o Chrome
            driver = webdriver.Chrome(service=service, options=options)
            
            # Configurar timeouts
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
            print("✅ Chrome iniciado com sucesso!")
            return driver
            
        except Exception as e:
            print(f"❌ Erro ao iniciar Chrome: {e}")
            return None
    
    def limpar_recursos(self, driver=None):
        """Limpa recursos e arquivos temporários"""
        try:
            if driver:
                driver.quit()
            
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                print("✅ Recursos limpos")
                
        except Exception as e:
            print(f"⚠️ Erro ao limpar recursos: {e}")

class ContenderBot:
    """Implementação do modo CONTENDER com os seletores corretos"""
    
    def __init__(self):
        self.driver = None
        self.chrome_fixer = ChromeFixer()
        
    def inicializar(self, profile_path):
        """Inicializa o bot com Chrome corrigido"""
        try:
            print("🔧 Inicializando bot CONTENDER...")
            
            # Usar o Chrome corrigido
            self.driver = self.chrome_fixer.iniciar_chrome_seguro(profile_path)
            
            if not self.driver:
                return False
                
            print("✅ Bot CONTENDER inicializado!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inicializar bot: {e}")
            return False
    
    def acessar_giveaways(self):
        """Acessa a página de giveaways"""
        try:
            print("🌐 Acessando página de giveaways...")
            
            # Acessar página principal primeiro
            self.driver.get("https://key-drop.com/")
            time.sleep(3)
            
            # Verificar se está logado
            if not self.verificar_login():
                print("❌ Usuário não está logado. Faça login primeiro.")
                return False
            
            # Acessar página de giveaways
            url = "https://key-drop.com/pt/giveaways/list"
            print(f"🔄 Acessando: {url}")
            
            self.driver.get(url)
            time.sleep(5)  # Aguardar carregamento
            
            # Verificar se chegou na página correta
            if "giveaways" not in self.driver.current_url.lower():
                print("❌ Não foi possível acessar página de giveaways")
                return False
            
            print("✅ Página de giveaways carregada!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao acessar giveaways: {e}")
            return False
    
    def verificar_login(self):
        """Verifica se o usuário está logado"""
        try:
            from selenium.webdriver.common.by import By
            
            # Procurar indicadores de login
            indicadores_login = [
                "profile",
                "logout",
                "dashboard",
                "account",
                "wallet"
            ]
            
            for indicador in indicadores_login:
                elementos = self.driver.find_elements(By.PARTIAL_LINK_TEXT, indicador)
                if elementos:
                    print(f"✅ Usuário está logado (encontrado: {indicador})")
                    return True
            
            # Verificar se há campo de login (indicaria que não está logado)
            campos_login = self.driver.find_elements(By.NAME, "email")
            campos_login += self.driver.find_elements(By.NAME, "password")
            
            if campos_login:
                print("❌ Usuário não está logado (campos de login encontrados)")
                return False
            
            print("✅ Assumindo que usuário está logado")
            return True
            
        except Exception as e:
            print(f"⚠️ Erro ao verificar login: {e}")
            return True  # Assumir que está logado em caso de erro
    
    def encontrar_giveaways(self):
        """Encontra giveaways disponíveis usando os seletores identificados"""
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            print("🔍 Procurando giveaways...")
            
            # Aguardar o container principal carregar
            wait = WebDriverWait(self.driver, 15)
            main_container = wait.until(
                EC.presence_of_element_located((By.ID, "main-view"))
            )
            
            print("✅ Container principal carregado")
            
            # Aguardar os giveaways carregarem
            time.sleep(3)
            
            # Encontrar todos os botões "Participar no Sorteio" usando múltiplos seletores
            botoes_participar = []
            
            # Método 1: Por texto do link
            try:
                botoes_link = self.driver.find_elements(By.LINK_TEXT, "Participar no Sorteio")
                botoes_participar.extend(botoes_link)
                print(f"📌 Encontrados {len(botoes_link)} botões por link text")
            except:
                pass
            
            # Método 2: Por XPath específico fornecido
            try:
                botoes_xpath = self.driver.find_elements(
                    By.XPATH, 
                    "//*[@id='main-view']/div/div[2]/div/div[3]/div/div/div/div/div[5]/a"
                )
                for botao in botoes_xpath:
                    if botao not in botoes_participar:
                        botoes_participar.append(botao)
                print(f"📌 Encontrados {len(botoes_xpath)} botões por XPath específico")
            except:
                pass
            
            # Método 3: Por CSS selector baseado no HTML fornecido
            try:
                botoes_css = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "div.flex.flex-col.gap-2\\.5 > a"
                )
                for botao in botoes_css:
                    if "Participar no Sorteio" in botao.text and botao not in botoes_participar:
                        botoes_participar.append(botao)
                print(f"📌 Encontrados {len(botoes_css)} botões por CSS selector")
            except:
                pass
            
            # Método 4: Procurar por todos os links que contenham "giveaway"
            try:
                botoes_giveaway = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    "a[href*='giveaway']"
                )
                for botao in botoes_giveaway:
                    if "Participar no Sorteio" in botao.text and botao not in botoes_participar:
                        botoes_participar.append(botao)
                print(f"📌 Encontrados {len(botoes_giveaway)} botões por href giveaway")
            except:
                pass
            
            print(f"🎯 TOTAL: {len(botoes_participar)} botões 'Participar no Sorteio' encontrados")
            
            giveaways_ativos = []
            
            for i, botao in enumerate(botoes_participar):
                try:
                    # Verificar se o botão está visível e habilitado
                    if botao.is_displayed() and botao.is_enabled():
                        # Verificar se não já está participando
                        texto_botao = botao.text.lower()
                        
                        if "participar" in texto_botao and "sorteio" in texto_botao:
                            giveaways_ativos.append({
                                'botao': botao,
                                'indice': i + 1,
                                'texto': botao.text
                            })
                            print(f"✅ Giveaway {i + 1}: Disponível para participação")
                        else:
                            print(f"⚠️ Giveaway {i + 1}: Já participando ou indisponível (texto: {botao.text})")
                    else:
                        print(f"⚠️ Giveaway {i + 1}: Botão não está visível/habilitado")
                        
                except Exception as e:
                    print(f"⚠️ Erro ao analisar giveaway {i + 1}: {e}")
                    continue
            
            print(f"🎯 Total de giveaways disponíveis: {len(giveaways_ativos)}")
            return giveaways_ativos
            
        except Exception as e:
            print(f"❌ Erro ao encontrar giveaways: {e}")
            return []
    
    def participar_giveaway(self, giveaway_info):
        """Participa de um giveaway específico"""
        try:
            botao = giveaway_info['botao']
            indice = giveaway_info['indice']
            
            print(f"🎯 Participando do giveaway {indice}...")
            
            # Scroll até o elemento para garantir que está visível
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
            time.sleep(1)
            
            # Verificar se o botão ainda está disponível
            if not botao.is_displayed() or not botao.is_enabled():
                print(f"⚠️ Giveaway {indice}: Botão não está mais disponível")
                return False
            
            # Aguardar elemento estar clicável
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            try:
                wait = WebDriverWait(self.driver, 5)
                wait.until(EC.element_to_be_clickable(botao))
            except:
                print(f"⚠️ Giveaway {indice}: Botão não ficou clicável")
            
            # Tentar clicar no botão
            try:
                # Primeiro tentar clique normal
                botao.click()
                print(f"✅ Clique normal realizado no giveaway {indice}")
            except Exception as e:
                print(f"⚠️ Clique normal falhou para giveaway {indice}: {e}")
                try:
                    # Se não funcionar, usar JavaScript
                    self.driver.execute_script("arguments[0].click();", botao)
                    print(f"✅ Clique via JavaScript realizado no giveaway {indice}")
                except Exception as e2:
                    print(f"❌ Clique via JavaScript falhou para giveaway {indice}: {e2}")
                    return False
            
            # Aguardar processamento da página
            time.sleep(5)
            
            # Verificar se houve redirecionamento ou mudança na página
            url_atual = self.driver.current_url
            if "giveaway" in url_atual:
                print(f"✅ Redirecionado para página do giveaway {indice}")
                
                # Aguardar e tentar voltar à página principal
                time.sleep(2)
                self.driver.back()
                time.sleep(3)
            
            print(f"✅ Participação no giveaway {indice} processada!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao participar do giveaway {giveaway_info['indice']}: {e}")
            return False
    
    def executar_modo_contender(self, profile_path):
        """Executa o modo CONTENDER completo"""
        print("🎯 INICIANDO MODO CONTENDER")
        print("=" * 50)
        
        participacoes_sucesso = 0
        
        try:
            # Inicializar bot
            if not self.inicializar(profile_path):
                return False
            
            # Acessar página de giveaways
            if not self.acessar_giveaways():
                return False
            
            # Encontrar giveaways disponíveis
            giveaways = self.encontrar_giveaways()
            
            if not giveaways:
                print("⚠️ Nenhum giveaway disponível para participação")
                return False
            
            # Participar de cada giveaway
            for giveaway in giveaways:
                if self.participar_giveaway(giveaway):
                    participacoes_sucesso += 1
                
                # Pausa entre participações para evitar rate limit
                time.sleep(2)
            
            print("\n" + "=" * 50)
            print("📊 RESULTADOS DO MODO CONTENDER")
            print("=" * 50)
            print(f"🎯 Giveaways encontrados: {len(giveaways)}")
            print(f"✅ Participações bem-sucedidas: {participacoes_sucesso}")
            print(f"❌ Falhas: {len(giveaways) - participacoes_sucesso}")
            print("=" * 50)
            
            return participacoes_sucesso > 0
            
        except Exception as e:
            print(f"❌ Erro no modo CONTENDER: {e}")
            return False
            
        finally:
            # Limpar recursos
            self.chrome_fixer.limpar_recursos(self.driver)

def main():
    """Função principal para teste"""
    print("🔧 TESTE DO MODO CONTENDER CORRIGIDO")
    print("=" * 60)
    
    # Solicitar perfil
    profile_input = input("📁 Caminho do perfil (ou Enter para Profile-1): ").strip()
    
    if not profile_input:
        profile_input = "profiles/Profile-1"
    
    # Converter para caminho absoleto
    if not os.path.isabs(profile_input):
        project_root = os.path.join(os.path.dirname(__file__), '..', '..')
        profile_path = os.path.abspath(os.path.join(project_root, profile_input))
    else:
        profile_path = profile_input
    
    print(f"📁 Usando perfil: {profile_path}")
    
    # Executar bot
    bot = ContenderBot()
    sucesso = bot.executar_modo_contender(profile_path)
    
    if sucesso:
        print("\n🎉 Modo CONTENDER executado com sucesso!")
    else:
        print("\n❌ Falha na execução do modo CONTENDER")
    
    print("\n" + "=" * 60)
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
