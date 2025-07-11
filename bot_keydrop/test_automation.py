#!/usr/bin/env python3
"""
Teste simples de automação Chrome para Keydrop Bot
"""

import sys
import time
from pathlib import Path

# Adicionar o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

from keydrop_bot_desktop_v4 import KeydropBot

def test_chrome_automation():
    """Testar automação básica do Chrome"""
    print("🧪 Iniciando teste de automação Chrome...")
    
    try:
        # Criar bot de teste
        config = {
            "num_tabs": 1,
            "execution_speed": 2.0,
            "retry_attempts": 3,
            "headless_mode": False,
            "mini_window_mode": True,
            "auto_restart": False,
            "restart_interval": 30
        }
        
        bot = KeydropBot(1, config)
        print("✅ Bot criado com sucesso")
        
        # Testar configuração do driver
        print("🔧 Configurando driver Chrome...")
        bot.setup_driver()
        print("✅ Driver Chrome configurado")
        
        # Testar navegação
        print("🌐 Navegando para Keydrop...")
        if bot.driver:
            bot.driver.get("https://key-drop.com/pt/")
            time.sleep(3)
            print(f"✅ Página carregada: {bot.driver.title}")
        
        # Testar fechamento de popups
        print("❌ Testando fechamento de popups...")
        bot.close_popups()
        print("✅ Popups fechados")
        
        # Aguardar um pouco para observar
        print("⏳ Aguardando 5 segundos para observação...")
        time.sleep(5)
        
        # Limpar
        print("🧹 Fechando driver...")
        bot.stop()
        print("✅ Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chrome_automation()
