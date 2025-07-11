"""
KeyDrop Bot - Production Launcher
=================================

Script de produção para iniciar o KeyDrop Bot com todas as otimizações.
Garante que o ambiente esteja configurado corretamente antes de iniciar.
"""

import os
import sys
import time
import subprocess
import json
from datetime import datetime

def print_banner():
    """Exibe o banner do bot"""
    # Carregar versão do arquivo version.json
    try:
        with open("version.json", "r") as f:
            version_data = json.load(f)
            version = version_data["version"]
    except:
        version = "2.0.7"
    
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║               KeyDrop Bot - Professional Edition             ║
    ║                          v{version}                              ║
    ║                                                              ║
    ║                   Desenvolvido por William Medrado              ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def verificar_python():
    """Verifica se Python está disponível"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Versão muito antiga")
            print("   Necessário Python 3.8 ou superior")
            return False
    except:
        print("❌ Erro ao verificar versão do Python")
        return False

def verificar_arquivos_principais():
    """Verifica se os arquivos principais existem"""
    arquivos = ["modern_gui.py", "keydrop_bot.py", "requirements.txt", "version.json"]
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} - OK")
        else:
            print(f"❌ {arquivo} - FALTANDO")
            return False
    
    return True

def instalar_dependencias():
    """Instala dependências se necessário"""
    print("🔧 Verificando dependências...")
    
    try:
        # Tenta importar as principais dependências
        import selenium
        import requests
        import psutil
        print("✅ Dependências já instaladas")
        return True
    except ImportError:
        print("⚠️ Instalando dependências...")
        try:
            # Primeiro, atualiza pip
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            
            # Instala dependências com versões flexíveis
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"])
            print("✅ Dependências instaladas com sucesso")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            print("🔧 Tentando instalação individual...")
            
            # Lista de dependências essenciais
            deps_essenciais = [
                "selenium>=4.15.0",
                "webdriver-manager>=4.0.0",
                "requests>=2.31.0",
                "psutil>=5.9.0",
                "pillow>=10.0.0",
                "colorama>=0.4.0"
            ]
            
            # Tenta instalar uma por uma
            for dep in deps_essenciais:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                    print(f"✅ {dep} instalado")
                except subprocess.CalledProcessError:
                    print(f"⚠️ Falha ao instalar {dep} - continuando...")
            
            # Tenta instalar pywin32 específico para Windows
            if sys.platform == "win32":
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
                    print("✅ pywin32 instalado")
                except subprocess.CalledProcessError:
                    print("⚠️ pywin32 não instalado - algumas funcionalidades podem não funcionar")
            
            return True

def verificar_chrome():
    """Verifica se Chrome está instalado"""
    chrome_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
    ]
    
    for path in chrome_paths:
        expanded_path = os.path.expandvars(path)
        if os.path.exists(expanded_path):
            print("✅ Google Chrome encontrado")
            return True
    
    print("❌ Google Chrome não encontrado")
    print("   Instale o Google Chrome antes de continuar")
    return False

def criar_diretorios_necessarios():
    """Cria diretórios necessários"""
    diretorios = ["profiles", "data", "backup"]
    
    for diretorio in diretorios:
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
            print(f"✅ Diretório '{diretorio}' criado")
        else:
            print(f"✅ Diretório '{diretorio}' - OK")

def executar_otimizacao():
    """Executa otimização se disponível"""
    if os.path.exists("final_optimizer.py"):
        print("🚀 Executando otimizações...")
        try:
            subprocess.run([sys.executable, "final_optimizer.py"], check=True)
            return True
        except subprocess.CalledProcessError:
            print("⚠️ Erro na otimização - continuando mesmo assim")
            return False
    else:
        print("⚠️ Otimizador não encontrado - continuando mesmo assim")
        return False

def iniciar_bot():
    """Inicia o bot principal"""
    print("\n🚀 Iniciando KeyDrop Bot...")
    print("=" * 50)
    
    try:
        # Inicia o bot com interface moderna
        subprocess.run([sys.executable, "modern_gui.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Erro ao iniciar o bot")
        return False
    except KeyboardInterrupt:
        print("\n⏹️ Bot interrompido pelo usuário")
        return True
    
    return True

def main():
    """Função principal"""
    print_banner()
    
    print("🔍 Verificando ambiente...")
    print("=" * 50)
    
    # Verificações de pré-requisitos
    verificacoes = [
        ("Python", verificar_python),
        ("Arquivos principais", verificar_arquivos_principais),
        ("Google Chrome", verificar_chrome),
        ("Dependências", instalar_dependencias)
    ]
    
    for nome, funcao in verificacoes:
        print(f"\n{nome}:")
        if not funcao():
            print(f"\n❌ Falha na verificação: {nome}")
            print("🛠️ Corrija o problema e tente novamente")
            input("Pressione Enter para sair...")
            return False
    
    # Preparação do ambiente
    print("\n🛠️ Preparando ambiente...")
    print("=" * 50)
    
    criar_diretorios_necessarios()
    executar_otimizacao()
    
    # Iniciar bot
    print("\n✅ Ambiente preparado com sucesso!")
    print("🎯 Iniciando KeyDrop Bot...")
    
    # Aguarda 3 segundos para o usuário ler
    for i in range(3, 0, -1):
        print(f"Iniciando em {i}...")
        time.sleep(1)
    
    return iniciar_bot()

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Execução interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")
        sys.exit(1)
