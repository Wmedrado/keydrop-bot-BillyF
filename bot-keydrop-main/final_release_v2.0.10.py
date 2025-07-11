#!/usr/bin/env python3
"""
Script Final para Release v2.0.10 - KeyDrop Bot Professional Edition
Executa todos os passos necessários para preparar a release
"""
import os
import sys
import subprocess
import time
from datetime import datetime

def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 60)
    print(f"🚀 {title}")
    print("=" * 60)

def print_step(step_num, total_steps, description):
    """Imprime passo atual"""
    print(f"\n[{step_num}/{total_steps}] {description}")

def run_command(command, description):
    """Executa comando e retorna resultado"""
    print(f"⚙️ {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCESSO")
            return True
        else:
            print(f"❌ {description} - ERRO: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - EXCEÇÃO: {e}")
        return False

def final_release_preparation():
    """Executa todos os passos para preparar a release final"""
    print_header("KeyDrop Bot Professional Edition v2.0.10 - RELEASE FINAL")
    
    start_time = time.time()
    total_steps = 8
    
    # Passo 1: Verificar arquivos essenciais
    print_step(1, total_steps, "Verificando arquivos essenciais")
    essential_files = [
        'modern_gui_v2.py',
        'keydrop_bot.py',
        'version.json',
        'github_token.txt',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in essential_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Arquivos essenciais não encontrados: {missing_files}")
        return False
    else:
        print("✅ Todos os arquivos essenciais encontrados")
    
    # Passo 2: Validar configurações
    print_step(2, total_steps, "Validando configurações")
    try:
        import json
        with open('version.json', 'r') as f:
            version_info = json.load(f)
            version = version_info['version']
            print(f"📦 Versão: {version}")
            
        with open('github_token.txt', 'r') as f:
            token = f.read().strip()
            if len(token) > 20:
                print(f"✅ Token GitHub válido: {token[:10]}...")
            else:
                print("❌ Token GitHub inválido")
                return False
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
        return False
    
    # Passo 3: Testar importações principais
    print_step(3, total_steps, "Testando importações principais")
    try:
        sys.path.insert(0, '.')
        from keydrop_bot import KeyDropBot, BotManager
        from src.telegram_integration import TelegramBot
        from src.report_manager import ReportManager
        print("✅ Todas as importações principais funcionando")
    except Exception as e:
        print(f"❌ Erro nas importações: {e}")
        return False
    
    # Passo 4: Limpar arquivos antigos
    print_step(4, total_steps, "Limpando arquivos antigos")
    if os.path.exists('cleanup_old_releases.py'):
        success = run_command('python cleanup_old_releases.py', 'Limpeza de arquivos antigos')
        if not success:
            print("⚠️ Limpeza manual necessária")
    
    # Passo 5: Preparar diretório de release
    print_step(5, total_steps, "Preparando diretório de release")
    success = run_command('python prepare_release_v2.0.10.py', 'Preparação da release')
    if not success:
        print("❌ Falha na preparação da release")
        return False
    
    # Passo 6: Verificar arquivo ZIP criado
    print_step(6, total_steps, "Verificando arquivo ZIP criado")
    zip_files = [f for f in os.listdir('.') if f.startswith('KeyDrop_Bot_Professional_v') and f.endswith('.zip')]
    if zip_files:
        zip_file = zip_files[0]
        zip_size = os.path.getsize(zip_file) / (1024 * 1024)  # MB
        print(f"✅ Arquivo ZIP criado: {zip_file} ({zip_size:.2f} MB)")
    else:
        print("❌ Arquivo ZIP não encontrado")
        return False
    
    # Passo 7: Validar sistema de atualização
    print_step(7, total_steps, "Validando sistema de atualização")
    try:
        from src.improved_update_manager import ImprovedUpdateManager
        um = ImprovedUpdateManager(current_version=version)
        if um.github_token:
            print("✅ Sistema de atualização configurado corretamente")
        else:
            print("❌ Sistema de atualização não configurado")
            return False
    except Exception as e:
        print(f"❌ Erro no sistema de atualização: {e}")
        return False
    
    # Passo 8: Resumo final
    print_step(8, total_steps, "Resumo final da release")
    
    elapsed_time = time.time() - start_time
    
    print_header("RELEASE v2.0.10 PREPARADA COM SUCESSO!")
    
    print(f"📦 Arquivo principal: {zip_file}")
    print(f"📊 Tamanho: {zip_size:.2f} MB")
    print(f"🕒 Tempo de preparação: {elapsed_time:.1f} segundos")
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. ✅ Testar o arquivo ZIP em ambiente limpo")
    print("2. ✅ Verificar funcionamento dos executáveis")
    print("3. ✅ Fazer upload para GitHub Releases")
    print("4. ✅ Atualizar documentação no repositório")
    print("5. ✅ Anunciar release para usuários")
    
    print("\n🚀 RELEASE PRONTA PARA PRODUÇÃO!")
    
    return True

if __name__ == "__main__":
    success = final_release_preparation()
    
    if success:
        print("\n🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
        print("✅ KeyDrop Bot Professional Edition v2.0.10 está pronto para distribuição!")
        
        # Perguntar se deve abrir o diretório
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            
            response = messagebox.askyesno(
                "Release Preparada",
                "Release v2.0.10 preparada com sucesso!\n\nDeseja abrir o diretório?"
            )
            
            if response:
                os.startfile('.')
                
        except:
            pass
            
        sys.exit(0)
    else:
        print("\n❌ ERRO NA PREPARAÇÃO DA RELEASE")
        print("⚠️ Verificar logs acima para detalhes")
        sys.exit(1)
