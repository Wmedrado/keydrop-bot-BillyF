#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilitários para desenvolvimento
👨‍💻 Desenvolvido por: Billy Franck (wmedrado)
📞 Discord: wmedrado
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime

class DevUtils:
    """Classe utilitária para desenvolvimento"""
    
    def __init__(self):
        self.dev_root = os.path.dirname(__file__)
        self.project_root = os.path.join(self.dev_root, '..')
        
    def criar_teste(self, nome_teste):
        """Cria um novo arquivo de teste"""
        template = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
{nome_teste}
👨‍💻 Desenvolvido por: Billy Franck (wmedrado)
📞 Discord: wmedrado
"""

import sys
import os

# Adicionar o diretório raiz do projeto ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def main():
    """Função principal do teste"""
    print("🧪 TESTE: {nome_teste}")
    print("=" * 50)
    
    # Seu código de teste aqui
    
    print("✅ Teste concluído!")
    print("=" * 50)
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
'''
        
        arquivo_teste = os.path.join(self.dev_root, 'tests', f'{nome_teste}.py')
        with open(arquivo_teste, 'w', encoding='utf-8') as f:
            f.write(template.format(nome_teste=nome_teste))
        
        print(f"✅ Teste criado: {arquivo_teste}")
        return arquivo_teste
    
    def criar_script(self, nome_script):
        """Cria um novo script de desenvolvimento"""
        template = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
{nome_script}
👨‍💻 Desenvolvido por: Billy Franck (wmedrado)
📞 Discord: wmedrado
"""

import os
import sys

def main():
    """Função principal do script"""
    print("🔧 SCRIPT: {nome_script}")
    print("=" * 50)
    
    # Seu código do script aqui
    
    print("✅ Script concluído!")
    print("=" * 50)
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
'''
        
        arquivo_script = os.path.join(self.dev_root, 'scripts', f'{nome_script}.py')
        with open(arquivo_script, 'w', encoding='utf-8') as f:
            f.write(template.format(nome_script=nome_script))
        
        print(f"✅ Script criado: {arquivo_script}")
        return arquivo_script
    
    def criar_exemplo(self, nome_exemplo):
        """Cria um novo exemplo"""
        template = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
{nome_exemplo}
👨‍💻 Desenvolvido por: Billy Franck (wmedrado)
📞 Discord: wmedrado
"""

import sys
import os

# Adicionar o diretório raiz do projeto ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def main():
    """Função principal do exemplo"""
    print("📚 EXEMPLO: {nome_exemplo}")
    print("=" * 50)
    
    # Seu código de exemplo aqui
    
    print("✅ Exemplo concluído!")
    print("=" * 50)
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
'''
        
        arquivo_exemplo = os.path.join(self.dev_root, 'examples', f'{nome_exemplo}.py')
        with open(arquivo_exemplo, 'w', encoding='utf-8') as f:
            f.write(template.format(nome_exemplo=nome_exemplo))
        
        print(f"✅ Exemplo criado: {arquivo_exemplo}")
        return arquivo_exemplo
    
    def limpar_temp(self):
        """Limpa arquivos temporários"""
        temp_dir = os.path.join(self.dev_root, 'temp')
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
        
        print("✅ Pasta temp limpa!")
    
    def limpar_logs(self):
        """Limpa logs de desenvolvimento"""
        logs_dir = os.path.join(self.dev_root, 'logs')
        if os.path.exists(logs_dir):
            for arquivo in os.listdir(logs_dir):
                if arquivo.endswith('.log'):
                    os.remove(os.path.join(logs_dir, arquivo))
        
        print("✅ Logs limpos!")
    
    def executar_teste(self, nome_teste):
        """Executa um teste específico"""
        arquivo_teste = os.path.join(self.dev_root, 'tests', f'{nome_teste}.py')
        if os.path.exists(arquivo_teste):
            subprocess.run([sys.executable, arquivo_teste])
        else:
            print(f"❌ Teste não encontrado: {nome_teste}")
    
    def listar_arquivos(self, pasta):
        """Lista arquivos em uma pasta específica"""
        pasta_path = os.path.join(self.dev_root, pasta)
        if os.path.exists(pasta_path):
            arquivos = [f for f in os.listdir(pasta_path) if f.endswith('.py')]
            if arquivos:
                print(f"📁 Arquivos em {pasta}:")
                for arquivo in sorted(arquivos):
                    print(f"   • {arquivo}")
            else:
                print(f"📁 Pasta {pasta} está vazia")
        else:
            print(f"❌ Pasta não encontrada: {pasta}")
    
    def criar_backup_dev(self):
        """Cria backup da pasta de desenvolvimento"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'backup_dev_{timestamp}.zip'
        backup_path = os.path.join(self.dev_root, 'backup', backup_name)
        
        shutil.make_archive(backup_path.replace('.zip', ''), 'zip', self.dev_root)
        print(f"✅ Backup criado: {backup_name}")
        return backup_path

def main():
    """Menu principal dos utilitários"""
    utils = DevUtils()
    
    print("🛠️ UTILITÁRIOS DE DESENVOLVIMENTO")
    print("=" * 50)
    
    opcoes = [
        ("1", "Criar novo teste", lambda: utils.criar_teste(input("Nome do teste: "))),
        ("2", "Criar novo script", lambda: utils.criar_script(input("Nome do script: "))),
        ("3", "Criar novo exemplo", lambda: utils.criar_exemplo(input("Nome do exemplo: "))),
        ("4", "Limpar temp", utils.limpar_temp),
        ("5", "Limpar logs", utils.limpar_logs),
        ("6", "Executar teste", lambda: utils.executar_teste(input("Nome do teste: "))),
        ("7", "Listar testes", lambda: utils.listar_arquivos('tests')),
        ("8", "Listar scripts", lambda: utils.listar_arquivos('scripts')),
        ("9", "Listar exemplos", lambda: utils.listar_arquivos('examples')),
        ("10", "Criar backup dev", utils.criar_backup_dev),
    ]
    
    print("📋 Opções disponíveis:")
    for codigo, nome, _ in opcoes:
        print(f"   {codigo}. {nome}")
    
    while True:
        try:
            escolha = input(f"\n🤔 Escolha uma opção (1-{len(opcoes)}) ou 'q' para sair: ").strip()
            
            if escolha.lower() == 'q':
                print("👋 Até logo!")
                break
            
            for codigo, nome, funcao in opcoes:
                if escolha == codigo:
                    print(f"\n🔄 Executando: {nome}")
                    print("-" * 30)
                    funcao()
                    print("-" * 30)
                    break
            else:
                print("❌ Opção inválida!")
                
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
