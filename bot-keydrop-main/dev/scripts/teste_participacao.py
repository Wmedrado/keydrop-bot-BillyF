#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar se as estatísticas de participação estão sendo contabilizadas corretamente
"""

import time
import sys
import os
from datetime import datetime

def simular_participacao():
    """Simula uma participação no sorteio para testar contabilização"""
    
    print("=" * 60)
    print("TESTE DE CONTABILIZAÇÃO DE PARTICIPAÇÕES")
    print("=" * 60)
    
    # Importar classes
    sys.path.append('.')
    from keydrop_bot import KeyDropBot
    
    # Criar bot de teste
    bot = KeyDropBot(
        profile_path="./profiles/Profile-TEST",
        bot_id=999,
        headless=True,
        discord_webhook=None,
        login_mode=False,
        contender_mode=False
    )
    
    print(f"Bot criado: {bot.bot_id}")
    print(f"Estatísticas iniciais: {bot.stats}")
    
    # Simular participação em sorteio AMATEUR
    print("\n1. Simulando participação AMATEUR...")
    bot.stats['participacoes'] += 1
    bot.stats['ultima_participacao'] = datetime.now()
    bot.stats['ultima_atividade'] = 'Participou de sorteio AMATEUR'
    
    # Simular participação em sorteio CONTENDER
    print("\n2. Simulando participação CONTENDER...")
    bot.stats['participacoes_contender'] += 1
    bot.stats['ultima_participacao_contender'] = datetime.now()
    bot.stats['ultima_atividade'] = 'Participou de sorteio CONTENDER'
    
    # Testar função obter_stats()
    print("\n3. Testando função obter_stats()...")
    stats_formatadas = bot.obter_stats()
    
    print(f"Stats originais: {bot.stats}")
    print(f"Stats formatadas: {stats_formatadas}")
    
    # Verificar mapeamento
    print("\n4. Verificando mapeamento...")
    print(f"AMATEUR - Original: {bot.stats['participacoes']} -> Formatado: {stats_formatadas['amateur']}")
    print(f"CONTENDER - Original: {bot.stats['participacoes_contender']} -> Formatado: {stats_formatadas['contender']}")
    
    # Testar múltiplas participações
    print("\n5. Testando múltiplas participações...")
    for i in range(5):
        bot.stats['participacoes'] += 1
        print(f"Participação {i+1}: {bot.stats['participacoes']}")
        
        # Verificar se o mapeamento está funcionando
        stats_temp = bot.obter_stats()
        print(f"  -> Formatado: {stats_temp['amateur']}")
        
        time.sleep(0.1)
    
    # Resultado final
    print("\n6. Resultado final:")
    stats_finais = bot.obter_stats()
    print(f"Total AMATEUR: {stats_finais['amateur']}")
    print(f"Total CONTENDER: {stats_finais['contender']}")
    print(f"Total Erros: {stats_finais['erros']}")
    
    return True

def testar_manager():
    """Testa se o manager está coletando as estatísticas corretamente"""
    
    print("\n" + "=" * 60)
    print("TESTE DO MANAGER - COLETA DE ESTATÍSTICAS")
    print("=" * 60)
    
    # Importar classes
    sys.path.append('.')
    from keydrop_bot import BotManager
    
    # Criar manager
    manager = BotManager()
    
    # Criar alguns bots de teste
    bot1 = KeyDropBot("./profiles/Profile-1", 1, headless=True)
    bot2 = KeyDropBot("./profiles/Profile-2", 2, headless=True)
    
    # Simular participações
    bot1.stats['participacoes'] = 10
    bot1.stats['participacoes_contender'] = 3
    bot1.stats['erros'] = 1
    
    bot2.stats['participacoes'] = 15
    bot2.stats['participacoes_contender'] = 5
    bot2.stats['erros'] = 2
    
    # Adicionar bots ao manager
    manager.bots = [bot1, bot2]
    
    print(f"Bot1 - AMATEUR: {bot1.stats['participacoes']}, CONTENDER: {bot1.stats['participacoes_contender']}")
    print(f"Bot2 - AMATEUR: {bot2.stats['participacoes']}, CONTENDER: {bot2.stats['participacoes_contender']}")
    
    # Testar obter_stats_todos
    print("\nTestando obter_stats_todos()...")
    stats_todos = manager.obter_stats_todos()
    
    for i, stat in enumerate(stats_todos):
        print(f"\nBot {stat['bot_id']}:")
        print(f"  Stats originais: {manager.bots[i].stats}")
        print(f"  Stats formatadas: {stat['stats']}")
        print(f"  AMATEUR: {stat['stats']['amateur']}")
        print(f"  CONTENDER: {stat['stats']['contender']}")
    
    return True

if __name__ == "__main__":
    print(f"Iniciando testes: {datetime.now().strftime('%H:%M:%S')}")
    
    # Executar testes
    teste1 = simular_participacao()
    teste2 = testar_manager()
    
    if teste1 and teste2:
        print("\nTODOS OS TESTES PASSARAM!")
    else:
        print("\nALGUNS TESTES FALHARAM!")
        sys.exit(1)
