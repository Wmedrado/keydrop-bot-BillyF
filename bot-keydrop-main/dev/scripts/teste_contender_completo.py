#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste completo do modo CONTENDER com logs detalhados
👨‍💻 Desenvolvido por: Billy Franck (wmedrado)
📞 Discord: wmedrado
"""

import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Configuração de log
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

class TestadorContender:
    """Classe para testar o modo CONTENDER"""
    
    def __init__(self):
        self.log_file = LOG_DIR / f"teste_contender_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.resultados = {
            'inicio': datetime.now().isoformat(),
            'etapas': [],
            'erros': [],
            'sucesso': False
        }
    
    def log(self, mensagem, nivel="INFO"):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{nivel}] {mensagem}"
        
        print(log_entry)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
        
        self.resultados['etapas'].append({
            'timestamp': timestamp,
            'nivel': nivel,
            'mensagem': mensagem
        })
    
    def verificar_dependencias(self):
        """Verifica se todas as dependências estão instaladas"""
        self.log("🔍 Verificando dependências...")
        
        try:
            import selenium
            self.log(f"✅ Selenium: {selenium.__version__}")
        except ImportError:
            self.log("❌ Selenium não está instalado", "ERROR")
            return False
        
        try:
            from selenium import webdriver
            self.log("✅ WebDriver importado com sucesso")
        except ImportError:
            self.log("❌ WebDriver não pode ser importado", "ERROR")
            return False
        
        # Verificar ChromeDriver
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(options=options)
            driver.quit()
            self.log("✅ ChromeDriver está funcionando")
        except Exception as e:
            self.log(f"❌ ChromeDriver não está funcionando: {e}", "ERROR")
            return False
        
        return True
    
    def verificar_profiles(self):
        """Verifica se os profiles do Chrome existem"""
        self.log("🔍 Verificando profiles...")
        
        profiles_dir = Path(__file__).parent.parent.parent / "profiles"
        
        if not profiles_dir.exists():
            self.log("❌ Diretório de profiles não encontrado", "ERROR")
            return False
        
        profiles = list(profiles_dir.glob("Profile-*"))
        
        if not profiles:
            self.log("❌ Nenhum profile encontrado", "ERROR")
            return False
        
        self.log(f"✅ Encontrados {len(profiles)} profiles")
        
        # Verificar se pelo menos um profile tem dados
        for profile in profiles:
            if (profile / "Preferences").exists():
                self.log(f"✅ Profile válido encontrado: {profile.name}")
                return True
        
        self.log("❌ Nenhum profile válido encontrado", "ERROR")
        return False
    
    def testar_importacao_contender(self):
        """Testa a importação do script contender"""
        self.log("🔍 Testando importação do script contender...")
        
        try:
            from contender_corrigido import ContenderBot
            self.log("✅ Script contender importado com sucesso")
            return True
        except Exception as e:
            self.log(f"❌ Erro ao importar script contender: {e}", "ERROR")
            return False
    
    def testar_inicializacao_bot(self):
        """Testa a inicialização do bot"""
        self.log("🔍 Testando inicialização do bot...")
        
        try:
            from contender_corrigido import ContenderBot
            
            # Encontrar um profile válido
            profiles_dir = Path(__file__).parent.parent.parent / "profiles"
            profile_path = None
            
            for profile in profiles_dir.glob("Profile-*"):
                if (profile / "Preferences").exists():
                    profile_path = str(profile)
                    break
            
            if not profile_path:
                self.log("❌ Nenhum profile válido encontrado", "ERROR")
                return False
            
            self.log(f"📁 Usando profile: {profile_path}")
            
            # Inicializar bot
            bot = ContenderBot()
            
            # Testar inicialização (sem executar)
            self.log("✅ Bot inicializado com sucesso")
            return True
            
        except Exception as e:
            self.log(f"❌ Erro ao inicializar bot: {e}", "ERROR")
            return False
    
    def testar_acesso_site(self):
        """Testa o acesso ao site KeyDrop"""
        self.log("🔍 Testando acesso ao site KeyDrop...")
        
        try:
            from contender_corrigido import ContenderBot
            
            # Encontrar um profile válido
            profiles_dir = Path(__file__).parent.parent.parent / "profiles"
            profile_path = None
            
            for profile in profiles_dir.glob("Profile-*"):
                if (profile / "Preferences").exists():
                    profile_path = str(profile)
                    break
            
            if not profile_path:
                self.log("❌ Nenhum profile válido encontrado", "ERROR")
                return False
            
            bot = ContenderBot()
            
            # Tentar inicializar e acessar site
            if bot.inicializar(profile_path):
                self.log("✅ Bot inicializado com sucesso")
                
                # Testar acesso à página principal
                bot.driver.get("https://key-drop.com/")
                time.sleep(3)
                
                if "key-drop" in bot.driver.current_url:
                    self.log("✅ Site acessado com sucesso")
                    
                    # Limpar recursos
                    bot.chrome_fixer.limpar_recursos(bot.driver)
                    return True
                else:
                    self.log("❌ Site não foi acessado corretamente", "ERROR")
                    bot.chrome_fixer.limpar_recursos(bot.driver)
                    return False
            else:
                self.log("❌ Falha ao inicializar bot", "ERROR")
                return False
            
        except Exception as e:
            self.log(f"❌ Erro ao testar acesso ao site: {e}", "ERROR")
            return False
    
    def executar_teste_completo(self):
        """Executa todos os testes"""
        self.log("🚀 INICIANDO TESTE COMPLETO DO MODO CONTENDER")
        self.log("=" * 60)
        
        testes = [
            ("Verificação de dependências", self.verificar_dependencias),
            ("Verificação de profiles", self.verificar_profiles),
            ("Importação do script contender", self.testar_importacao_contender),
            ("Inicialização do bot", self.testar_inicializacao_bot),
            ("Acesso ao site", self.testar_acesso_site)
        ]
        
        sucesso_total = 0
        
        for nome, teste in testes:
            self.log(f"\n📋 {nome}...")
            
            try:
                if teste():
                    sucesso_total += 1
                    self.log(f"✅ {nome}: SUCESSO")
                else:
                    self.log(f"❌ {nome}: FALHA", "ERROR")
                    self.resultados['erros'].append(f"{nome}: FALHA")
            except Exception as e:
                self.log(f"❌ {nome}: ERRO - {e}", "ERROR")
                self.resultados['erros'].append(f"{nome}: ERRO - {e}")
        
        self.log("\n" + "=" * 60)
        self.log("📊 RESULTADOS DO TESTE")
        self.log("=" * 60)
        self.log(f"✅ Testes bem-sucedidos: {sucesso_total}/{len(testes)}")
        self.log(f"❌ Testes falhados: {len(testes) - sucesso_total}/{len(testes)}")
        
        if self.resultados['erros']:
            self.log("\n🔍 ERROS ENCONTRADOS:")
            for erro in self.resultados['erros']:
                self.log(f"  • {erro}")
        
        self.resultados['sucesso'] = sucesso_total == len(testes)
        self.resultados['fim'] = datetime.now().isoformat()
        
        # Salvar resultados
        resultado_file = LOG_DIR / f"resultado_teste_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(resultado_file, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        
        self.log(f"\n📄 Log salvo em: {self.log_file}")
        self.log(f"📄 Resultados salvos em: {resultado_file}")
        self.log("=" * 60)
        
        return self.resultados['sucesso']

def main():
    """Função principal"""
    testador = TestadorContender()
    
    try:
        sucesso = testador.executar_teste_completo()
        
        if sucesso:
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            print("O modo CONTENDER está pronto para uso.")
            return 0
        else:
            print("\n⚠️ ALGUNS TESTES FALHARAM!")
            print("Verifique os logs para mais detalhes.")
            return 1
            
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
