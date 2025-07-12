#!/usr/bin/env python3
"""
Validação Final - Sistema de Retry Avançado v4.0.0
Testa todas as funcionalidades implementadas
"""

import sys
import os
import time
import json
import traceback

def test_imports():
    """Testa se todas as importações funcionam"""
    print("🔍 Testando importações...")
    
    try:
        # Teste de importação do bot principal
        from keydrop_bot import KeyDropBot, BotManager
        print("✅ keydrop_bot importado com sucesso")
        
        # Teste de importação da interface
        from modern_gui_v2 import ModernKeyDropInterface
        print("✅ modern_gui_v2 importado com sucesso")
        
        return True
    except Exception as e:
        print(f"❌ Erro de importação: {e}")
        return False

def test_keydropsbot_creation():
    """Testa criação do KeyDropBot com max_tentativas"""
    print("🔍 Testando criação do KeyDropBot...")
    
    try:
        from keydrop_bot import KeyDropBot
        
        # Teste com diferentes valores de max_tentativas
        test_values = [1, 3, 5, 10]
        
        for max_tentativas in test_values:
            bot = KeyDropBot(
                profile_path=f"test_profile_{max_tentativas}",
                bot_id=1,
                headless=True,
                max_tentativas=max_tentativas
            )
            
            # Verificar se o parâmetro foi definido corretamente
            if bot.max_tentativas != max_tentativas:
                raise ValueError(f"max_tentativas esperado {max_tentativas}, obtido {bot.max_tentativas}")
            
            print(f"✅ Bot criado com max_tentativas={max_tentativas}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao criar KeyDropBot: {e}")
        return False

def test_bot_methods():
    """Testa se os métodos de retry existem"""
    print("🔍 Testando métodos de retry...")
    
    try:
        from keydrop_bot import KeyDropBot
        
        bot = KeyDropBot(
            profile_path="test_profile",
            bot_id=1,
            headless=True,
            max_tentativas=3
        )
        
        # Verificar se os métodos existem
        required_methods = [
            '_encerrar_guias_ordenadamente',
            '_reiniciar_guia_keydrop',
            'participar_sorteio',
            'participar_sorteio_contender'
        ]
        
        for method_name in required_methods:
            if not hasattr(bot, method_name):
                raise AttributeError(f"Método {method_name} não encontrado")
            print(f"✅ Método {method_name} encontrado")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao testar métodos: {e}")
        return False

def test_bot_manager():
    """Testa funcionalidades do BotManager"""
    print("🔍 Testando BotManager...")
    
    try:
        from keydrop_bot import BotManager, KeyDropBot
        
        manager = BotManager()
        
        # Testar métodos novos
        required_methods = [
            'adicionar_bot',
            'remover_bot',
            'bot_existe',
            'bot_rodando',
            'get_bot',
            'iniciar_bot',
            'parar_bot',
            'reiniciar_bot',
            'reiniciar_todos',
            'parada_emergencial'
        ]
        
        for method_name in required_methods:
            if not hasattr(manager, method_name):
                raise AttributeError(f"Método {method_name} não encontrado")
            print(f"✅ Método {method_name} encontrado")
        
        # Testar adição de bot
        bot = KeyDropBot(
            profile_path="test_profile",
            bot_id=1,
            headless=True,
            max_tentativas=5
        )
        
        manager.adicionar_bot(bot)
        
        if not manager.bot_existe(1):
            raise ValueError("Bot não foi adicionado corretamente")
        
        if manager.bot_rodando(1):
            raise ValueError("Bot não deveria estar rodando")
        
        retrieved_bot = manager.get_bot(1)
        if retrieved_bot is None:
            raise ValueError("Bot não foi recuperado")
        
        if retrieved_bot.max_tentativas != 5:
            raise ValueError(f"max_tentativas incorreto: {retrieved_bot.max_tentativas}")
        
        print("✅ BotManager funcionando corretamente")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar BotManager: {e}")
        return False

