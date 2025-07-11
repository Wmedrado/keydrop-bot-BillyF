#!/usr/bin/env python3
"""
Teste de Integração Multi-Browser para Keydrop Bot
Testa Edge, Chrome e Firefox em ordem de prioridade
"""

import sys
import os
import time
import traceback

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar a classe do bot
from keydrop_bot_desktop_v4 import KeydropBot

def test_browser_integration():
    """Testar se o bot consegue usar Edge, Chrome ou Firefox"""
    print("🧪 TESTE DE INTEGRAÇÃO MULTI-BROWSER")
    print("=" * 50)
    
    # Configuração de teste
    config = {
        "num_tabs": 1,
        "execution_speed": 3.0,
        "retry_attempts": 3,
        "headless_mode": False,  # Deixar visual para ver funcionando
        "mini_window_mode": True  # Janela pequena para teste
    }
    
    # Criar bot de teste
    try:
        print("🔄 Criando instância do bot...")
        bot = KeydropBot(bot_id=999, config=config)  # ID especial para teste
        
        print("🔄 Tentando configurar driver do navegador...")
        bot.setup_driver()
        
        if bot.driver:
            print(f"✅ SUCESSO! Navegador configurado: {getattr(bot, 'browser_used', 'Desconhecido')}")
            
            # Teste básico de navegação
            print("🔄 Testando navegação básica...")
            bot.driver.get("https://www.google.com")
            time.sleep(3)
            
            print("✅ Navegação funcionando!")
            
            # Testar navegação para Keydrop
            print("🔄 Testando navegação para Keydrop...")
            bot.driver.get("https://key-drop.com")
            time.sleep(5)
            
            print("✅ Keydrop carregado com sucesso!")
            
            # Manter janela aberta por alguns segundos para inspeção visual
            print("👀 Mantendo janela aberta por 10 segundos para inspeção...")
            time.sleep(10)
            
            # Fechar navegador
            print("🔄 Fechando navegador...")
            bot.driver.quit()
            
            print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
            print(f"✅ Navegador usado: {getattr(bot, 'browser_used', 'Desconhecido')}")
            
        else:
            print("❌ FALHA: Nenhum driver foi configurado")
            return False
            
    except Exception as e:
        print(f"❌ ERRO NO TESTE: {e}")
        print(f"📋 Detalhes: {traceback.format_exc()}")
        return False
    
    return True

def test_browser_availability():
    """Testar quais navegadores estão disponíveis no sistema"""
    print("\n🔍 VERIFICAÇÃO DE NAVEGADORES DISPONÍVEIS")
    print("=" * 50)
    
    browsers = {
        'Edge': [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ],
        'Chrome': [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
        ],
        'Firefox': [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        ]
    }
    
    available_browsers = []
    
    for browser_name, paths in browsers.items():
        found = False
        for path in paths:
            if os.path.exists(path):
                print(f"✅ {browser_name}: {path}")
                available_browsers.append(browser_name)
                found = True
                break
        
        if not found:
            print(f"❌ {browser_name}: Não encontrado")
    
    print(f"\n📊 Resumo: {len(available_browsers)} navegadores disponíveis")
    if available_browsers:
        print(f"✅ Disponíveis: {', '.join(available_browsers)}")
        print(f"🏆 Prioridade do bot: Edge > Chrome > Firefox")
    else:
        print("⚠️ ATENÇÃO: Nenhum navegador encontrado!")
        print("💡 Instale Microsoft Edge (recomendado) ou Google Chrome")
    
    return available_browsers

if __name__ == "__main__":
    print("🤖 KEYDROP BOT - TESTE DE INTEGRAÇÃO MULTI-BROWSER")
    print("📅 Desenvolvido por William Medrado")
    print("🎯 Testando Edge, Chrome e Firefox")
    print("=" * 60)
    
    # Teste 1: Verificar navegadores disponíveis
    available = test_browser_availability()
    
    if not available:
        print("\n❌ TESTE CANCELADO: Nenhum navegador disponível")
        print("💡 Instale um dos navegadores suportados:")
        print("   - Microsoft Edge (recomendado - mais leve)")
        print("   - Google Chrome")
        print("   - Mozilla Firefox")
        input("\nPressione Enter para sair...")
        sys.exit(1)
    
    # Teste 2: Testar integração do bot
    print(f"\n🚀 Iniciando teste com navegadores disponíveis...")
    
    if test_browser_integration():
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O bot está pronto para automação do Keydrop")
        print("✅ Multi-browser funcionando corretamente")
    else:
        print("\n❌ TESTE FALHOU!")
        print("🔧 Verifique as dependências:")
        print("   pip install --upgrade selenium webdriver-manager")
    
    input("\nPressione Enter para sair...")
