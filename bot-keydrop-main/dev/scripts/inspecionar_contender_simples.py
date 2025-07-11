#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Inspetor simples do modo CONTENDER (sem Selenium)
👨‍💻 Desenvolvido por: Billy Franck (wmedrado)
📞 Discord: wmedrado
"""

import requests
import re
import os
from bs4 import BeautifulSoup
import json

class ContenderInspectorSimples:
    """Inspetor simples para analisar a página de giveaways"""
    
    def __init__(self):
        self.session = requests.Session()
        # Headers para simular um navegador real
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def obter_html_pagina(self, url):
        """Obtém o HTML da página de giveaways"""
        try:
            print(f"🔄 Fazendo requisição para: {url}")
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            print(f"✅ Página obtida! Status: {response.status_code}")
            print(f"📊 Tamanho: {len(response.content)} bytes")
            
            return response.text
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao obter página: {e}")
            return None
    
    def analisar_html(self, html_content):
        """Analisa o HTML para encontrar padrões de giveaways"""
        print("\n🔍 ANALISANDO HTML")
        print("=" * 40)
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Salvar HTML formatado
            temp_dir = os.path.join(os.path.dirname(__file__), '..', 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            
            html_file = os.path.join(temp_dir, 'giveaways_page.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            
            print(f"💾 HTML salvo em: {html_file}")
            
            # Análise de padrões
            padroes = self._analisar_padroes(soup)
            seletores = self._encontrar_seletores(soup)
            
            return {
                'padroes': padroes,
                'seletores': seletores,
                'html_file': html_file
            }
            
        except Exception as e:
            print(f"❌ Erro ao analisar HTML: {e}")
            return None
    
    def _analisar_padroes(self, soup):
        """Analisa padrões no HTML"""
        print("\n🔍 Padrões encontrados:")
        
        padroes = {}
        
        # Palavras-chave relacionadas a giveaways
        keywords = [
            'giveaway', 'contest', 'promotion', 'draw', 'raffle',
            'participate', 'join', 'enter', 'claim', 'win',
            'prize', 'reward', 'gift', 'free', 'sortear',
            'participar', 'ganhar', 'prêmio', 'grátis'
        ]
        
        html_lower = str(soup).lower()
        
        for keyword in keywords:
            count = html_lower.count(keyword.lower())
            if count > 0:
                padroes[keyword] = count
        
        # Mostrar padrões mais relevantes
        sorted_patterns = sorted(padroes.items(), key=lambda x: x[1], reverse=True)
        for pattern, count in sorted_patterns[:10]:
            print(f"   {pattern}: {count} ocorrências")
        
        return padroes
    
    def _encontrar_seletores(self, soup):
        """Encontra possíveis seletores CSS"""
        print("\n🎯 Procurando seletores relevantes:")
        
        seletores_encontrados = {}
        
        # Procurar por classes e IDs relevantes
        elementos_interesse = [
            # Containers
            {'tag': 'div', 'pattern': r'giveaway|contest|promotion|card|item'},
            {'tag': 'section', 'pattern': r'giveaway|contest|promotion'},
            {'tag': 'article', 'pattern': r'giveaway|contest|promotion'},
            
            # Botões
            {'tag': 'button', 'pattern': r'participate|join|enter|claim|btn'},
            {'tag': 'a', 'pattern': r'participate|join|enter|claim|btn'},
            
            # Listas
            {'tag': 'ul', 'pattern': r'list|items|giveaway'},
            {'tag': 'li', 'pattern': r'item|giveaway|contest'},
        ]
        
        for elemento in elementos_interesse:
            tag = elemento['tag']
            pattern = elemento['pattern']
            
            # Procurar elementos com essa tag
            elementos = soup.find_all(tag)
            
            for elem in elementos:
                # Verificar classes
                classes = elem.get('class', [])
                for classe in classes:
                    if re.search(pattern, classe, re.IGNORECASE):
                        seletor = f"{tag}.{classe}"
                        if seletor not in seletores_encontrados:
                            seletores_encontrados[seletor] = []
                        seletores_encontrados[seletor].append({
                            'text': elem.get_text()[:100],
                            'attrs': dict(elem.attrs)
                        })
                
                # Verificar ID
                elem_id = elem.get('id', '')
                if elem_id and re.search(pattern, elem_id, re.IGNORECASE):
                    seletor = f"{tag}#{elem_id}"
                    if seletor not in seletores_encontrados:
                        seletores_encontrados[seletor] = []
                    seletores_encontrados[seletor].append({
                        'text': elem.get_text()[:100],
                        'attrs': dict(elem.attrs)
                    })
        
        # Mostrar seletores encontrados
        for seletor, elementos in list(seletores_encontrados.items())[:20]:
            print(f"   ✅ {seletor}: {len(elementos)} elementos")
            if elementos:
                texto_exemplo = elementos[0]['text'].strip()[:50]
                if texto_exemplo:
                    print(f"      Exemplo: '{texto_exemplo}...'")
        
        return seletores_encontrados
    
    def gerar_relatorio(self, analise_resultado):
        """Gera relatório detalhado da análise"""
        print("\n📊 GERANDO RELATÓRIO")
        print("=" * 40)
        
        temp_dir = os.path.join(os.path.dirname(__file__), '..', 'temp')
        
        # Relatório em JSON
        relatorio_json = os.path.join(temp_dir, 'analise_contender.json')
        with open(relatorio_json, 'w', encoding='utf-8') as f:
            json.dump(analise_resultado, f, indent=2, ensure_ascii=False)
        
        # Relatório em Markdown
        relatorio_md = os.path.join(temp_dir, 'relatorio_contender.md')
        
        with open(relatorio_md, 'w', encoding='utf-8') as f:
            f.write("# 📊 RELATÓRIO DE ANÁLISE - MODO CONTENDER\n\n")
            
            f.write("## 🔍 Padrões Encontrados\n\n")
            padroes = analise_resultado.get('padroes', {})
            for pattern, count in sorted(padroes.items(), key=lambda x: x[1], reverse=True):
                f.write(f"- **{pattern}**: {count} ocorrências\n")
            
            f.write("\n## 🎯 Seletores CSS Identificados\n\n")
            seletores = analise_resultado.get('seletores', {})
            for seletor, elementos in seletores.items():
                f.write(f"### `{seletor}`\n")
                f.write(f"- **Quantidade**: {len(elementos)} elementos\n")
                if elementos:
                    exemplo = elementos[0]
                    texto = exemplo.get('text', '').strip()[:100]
                    if texto:
                        f.write(f"- **Exemplo**: {texto}...\n")
                f.write("\n")
            
            f.write("## 💻 Código Sugerido\n\n")
            f.write("```python\n")
            f.write("def modo_contender(self):\n")
            f.write('    """Modo CONTENDER implementado baseado na análise"""\n')
            f.write("    try:\n")
            f.write('        self.driver.get("https://key-drop.com/pt/giveaways/list")\n')
            f.write("        time.sleep(3)\n\n")
            
            # Sugerir seletores mais promissores
            seletores_relevantes = [s for s in seletores.keys() if any(term in s.lower() for term in ['giveaway', 'contest', 'btn', 'participate', 'join'])]
            
            if seletores_relevantes:
                f.write("        # Seletores identificados:\n")
                for seletor in seletores_relevantes[:5]:
                    f.write(f"        # {seletor}\n")
                
                f.write(f"\n        # Exemplo usando {seletores_relevantes[0]}:\n")
                f.write(f'        elementos = self.driver.find_elements(By.CSS_SELECTOR, "{seletores_relevantes[0]}")\n')
                f.write("        \n")
                f.write("        for elemento in elementos:\n")
                f.write("            try:\n")
                f.write("                elemento.click()\n")
                f.write("                time.sleep(1)\n")
                f.write("            except:\n")
                f.write("                continue\n")
            
            f.write("        \n")
            f.write("        return True\n")
            f.write("    except Exception as e:\n")
            f.write("        print(f'Erro: {e}')\n")
            f.write("        return False\n")
            f.write("```\n")
        
        print(f"📊 Relatório JSON: {relatorio_json}")
        print(f"📝 Relatório MD: {relatorio_md}")
        
        return relatorio_md
    
    def executar_analise(self, url="https://key-drop.com/pt/giveaways/list"):
        """Executa análise completa"""
        print("🔍 ANÁLISE SIMPLES DO MODO CONTENDER")
        print("=" * 50)
        
        # Obter HTML
        html_content = self.obter_html_pagina(url)
        if not html_content:
            return False
        
        # Analisar HTML
        analise_resultado = self.analisar_html(html_content)
        if not analise_resultado:
            return False
        
        # Gerar relatório
        relatorio_file = self.gerar_relatorio(analise_resultado)
        
        print("\n" + "=" * 50)
        print("✅ ANÁLISE CONCLUÍDA!")
        print(f"📁 Arquivos gerados em: dev/temp/")
        print("💡 Verifique os relatórios para implementar o modo CONTENDER")
        print("=" * 50)
        
        return True

def main():
    """Função principal"""
    print("🔍 INSPETOR SIMPLES - MODO CONTENDER")
    print("=" * 50)
    print("⚠️ Este script não usa Selenium, apenas analisa o HTML")
    print("📌 Para análise mais detalhada, use a versão com Selenium")
    print()
    
    inspector = ContenderInspectorSimples()
    
    try:
        inspector.executar_analise()
    except KeyboardInterrupt:
        print("\n\n⚠️ Análise interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
