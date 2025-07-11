#!/usr/bin/env python3
"""
Teste simples do sistema de stop melhorado
"""

import sys
import os
import time
import psutil

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar o módulo do bot
import keydrop_bot
from keydrop_bot import KeyDropBot

def contar_processos_chrome():
    """Conta processos Chrome"""
    count = 0
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return count

def teste_rapido():
    """Teste rápido do sistema"""
    print("=== TESTE SIMPLES DO SISTEMA DE STOP ===")
    
    # Contar processos Chrome antes
    antes = contar_processos_chrome()
    print(f"📊 Processos Chrome antes: {antes}")
    
    # Criar diretório de teste
    test_dir = "c:\\temp\\test_profile_simple"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # Criar bot
    print("🚀 Criando bot...")
    bot = KeyDropBot(test_dir, 1, headless=True)
    
    # Tentar criar driver
    if bot.criar_driver():
        print("✅ Bot criado com sucesso")
        
        # Aguardar um pouco
        time.sleep(2)
        
        # Contar processos Chrome após criação
        meio = contar_processos_chrome()
        print(f"📊 Processos Chrome após criação: {meio}")
        
        # Parar bot
        print("⏹️ Parando bot...")
        bot.parar()
        
        # Aguardar limpeza
        time.sleep(3)
        
        # Contar processos Chrome após parada
        depois = contar_processos_chrome()
        print(f"📊 Processos Chrome após parada: {depois}")
        
        # Verificar resultado
        if depois <= antes:
            print("✅ Sistema de stop funcionando corretamente!")
        else:
            print("⚠️ Alguns processos podem ter ficado órfãos")
            
    else:
        print("❌ Falha ao criar bot")

if __name__ == "__main__":
    try:
        teste_rapido()
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
