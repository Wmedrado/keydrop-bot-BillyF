#!/usr/bin/env python3
"""
Teste rápido da automação Keydrop Bot v4.0.0
"""

import sys
import os

def test_selenium():
    """Testar se Selenium está funcionando"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        print("✅ Selenium importado com sucesso")
        
        # Testar criação do driver
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ ChromeDriver criado com sucesso")
        
        # Testar navegação
        driver.get("https://www.google.com")
        print("✅ Navegação web funcionando")
        
        driver.quit()
        print("✅ Driver fechado corretamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no Selenium: {e}")
        return False

def test_tkinter():
    """Testar se Tkinter está funcionando"""
    try:
        import tkinter as tk
        print("✅ Tkinter importado com sucesso")
        
        # Testar criação de janela
        root = tk.Tk()
        root.withdraw()  # Não mostrar
        root.destroy()
        print("✅ Interface gráfica funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no Tkinter: {e}")
        return False

def test_dependencies():
    """Testar outras dependências"""
    try:
        import requests
        import psutil
        import json
        import threading
        import datetime
        print("✅ Todas as dependências importadas")
        
        # Testar requests
        response = requests.get("https://httpbin.org/get", timeout=5)
        if response.status_code == 200:
            print("✅ Requisições HTTP funcionando")
        
        # Testar psutil
        cpu = psutil.cpu_percent()
        print(f"✅ Monitoramento de sistema funcionando (CPU: {cpu}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nas dependências: {e}")
        return False

def main():
    print("🤖 Keydrop Bot Professional v4.0.0 - Teste de Sistema")
    print("=" * 60)
    print()
    
    tests = [
        ("Interface Gráfica (Tkinter)", test_tkinter),
        ("Dependências Básicas", test_dependencies),
        ("Automação Web (Selenium)", test_selenium),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"🔍 Testando {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name}: OK")
        else:
            print(f"❌ {test_name}: FALHOU")
        print()
    
    print("=" * 60)
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 SISTEMA PRONTO PARA AUTOMAÇÃO COMPLETA!")
        print("✅ Execute KeydropBot_v4.0.0_AUTO.exe")
        print("✅ Configure suas preferências")
        print("✅ Marque 'Participar Sorteios 1h' se desejar")
        print("✅ Clique em 'INICIAR AUTOMAÇÃO'")
    elif passed >= 2:
        print("⚠️  SISTEMA PARCIALMENTE FUNCIONAL")
        print("✅ Interface e funcionalidades básicas OK")
        if not test_selenium():
            print("❌ Automação de sorteios não disponível")
            print("💡 Execute: instalar_dependencias.bat")
            print("💡 Ou use modo Edge básico")
    else:
        print("❌ SISTEMA COM PROBLEMAS")
        print("💡 Verifique a instalação do Python")
        print("💡 Execute: pip install -r requirements.txt")
    
    print()
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
