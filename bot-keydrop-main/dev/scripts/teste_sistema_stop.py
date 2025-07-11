#!/usr/bin/env python3
"""
Script para testar o sistema de stop melhorado do KeyDrop Bot
Testa diferentes cenários de encerramento de processos Chrome
"""

import sys
import os
import time
import psutil
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from keydrop_bot import KeyDropBot, BotManager

def listar_processos_chrome():
    """Lista todos os processos Chrome ativos"""
    processos = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                processos.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cmdline': proc.info['cmdline']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processos

def teste_stop_individual():
    """Testa o stop de um bot individual"""
    print("=== TESTE 1: Stop Individual ===")
    
    # Listar processos Chrome antes
    processos_antes = listar_processos_chrome()
    print(f"Processos Chrome antes: {len(processos_antes)}")
    
    # Criar e iniciar 1 bot
    bot = KeyDropBot("c:\\temp\\test_profile_1", 1, headless=True)
    if bot.criar_driver():
        print("✅ Bot criado com sucesso")
        
        # Aguardar um pouco
        time.sleep(3)
        
        # Listar processos Chrome após criação
        processos_meio = listar_processos_chrome()
        print(f"Processos Chrome após criação: {len(processos_meio)}")
        
        # Parar bot
        print("Parando bot...")
        bot.parar()
        
        # Aguardar limpeza
        time.sleep(5)
        
        # Listar processos Chrome após parada
        processos_depois = listar_processos_chrome()
        print(f"Processos Chrome após parada: {len(processos_depois)}")
        
        # Verificar se limpou
        if len(processos_depois) <= len(processos_antes):
            print("✅ Stop individual funcionando corretamente")
        else:
            print("❌ Stop individual deixou processos órfãos")
    else:
        print("❌ Falha ao criar bot")

def teste_stop_multiplos():
    """Testa o stop de múltiplos bots"""
    print("\n=== TESTE 2: Stop Múltiplos Bots ===")
    
    # Listar processos Chrome antes
    processos_antes = listar_processos_chrome()
    print(f"Processos Chrome antes: {len(processos_antes)}")
    
    # Criar manager e bots
    manager = BotManager()
    manager.criar_bots(3, headless=True)
    
    # Iniciar bots com velocidade rápida
    config = manager.carregar_config()
    config['velocidade_navegacao'] = 1
    manager.salvar_config(config)
    
    print("Iniciando 3 bots...")
    threads = manager.iniciar_todos(300)  # 5 minutos
    
    # Aguardar um pouco
    time.sleep(10)
    
    # Listar processos Chrome após criação
    processos_meio = listar_processos_chrome()
    print(f"Processos Chrome após criação: {len(processos_meio)}")
    
    # Parar todos os bots
    print("Parando todos os bots...")
    manager.parar_todos("Teste")
    
    # Aguardar limpeza
    time.sleep(10)
    
    # Listar processos Chrome após parada
    processos_depois = listar_processos_chrome()
    print(f"Processos Chrome após parada: {len(processos_depois)}")
    
    # Verificar se limpou
    if len(processos_depois) <= len(processos_antes):
        print("✅ Stop múltiplos bots funcionando corretamente")
    else:
        print("❌ Stop múltiplos bots deixou processos órfãos")

def teste_stop_emergencia():
    """Testa o stop de emergência"""
    print("\n=== TESTE 3: Stop Emergência ===")
    
    # Listar processos Chrome antes
    processos_antes = listar_processos_chrome()
    print(f"Processos Chrome antes: {len(processos_antes)}")
    
    # Criar manager e bots
    manager = BotManager()
    manager.criar_bots(2, headless=True)
    
    print("Iniciando 2 bots...")
    threads = manager.iniciar_todos(300)
    
    # Aguardar um pouco
    time.sleep(5)
    
    # Listar processos Chrome após criação
    processos_meio = listar_processos_chrome()
    print(f"Processos Chrome após criação: {len(processos_meio)}")
    
    # Usar stop de emergência
    print("Executando stop de emergência...")
    processos_encerrados = manager.encerrar_chrome_emergencia()
    print(f"Processos encerrados: {processos_encerrados}")
    
    # Aguardar limpeza
    time.sleep(5)
    
    # Listar processos Chrome após parada
    processos_depois = listar_processos_chrome()
    print(f"Processos Chrome após parada: {len(processos_depois)}")
    
    # Verificar se limpou
    if len(processos_depois) <= len(processos_antes):
        print("✅ Stop emergência funcionando corretamente")
    else:
        print("❌ Stop emergência deixou processos órfãos")

def teste_deteccao_orfaos():
    """Testa a detecção de processos órfãos"""
    print("\n=== TESTE 4: Detecção de Órfãos ===")
    
    # Criar bot
    bot = KeyDropBot("c:\\temp\\test_profile_orphan", 99, headless=True)
    if bot.criar_driver():
        print("✅ Bot criado")
        
        # Simular crash (não usar parar normal)
        print("Simulando crash...")
        bot.driver = None  # Simular perda de referência
        
        # Aguardar um pouco
        time.sleep(3)
        
        # Tentar limpar órfãos
        print("Limpando órfãos...")
        bot._encerrar_chrome_orfaos()
        
        print("✅ Teste de detecção de órfãos concluído")
    else:
        print("❌ Falha ao criar bot")

if __name__ == "__main__":
    print("🧪 Iniciando testes do sistema de stop melhorado")
    print("=" * 60)
    
    try:
        # Executar testes
        teste_stop_individual()
        teste_stop_multiplos()
        teste_stop_emergencia()
        teste_deteccao_orfaos()
        
        print("\n" + "=" * 60)
        print("✅ Todos os testes concluídos!")
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
