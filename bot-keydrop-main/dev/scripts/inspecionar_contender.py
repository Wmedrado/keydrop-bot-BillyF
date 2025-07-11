#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para inspecionar e implementar o modo CONTENDER
👨‍💻 Desenvolvido por: Billy Franck (wmedrado)
📞 Discord: wmedrado
"""

import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Adicionar o diretório raiz do projeto ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class ContenderInspector:
    """Classe para inspecionar e implementar o modo CONTENDER"""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def configurar_driver(self, profile_path):
        """Configura o driver do Chrome com perfil específico"""
        try:
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            import tempfile
            
            options = Options()
            
            # Estratégias para resolver problemas de crash
            print("🔧 Configurando Chrome com estratégias anti-crash...")
            
            # 1. Usar perfil temporário se o original causar problemas
            temp_profile = None
            try:
                if profile_path and os.path.exists(profile_path):
                    options.add_argument(f'--user-data-dir={profile_path}')
                    print(f"📁 Usando perfil: {profile_path}")
                else:
                    # Criar perfil temporário
                    temp_profile = tempfile.mkdtemp(prefix='chrome_profile_')
                    options.add_argument(f'--user-data-dir={temp_profile}')
                    print(f"📁 Usando perfil temporário: {temp_profile}")
            except:
                # Usar perfil padrão
                print("📁 Usando perfil padrão do Chrome")
            
            # 2. Argumentos para estabilidade
            stability_args = [
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images',
                '--disable-javascript',  # Temporariamente para inspeção
                '--disable-default-apps',
                '--disable-sync',
                '--disable-translate',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-field-trial-config',
                '--disable-back-forward-cache',
                '--disable-ipc-flooding-protection',
                '--remote-debugging-port=0',  # Evita conflitos de porta
                '--disable-crash-reporter',
                '--disable-in-process-stack-traces',
                '--disable-logging',
                '--silent',
                '--log-level=3',
                '--window-size=1920,1080',
                '--start-maximized'
            ]
            
            for arg in stability_args:
                options.add_argument(arg)
            
            # 3. Configurações de performance
            prefs = {
                "profile.default_content_setting_values": {
                    "notifications": 2,
                    "media_stream": 2,
                    "geolocation": 2
                },
                "profile.managed_default_content_settings": {
                    "images": 2
                }
            }
            options.add_experimental_option("prefs", prefs)
            
            # 4. Tentar múltiplas estratégias
            strategies = [
                ("Headless", lambda opts: opts.add_argument('--headless')),
                ("Normal", lambda opts: None),
                ("Sem perfil", lambda opts: self._remove_profile_args(opts))
            ]
            
            for strategy_name, strategy_func in strategies:
                try:
                    print(f"🔄 Tentativa: {strategy_name}")
                    
                    # Aplicar estratégia específica
                    if strategy_func:
                        strategy_func(options)
                    
                    # Criar service (pode resolver alguns problemas)
                    service = Service()
                    service.start()
                    
                    # Criar driver
                    self.driver = webdriver.Chrome(service=service, options=options)
                    self.wait = WebDriverWait(self.driver, 10)
                    
                    # Testar se funciona
                    self.driver.get("about:blank")
                    
                    print(f"✅ Driver configurado com sucesso! Estratégia: {strategy_name}")
                    return True
                    
                except Exception as e:
                    print(f"⚠️ Estratégia {strategy_name} falhou: {str(e)[:100]}...")
                    if self.driver:
                        try:
                            self.driver.quit()
                        except:
                            pass
                        self.driver = None
                    continue
            
            print("❌ Todas as estratégias falharam!")
            return False
            
        except Exception as e:
            print(f"❌ Erro geral ao configurar driver: {e}")
            return False
    
    def _remove_profile_args(self, options):
        """Remove argumentos de perfil das opções"""
        # Filtrar argumentos relacionados a user-data-dir
        new_args = []
        for arg in options.arguments:
            if not arg.startswith('--user-data-dir'):
                new_args.append(arg)
        options.arguments = new_args
    
    def acessar_giveaways(self):
        """Acessa a página de giveaways"""
        try:
            url = "https://key-drop.com/pt/giveaways/list"
            print(f"🔄 Acessando: {url}")
            
            self.driver.get(url)
            time.sleep(3)
            
            print("✅ Página carregada!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao acessar página: {e}")
            return False
    
    def inspecionar_elementos(self):
        """Inspeciona os elementos da página para encontrar seletores"""
        print("\n🔍 INSPECIONANDO ELEMENTOS DA PÁGINA")
        print("=" * 50)
        
        elementos_encontrados = {}
        
        # Lista de possíveis seletores para giveaways
        seletores_teste = [
            # Containers de giveaways
            ('.giveaway', 'container de giveaway'),
            ('.giveaway-item', 'item de giveaway'),
            ('.contest', 'contest'),
            ('.promotion', 'promoção'),
            ('[data-giveaway]', 'elemento com data-giveaway'),
            
            # Botões de participação
            ('.participate', 'botão participar'),
            ('.join', 'botão join'),
            ('.enter', 'botão enter'),
            ('.btn-participate', 'botão participar'),
            ('.btn-join', 'botão join'),
            ('button[data-participate]', 'botão com data-participate'),
            
            # Informações dos giveaways
            ('.giveaway-title', 'título do giveaway'),
            ('.giveaway-prize', 'prêmio'),
            ('.giveaway-time', 'tempo restante'),
            ('.participants', 'participantes'),
            ('.entries', 'entradas'),
            
            # Estados
            ('.active', 'ativo'),
            ('.ended', 'finalizado'),
            ('.joined', 'já participando'),
            ('.available', 'disponível'),
        ]
        
        for seletor, descricao in seletores_teste:
            try:
                elementos = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                if elementos:
                    elementos_encontrados[seletor] = {
                        'descricao': descricao,
                        'quantidade': len(elementos),
                        'texto_exemplo': elementos[0].text[:100] if elementos[0].text else 'Sem texto'
                    }
                    print(f"✅ {seletor}: {len(elementos)} elementos - {descricao}")
                
            except Exception as e:
                continue
        
        return elementos_encontrados
    
    def analisar_estrutura_html(self):
        """Analisa a estrutura HTML da página"""
        print("\n📄 ANALISANDO ESTRUTURA HTML")
        print("=" * 50)
        
        try:
            # Salvar HTML da página
            html_content = self.driver.page_source
            
            # Procurar por padrões comuns
            padroes = [
                'giveaway',
                'contest',
                'participate',
                'join',
                'enter',
                'btn',
                'button',
                'card',
                'item',
                'list'
            ]
            
            padroes_encontrados = {}
            
            for padrao in padroes:
                # Contar ocorrências (case insensitive)
                count = html_content.lower().count(padrao.lower())
                if count > 0:
                    padroes_encontrados[padrao] = count
            
            print("🔍 Padrões encontrados no HTML:")
            for padrao, count in sorted(padroes_encontrados.items(), key=lambda x: x[1], reverse=True):
                print(f"   {padrao}: {count} ocorrências")
            
            # Salvar HTML para análise manual
            html_file = os.path.join(os.path.dirname(__file__), '..', 'temp', 'giveaways_page.html')
            os.makedirs(os.path.dirname(html_file), exist_ok=True)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n💾 HTML salvo em: {html_file}")
            
            return padroes_encontrados
            
        except Exception as e:
            print(f"❌ Erro ao analisar HTML: {e}")
            return {}
    
    def testar_interacao(self):
        """Testa interação com elementos encontrados"""
        print("\n🖱️ TESTANDO INTERAÇÕES")
        print("=" * 50)
        
        # Lista de seletores para testar cliques
        seletores_clique = [
            'button',
            '.btn',
            '[role="button"]',
            'a.btn',
            'button.btn',
            '.participate',
            '.join',
            '.enter'
        ]
        
        for seletor in seletores_clique:
            try:
                elementos = self.driver.find_elements(By.CSS_SELECTOR, seletor)
                if elementos:
                    print(f"🔍 Encontrados {len(elementos)} elementos para: {seletor}")
                    
                    # Mostrar informações dos primeiros elementos
                    for i, elemento in enumerate(elementos[:3]):
                        try:
                            texto = elemento.text or elemento.get_attribute('title') or elemento.get_attribute('aria-label') or 'Sem texto'
                            classes = elemento.get_attribute('class') or 'Sem classes'
                            print(f"   {i+1}. Texto: '{texto[:50]}' | Classes: '{classes}'")
                        except:
                            continue
                            
            except Exception as e:
                continue
    
    def gerar_codigo_contender(self, elementos_encontrados):
        """Gera código para implementar o modo CONTENDER"""
        print("\n💻 GERANDO CÓDIGO PARA MODO CONTENDER")
        print("=" * 50)
        
        codigo_template = '''
def modo_contender(self):
    """Implementação do modo CONTENDER para KeyDrop"""
    try:
        # Acessar página de giveaways
        self.driver.get("https://key-drop.com/pt/giveaways/list")
        time.sleep(3)
        
        # SELETORES IDENTIFICADOS:
        # (Baseado na inspeção da página)
        
        # Encontrar containers de giveaways
        giveaway_containers = self.driver.find_elements(By.CSS_SELECTOR, "SELETOR_AQUI")
        
        if not giveaway_containers:
            print("⚠️ Nenhum giveaway encontrado")
            return False
        
        print(f"🎯 Encontrados {len(giveaway_containers)} giveaways")
        
        participacoes = 0
        
        for i, container in enumerate(giveaway_containers):
            try:
                # Verificar se o giveaway está ativo
                # (Implementar verificação baseada nos elementos encontrados)
                
                # Procurar botão de participação
                btn_participar = container.find_element(By.CSS_SELECTOR, "SELETOR_BOTAO_AQUI")
                
                if btn_participar and btn_participar.is_enabled():
                    # Clicar para participar
                    self.driver.execute_script("arguments[0].click();", btn_participar)
                    time.sleep(2)
                    
                    participacoes += 1
                    print(f"✅ Participou do giveaway {i+1}")
                    
                    # Aguardar entre participações
                    time.sleep(1)
                
            except Exception as e:
                print(f"⚠️ Erro no giveaway {i+1}: {e}")
                continue
        
        print(f"🎉 Total de participações: {participacoes}")
        return participacoes > 0
        
    except Exception as e:
        print(f"❌ Erro no modo CONTENDER: {e}")
        return False
'''
        
        # Salvar código template
        codigo_file = os.path.join(os.path.dirname(__file__), '..', 'temp', 'modo_contender_template.py')
        
        with open(codigo_file, 'w', encoding='utf-8') as f:
            f.write(codigo_template)
        
        print(f"💾 Template salvo em: {codigo_file}")
        
        # Gerar relatório de elementos
        relatorio = "\n# RELATÓRIO DE ELEMENTOS ENCONTRADOS\n\n"
        
        for seletor, info in elementos_encontrados.items():
            relatorio += f"## {seletor}\n"
            relatorio += f"- Descrição: {info['descricao']}\n"
            relatorio += f"- Quantidade: {info['quantidade']}\n"
            relatorio += f"- Exemplo: {info['texto_exemplo']}\n\n"
        
        relatorio_file = os.path.join(os.path.dirname(__file__), '..', 'temp', 'relatorio_elementos.md')
        
        with open(relatorio_file, 'w', encoding='utf-8') as f:
            f.write(relatorio)
        
        print(f"📊 Relatório salvo em: {relatorio_file}")
    
    def executar_inspecao_completa(self, profile_path):
        """Executa inspeção completa da página"""
        print("🔍 INSPEÇÃO COMPLETA DO MODO CONTENDER")
        print("=" * 60)
        
        try:
            # Configurar driver
            if not self.configurar_driver(profile_path):
                return False
            
            # Acessar página
            if not self.acessar_giveaways():
                return False
            
            # Inspecionar elementos
            elementos = self.inspecionar_elementos()
            
            # Analisar HTML
            self.analisar_estrutura_html()
            
            # Testar interações
            self.testar_interacao()
            
            # Gerar código
            self.gerar_codigo_contender(elementos)
            
            print("\n" + "=" * 60)
            print("✅ INSPEÇÃO CONCLUÍDA!")
            print("📁 Arquivos gerados em: dev/temp/")
            print("💡 Análise os arquivos e forneça os seletores corretos")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na inspeção: {e}")
            return False
            
        finally:
            if self.driver:
                self.driver.quit()

def main():
    """Função principal"""
    print("🔍 INSPETOR DO MODO CONTENDER")
    print("=" * 50)
    
    # Solicitar caminho do perfil
    profile_path = input("📁 Caminho do perfil do Chrome (ex: profiles/Profile-1): ").strip()
    
    if not profile_path:
        profile_path = "profiles/Profile-1"
    
    # Converter para caminho absoluto
    if not os.path.isabs(profile_path):
        project_root = os.path.join(os.path.dirname(__file__), '..', '..')
        profile_path = os.path.join(project_root, profile_path)
    
    inspector = ContenderInspector()
    inspector.executar_inspecao_completa(profile_path)
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
