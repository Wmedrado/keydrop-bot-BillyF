#!/usr/bin/env python3
"""
Teste direto do sistema de stop melhorado
"""

import os
import sys
import time
import psutil

# Funcão para contar processos Chrome
def contar_chrome():
    count = 0
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return count

if __name__ == "__main__":
    print("=== TESTE DIRETO DO SISTEMA DE STOP ===")
    
    # Contar processos Chrome antes
    antes = contar_chrome()
    print(f"📊 Processos Chrome antes: {antes}")
    
    # Importar o módulo do bot
    exec(open("keydrop_bot.py").read())
    
    # Criar bot
    print("🚀 Criando bot...")
    bot = KeyDropBot("c:\\temp\\test_profile_direct", 1, headless=True)
    
    # Tentar criar driver
    if bot.criar_driver():
        print("✅ Bot criado com sucesso")
        
        # Aguardar um pouco
        time.sleep(2)
        
        # Contar processos Chrome após criação
        meio = contar_chrome()
        print(f"📊 Processos Chrome após criação: {meio}")
        
        # Parar bot
        print("⏹️ Parando bot...")
        bot.parar()
        
        # Aguardar limpeza
        time.sleep(3)
        
        # Contar processos Chrome após parada
        depois = contar_chrome()
        print(f"📊 Processos Chrome após parada: {depois}")
        
        # Verificar resultado
        if depois <= antes:
            print("✅ Sistema de stop funcionando corretamente!")
        else:
            print("⚠️ Alguns processos podem ter ficado órfãos")
            
    else:
        print("❌ Falha ao criar bot")
        
    print("\n=== TESTE CONCLUÍDO ===")
