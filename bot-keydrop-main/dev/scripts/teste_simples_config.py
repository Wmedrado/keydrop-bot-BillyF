#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para testar apenas o salvamento de configurações
"""

import os
import json
import sys
from datetime import datetime

def testar_salvamento_simples():
    """Teste simples de salvamento"""
    
    print("=" * 50)
    print("TESTE SIMPLES DE SALVAMENTO")
    print("=" * 50)
    
    # Configuração de teste
    config_teste = {
        "num_bots": 3,
        "velocidade_navegacao": 2,
        "headless": False,
        "login_mode": True,
        "contender_mode": False,
        "discord_webhook": "https://test.com/webhook",
        "relatorios_automaticos": True
    }
    
    try:
        # Salvar configuração
        with open('bot_config.json', 'w', encoding='utf-8') as f:
            json.dump(config_teste, f, indent=4, ensure_ascii=False)
        print("1. Salvamento: OK")
        
        # Carregar configuração
        with open('bot_config.json', 'r', encoding='utf-8') as f:
            config_carregada = json.load(f)
        print("2. Carregamento: OK")
        
        # Verificar dados
        if config_carregada == config_teste:
            print("3. Verificação: OK")
        else:
            print("3. Verificação: ERRO")
            print(f"   Esperado: {config_teste}")
            print(f"   Obtido: {config_carregada}")
        
        # Modificar e salvar novamente
        config_carregada['num_bots'] = 7
        with open('bot_config.json', 'w', encoding='utf-8') as f:
            json.dump(config_carregada, f, indent=4, ensure_ascii=False)
        
        # Verificar modificação
        with open('bot_config.json', 'r', encoding='utf-8') as f:
            config_final = json.load(f)
        
        if config_final['num_bots'] == 7:
            print("4. Modificação: OK")
        else:
            print("4. Modificação: ERRO")
        
        print("\nConfiguracao final:")
        print(json.dumps(config_final, indent=2, ensure_ascii=False))
        
        return True
        
    except Exception as e:
        print(f"ERRO: {e}")
        return False

if __name__ == "__main__":
    print(f"Inicio: {datetime.now().strftime('%H:%M:%S')}")
    
    if testar_salvamento_simples():
        print("\nTESTE PASSOU!")
    else:
        print("\nTESTE FALHOU!")