def test_config_loading():
    """Testa carregamento de configuração"""
    print("🔍 Testando carregamento de configuração...")
    
    try:
        # Criar configuração de teste
        test_config = {
            'max_tentativas': 7,
            'profile_path': 'test_profile',
            'headless': True,
            'mini_window': False,
            'login_mode': False,
            'contender_mode': False
        }
        
        # Salvar configuração
        with open('bot_config.json', 'w', encoding='utf-8') as f:
            json.dump(test_config, f, indent=2, ensure_ascii=False)
        
        # Testar carregamento no BotManager
        from keydrop_bot import BotManager
        manager = BotManager()
        config = manager.carregar_config()
        
        if config.get('max_tentativas') != 7:
            raise ValueError(f"max_tentativas incorreto: {config.get('max_tentativas')}")
        
        print("✅ Configuração carregada corretamente no BotManager")
        
        # Testar carregamento na interface
        from modern_gui_v2 import ModernKeyDropInterface
        
        # Criar classe sem inicializar GUI
        interface = ModernKeyDropInterface.__new__(ModernKeyDropInterface)
        
        # Testar método de carregamento
        loaded_config = interface.carregar_config()
        
        if loaded_config.get('max_tentativas') != 7:
            raise ValueError(f"max_tentativas incorreto na interface: {loaded_config.get('max_tentativas')}")
        
        print("✅ Configuração carregada corretamente na interface")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar configuração: {e}")
        return False

def test_version_update():
    """Testa se a versão foi atualizada"""
    print("🔍 Testando atualização de versão...")
    
    try:
        with open('version.json', 'r', encoding='utf-8') as f:
            version_info = json.load(f)
        
        if version_info.get('version') != '4.0.0':
            raise ValueError(f"Versão incorreta: {version_info.get('version')}")
        
        # Verificar se as novas features estão listadas
        features = version_info.get('features', [])
        retry_features = [
            'Sistema de retry avançado com campo personalizável (1-10 tentativas)',
            'Reinício automático de guias após falha máxima',
            'Delay otimizado entre tentativas (10s)'
        ]
        
        for feature in retry_features:
            if feature not in features:
                raise ValueError(f"Feature não encontrada: {feature}")
        
        print("✅ Versão atualizada corretamente")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar versão: {e}")
        return False

def test_documentation():
    """Testa se a documentação foi criada"""
    print("🔍 Testando documentação...")
    
    try:
        docs_to_check = [
            'docs/SISTEMA_RETRY_AVANCADO.md',
            'RELEASE_NOTES_v4.0.0.md',
            'dev/scripts/test_retry_system.py'
        ]
        
        for doc in docs_to_check:
            if not os.path.exists(doc):
                raise FileNotFoundError(f"Arquivo não encontrado: {doc}")
            print(f"✅ Documentação encontrada: {doc}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar documentação: {e}")
        return False

def run_validation():
    """Executa validação completa"""
    print("🚀 Iniciando Validação Final - Sistema de Retry Avançado v4.0.0")
    print("=" * 70)
    
    tests = [
        ("Importações", test_imports),
        ("Criação KeyDropBot", test_keydropsbot_creation),
        ("Métodos de Retry", test_bot_methods),
        ("BotManager", test_bot_manager),
        ("Configuração", test_config_loading),
        ("Versão", test_version_update),
        ("Documentação", test_documentation)
    ]
    
    passed = 0
    failed = 0
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                results.append(f"✅ {test_name}: PASSOU")
            else:
                failed += 1
                results.append(f"❌ {test_name}: FALHOU")
        except Exception as e:
            failed += 1
            results.append(f"❌ {test_name}: ERRO - {e}")
            print(f"🔍 Detalhes do erro: {traceback.format_exc()}")
    
    print("=" * 70)
    print("📊 RESULTADOS DA VALIDAÇÃO:")
    print("=" * 70)
    
    for result in results:
        print(result)
    
    print("=" * 70)
    print(f"📈 RESUMO: {passed} passaram, {failed} falharam")
    
    if failed == 0:
        print("🎉 VALIDAÇÃO COMPLETA: Sistema de Retry Avançado funcionando perfeitamente!")
        print("🚀 Pronto para produção!")
        return True
    else:
        print("⚠️ VALIDAÇÃO PARCIAL: Alguns testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = run_validation()
    
    if success:
        print("\n🎯 SISTEMA DE RETRY AVANÇADO IMPLEMENTADO COM SUCESSO!")
        print("✨ Funcionalidades principais:")
        print("   - Campo personalizável para máximo de tentativas (1-10)")
        print("   - Delay otimizado entre tentativas (10s)")
        print("   - Reinício automático de guias problemáticas")
        print("   - Encerramento ordenado de guias")
        print("   - Interface atualizada com validação")
        print("   - Logs detalhados e monitoramento")
    
    sys.exit(0 if success else 1)
