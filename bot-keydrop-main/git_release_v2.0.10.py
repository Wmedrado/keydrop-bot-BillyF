#!/usr/bin/env python3
"""
Script para fazer commit e criar tag da versão v2.0.10
"""
import subprocess
import os
import sys

def run_git_command(command, description):
    """Executa comando git e retorna resultado"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            print(f"✅ {description} - SUCESSO")
            if result.stdout.strip():
                print(f"📝 Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - ERRO: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - EXCEÇÃO: {e}")
        return False

def create_release_commit():
    """Cria commit e tag para a release v2.0.10"""
    print("🚀 Criando commit e tag para KeyDrop Bot Professional Edition v2.0.10")
    print("=" * 70)
    
    # Verificar se estamos em um repositório git
    if not os.path.exists('.git'):
        print("❌ Não é um repositório git!")
        return False
    
    # Adicionar todos os arquivos
    print("\n📁 Adicionando arquivos ao staging area...")
    if not run_git_command('git add .', 'Adicionando arquivos'):
        return False
    
    # Criar commit
    commit_message = '''🚀 Release v2.0.10 - Sistema de Atualização Validado e Preparação para Produção

🔄 Sistema de Atualização Completamente Validado:
- Testes automatizados para verificação de GitHub API
- Download automático de atualizações funcionando perfeitamente
- Verificação de token GitHub aprimorada
- Tratamento robusto de erros durante atualização

🧹 Otimização e Limpeza:
- Remoção automática de arquivos antigos de release
- Estrutura limpa para distribuição em produção
- Empacotamento otimizado com arquivos essenciais
- Documentação atualizada e organizada

📦 Preparação Completa para Produção:
- Script automatizado para criação de releases
- Validação completa de todos os sistemas
- Arquivo ZIP otimizado pronto para distribuição
- Testes de integração validados

🔧 Funcionalidades Mantidas:
- Integração Telegram completa com controle remoto
- Sistema de relatórios avançado personalizável
- Banco de dados SQLite para estatísticas
- Interface moderna com monitoramento em tempo real
- Comandos Telegram: /iniciar, /parar, /status, /relatorio, etc.

✅ Validação Completa:
- Sistema de atualização testado e funcionando
- Integração Telegram validada
- Sistema de relatórios operacional
- Interface moderna responsiva
- Documentação atualizada
- Arquivo de distribuição otimizado

📊 Métricas nos Relatórios:
- Total de sorteios joinados (Amateur + Contender)
- Total de erros e taxa de sucesso
- Lucro total e saldo atual em skins
- Média de CPU e RAM durante período
- Número de bots executando simultaneamente
- Consumo total de internet (GB)
- Número de guias reiniciadas
- IP público incluído no relatório

🎯 Pronto para produção e distribuição!'''
    
    print("\n📝 Criando commit...")
    if not run_git_command(f'git commit -m "{commit_message}"', 'Criando commit'):
        return False
    
    # Criar tag
    tag_message = '''KeyDrop Bot Professional Edition v2.0.10

Sistema de Atualização Validado e Preparação para Produção

- Sistema de atualização automática completamente validado
- Integração Telegram completa com controle remoto
- Sistema de relatórios avançado personalizável
- Otimização e limpeza para produção
- Documentação atualizada e organizada
- Arquivo de distribuição otimizado

Pronto para distribuição em produção!'''
    
    print("\n🏷️ Criando tag v2.0.10...")
    if not run_git_command(f'git tag -a v2.0.10 -m "{tag_message}"', 'Criando tag'):
        return False
    
    # Mostrar status
    print("\n📊 Status do repositório:")
    run_git_command('git status', 'Verificando status')
    
    print("\n🏷️ Tags criadas:")
    run_git_command('git tag -l | tail -5', 'Listando tags recentes')
    
    print("\n" + "=" * 70)
    print("🎉 COMMIT E TAG CRIADOS COM SUCESSO!")
    print("🏷️ Tag: v2.0.10")
    print("📝 Commit: Release v2.0.10 - Sistema de Atualização Validado")
    print("🚀 Pronto para push e criação da release no GitHub!")
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. git push origin main")
    print("2. git push origin v2.0.10")
    print("3. Criar release no GitHub com o arquivo ZIP")
    print("4. Anunciar para usuários")
    
    return True

def push_to_github():
    """Faz push para o GitHub"""
    print("\n🌐 Fazendo push para o GitHub...")
    
    # Push do branch principal
    if not run_git_command('git push origin main', 'Push do branch principal'):
        return False
    
    # Push da tag
    if not run_git_command('git push origin v2.0.10', 'Push da tag v2.0.10'):
        return False
    
    print("✅ Push realizado com sucesso!")
    return True

if __name__ == "__main__":
    print("🤖 KeyDrop Bot Professional Edition v2.0.10 - Git Release")
    print("=" * 70)
    
    # Criar commit e tag
    if create_release_commit():
        print("\n🎯 Deseja fazer push para o GitHub? (s/n): ", end="")
        try:
            choice = input().lower().strip()
            if choice in ['s', 'sim', 'y', 'yes']:
                push_to_github()
            else:
                print("⚠️ Push cancelado. Execute manualmente:")
                print("   git push origin main")
                print("   git push origin v2.0.10")
        except KeyboardInterrupt:
            print("\n⚠️ Operação cancelada pelo usuário")
        
        print("\n🎉 Release v2.0.10 preparada com sucesso!")
    else:
        print("\n❌ Falha na criação do commit/tag")
        sys.exit(1)
