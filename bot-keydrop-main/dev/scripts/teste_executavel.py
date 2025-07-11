#!/usr/bin/env python3
"""
Script para testar o executável gerado
"""

import os
import sys
import subprocess
import time

def testar_executavel():
    """Testa o executável gerado"""
    print("=" * 60)
    print("TESTE DO EXECUTÁVEL GERADO")
    print("=" * 60)
    
    # Caminho para o executável
    executavel_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "startup", "executavel", "KeyDrop_Bot_Moderno.exe"
    )
    
    print(f"Caminho do executável: {executavel_path}")
    
    # Verifica se o executável existe
    if not os.path.exists(executavel_path):
        print("❌ Executável não encontrado!")
        return False
    
    # Verifica o tamanho do arquivo
    size = os.path.getsize(executavel_path)
    print(f"✅ Executável encontrado - Tamanho: {size / 1024 / 1024:.2f} MB")
    
    # Tenta executar o executável (apenas para ver se inicia)
    try:
        print("🔄 Testando execução do executável...")
        # Executa em background por 5 segundos
        process = subprocess.Popen([executavel_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Aguarda 5 segundos
        time.sleep(5)
        
        # Termina o processo
        process.terminate()
        
        # Verifica se houve erro
        if process.returncode is None:
            print("✅ Executável iniciou com sucesso!")
            return True
        else:
            print(f"❌ Erro na execução: {process.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")
        return False

if __name__ == "__main__":
    sucesso = testar_executavel()
    sys.exit(0 if sucesso else 1)
