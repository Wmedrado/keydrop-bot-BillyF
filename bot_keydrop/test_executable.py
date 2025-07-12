#!/usr/bin/env python3
"""
Script para testar o executável gerado
"""

import subprocess
import time
import requests
from pathlib import Path

def test_executable():
    """Testa se o executável funciona corretamente"""
    print("🧪 Testando o executável...")
    
    exe_path = Path(__file__).parent / "dist" / "KeydropBot_Professional.exe"
    
    if not exe_path.exists():
        print("❌ Executável não encontrado!")
        return False
    
    print(f"📦 Executável encontrado: {exe_path}")
    print(f"📊 Tamanho: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    
    # Iniciar o executável em background
    print("🚀 Iniciando executável...")
    
    try:
        # Executar o arquivo
        process = subprocess.Popen(
            [str(exe_path)],
            cwd=exe_path.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Aguardar alguns segundos para inicialização
        print("⏳ Aguardando inicialização (10 segundos)...")
        time.sleep(10)
        
        # Testar se o servidor está respondendo
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor respondendo!")
                print(f"📝 Resposta: {response.json()}")
                
                # Testar interface web
                ui_response = requests.get("http://localhost:8000/", timeout=5)
                if ui_response.status_code == 200:
                    print("✅ Interface web funcionando!")
                else:
                    print("⚠️ Interface web com problemas")
                
                # Terminar processo
                process.terminate()
                process.wait(timeout=5)
                
                print("🎉 Teste concluído com sucesso!")
                return True
            else:
                print(f"❌ Servidor não respondeu corretamente: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de conexão: {e}")
        
        # Terminar processo se ainda estiver rodando
        if process.poll() is None:
            process.terminate()
            process.wait(timeout=5)
            
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")
        return False
    
    return False

def create_launch_script():
    """Cria script de lançamento para o usuário"""
    script_content = '''@echo off
title Keydrop Bot Professional v2.1.0
echo.
echo ===============================================
echo   Keydrop Bot Professional v2.1.0
echo   Desenvolvido por: William Medrado (wmedrado)
echo ===============================================
echo.
echo 🚀 Iniciando o bot...
echo.

REM Executar o bot
"%~dp0KeydropBot_Professional.exe"

echo.
echo ⚠️ O bot foi finalizado.
echo 📝 Se houve algum erro, verifique os logs acima.
echo.
pause
'''
    
    script_path = Path(__file__).parent / "dist" / "Iniciar_Bot.bat"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✅ Script de lançamento criado: {script_path}")

if __name__ == "__main__":
    print("🧪 Keydrop Bot Professional - Teste do Executável")
    print("=" * 60)
    
    # Criar script de lançamento
    create_launch_script()
    
    # Testar executável
    if test_executable():
        print("\n✅ Executável testado e funcionando!")
    else:
        print("\n⚠️ Executável pode ter problemas. Verifique os logs.")
    
    print("\n📁 Arquivos disponíveis na pasta dist/:")
    dist_path = Path(__file__).parent / "dist"
    for item in dist_path.iterdir():
        if item.is_file():
            size = item.stat().st_size / (1024*1024) if item.suffix == '.exe' else item.stat().st_size / 1024
            unit = 'MB' if item.suffix == '.exe' else 'KB'
            print(f"  📄 {item.name} ({size:.1f} {unit})")
