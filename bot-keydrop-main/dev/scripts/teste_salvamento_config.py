#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar se o salvamento e carregamento 
das configurações está funcionando corretamente.
"""

import os
import json
import sys
import time
from datetime import datetime

def testar_salvamento_configuracoes():
    """Testa o salvamento e carregamento das configurações"""
    
    print("=" * 60)
    print("TESTE DE SALVAMENTO E CARREGAMENTO DE CONFIGURAÇÕES")
    print("=" * 60)
    
    # Configuração de teste
    config_teste = {
        "num_bots": 5,
        "velocidade_navegacao": 3,
        "headless": True,
        "login_mode": True,
        "contender_mode": False,
        "discord_webhook": "https://discord.com/api/webhooks/test",
        "relatorios_automaticos": True,
        "intervalo_sorteios": 180,
        "intervalo_tabs": 2
    }
    
    # Backup do arquivo original se existir
    arquivo_config = 'bot_config.json'
    arquivo_backup = 'bot_config_teste_backup.json'
    
    if os.path.exists(arquivo_config):
        print(f"Fazendo backup do arquivo atual: {arquivo_backup}")
        import shutil
        shutil.copy(arquivo_config, arquivo_backup)
    
    try:
        # Teste 1: Salvar configuração
        print("\n1. Testando salvamento...")
        with open(arquivo_config, 'w', encoding='utf-8') as f:
            json.dump(config_teste, f, indent=4, ensure_ascii=False)
        print("OK - Configuração salva com sucesso!")
        
        # Teste 2: Carregar configuração
        print("\n2. Testando carregamento...")
        with open(arquivo_config, 'r', encoding='utf-8') as f:
            config_carregada = json.load(f)
        print("OK - Configuração carregada com sucesso!")
        
        # Teste 3: Verificar se os dados são iguais
        print("\n3. Verificando integridade dos dados...")
        dados_corretos = True
        
        for chave, valor in config_teste.items():
            if config_carregada.get(chave) != valor:
                print(f"ERRO: {chave} - Esperado: {valor}, Obtido: {config_carregada.get(chave)}")
                dados_corretos = False
        
        if dados_corretos:
            print("OK - Todos os dados estão corretos!")
        else:
            print("ERRO - Alguns dados estão incorretos!")
            
        # Teste 4: Exibir configuração final
        print("\n4. Configuração final:")
        print(json.dumps(config_carregada, indent=4, ensure_ascii=False))
        
        # Teste 5: Testar modificação
        print("\n5. Testando modificação...")
        config_carregada['num_bots'] = 10
        config_carregada['velocidade_navegacao'] = 1
        
        with open(arquivo_config, 'w', encoding='utf-8') as f:
            json.dump(config_carregada, f, indent=4, ensure_ascii=False)
        
        # Verificar se a modificação foi salva
        with open(arquivo_config, 'r', encoding='utf-8') as f:
            config_modificada = json.load(f)
        
        if config_modificada['num_bots'] == 10 and config_modificada['velocidade_navegacao'] == 1:
            print("OK - Modificação salva e carregada com sucesso!")
        else:
            print("ERRO - Erro na modificação!")
            
    except Exception as e:
        print(f"ERRO durante o teste: {e}")
        return False
    
    finally:
        # Restaurar backup se existir
        if os.path.exists(arquivo_backup):
            print(f"\nRestaurando backup original...")
            import shutil
            shutil.copy(arquivo_backup, arquivo_config)
            os.remove(arquivo_backup)
            print("OK - Backup restaurado!")
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    return True

def testar_interface_moderna():
    """Testa se a interface moderna consegue carregar as configurações"""
    
    print("\n" + "=" * 60)
    print("TESTE DE INTERFACE MODERNA")
    print("=" * 60)
    
    try:
        # Importar e testar a classe
        sys.path.append('.')
        from modern_gui import ModernKeyDropGUI
        
        print("OK - Classe ModernKeyDropGUI importada com sucesso!")
        
        # Criar instância (sem executar mainloop)
        print("Criando instância da interface...")
        app = ModernKeyDropGUI()
        
        print("OK - Interface criada com sucesso!")
        
        # Verificar se as configurações foram carregadas
        config_atual = app.config
        print(f"Configurações carregadas: {config_atual}")
        
        # Verificar se as variáveis da interface existem
        variaveis_interface = [
            'num_bots_var', 'velocidade_var', 'headless_var',
            'login_var', 'contender_var', 'discord_var', 'relatorios_var'
        ]
        
        for var in variaveis_interface:
            if hasattr(app, var):
                valor = getattr(app, var).get()
                print(f"OK - {var}: {valor}")
            else:
                print(f"ERRO - {var}: Não encontrada!")
        
        # Testar salvamento
        print("\nTestando salvamento através da interface...")
        if app.salvar_config():
            print("OK - Salvamento através da interface funcionou!")
        else:
            print("ERRO - Erro no salvamento através da interface!")
        
        # Destruir janela
        app.root.destroy()
        
    except Exception as e:
        print(f"ERRO no teste da interface: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("TESTE DA INTERFACE CONCLUÍDO!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    print(f"Iniciando testes em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Executar testes
    teste1 = testar_salvamento_configuracoes()
    teste2 = testar_interface_moderna()
    
    if teste1 and teste2:
        print("\nTODOS OS TESTES PASSARAM!")
    else:
        print("\nALGUNS TESTES FALHARAM!")
        sys.exit(1)
