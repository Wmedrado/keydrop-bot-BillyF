#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Executor do modo CONTENDER com interface amigável
👨‍💻 Desenvolvido por: Billy Franck (wmedrado)
📞 Discord: wmedrado
"""

import sys
import os
import time
import json
from datetime import datetime, timedelta
from pathlib import Path

# Adicionar o diretório raiz do projeto ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class ContenderExecutor:
    """Executor do modo CONTENDER"""
    
    def __init__(self):
        self.log_dir = Path(__file__).parent.parent / "logs"
        self.log_dir.mkdir(exist_ok=True)
        
        self.stats = {
            'execucoes': 0,
            'sucessos': 0,
            'falhas': 0,
            'giveaways_participados': 0,
            'ultima_execucao': None,
            'proxima_execucao': None
        }
        
        self.stats_file = self.log_dir / "contender_stats.json"
        self.carregar_stats()
    
    def carregar_stats(self):
        """Carrega estatísticas salvas"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    self.stats.update(json.load(f))
            except:
                pass
    
    def salvar_stats(self):
        """Salva estatísticas"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def mostrar_banner(self):
        """Mostra banner do modo CONTENDER"""
        print("🎯" + "=" * 58 + "🎯")
        print("🎯" + " " * 20 + "MODO CONTENDER" + " " * 25 + "🎯")
        print("🎯" + " " * 15 + "KeyDrop Bot by Billy Franck" + " " * 15 + "🎯")
        print("🎯" + " " * 18 + "Discord: wmedrado" + " " * 22 + "🎯")
        print("🎯" + "=" * 58 + "🎯")
        print()
    
    def mostrar_stats(self):
        """Mostra estatísticas"""
        print("📊 ESTATÍSTICAS DO MODO CONTENDER")
        print("-" * 40)
        print(f"🔄 Execuções totais: {self.stats['execucoes']}")
        print(f"✅ Sucessos: {self.stats['sucessos']}")
        print(f"❌ Falhas: {self.stats['falhas']}")
        print(f"🎁 Giveaways participados: {self.stats['giveaways_participados']}")
        
        if self.stats['ultima_execucao']:
            print(f"⏰ Última execução: {self.stats['ultima_execucao']}")
        
        if self.stats['proxima_execucao']:
            print(f"⏰ Próxima execução: {self.stats['proxima_execucao']}")
        
        print("-" * 40)
        print()
    
    def escolher_profile(self):
        """Permite ao usuário escolher um profile"""
        profiles_dir = Path(__file__).parent.parent.parent / "profiles"
        
        if not profiles_dir.exists():
            print("❌ Diretório de profiles não encontrado!")
            return None
        
        profiles = []
        for profile in profiles_dir.glob("Profile-*"):
            if (profile / "Preferences").exists():
                profiles.append(profile)
        
        if not profiles:
            print("❌ Nenhum profile válido encontrado!")
            return None
        
        print("📁 PROFILES DISPONÍVEIS:")
        print("-" * 30)
        
        for i, profile in enumerate(profiles, 1):
            print(f"{i}. {profile.name}")
        
        print("-" * 30)
        
        while True:
            try:
                escolha = input("Escolha um profile (número): ").strip()
                
                if not escolha:
                    print("⚠️ Digite um número válido!")
                    continue
                
                num = int(escolha)
                
                if 1 <= num <= len(profiles):
                    profile_escolhido = profiles[num - 1]
                    print(f"✅ Profile selecionado: {profile_escolhido.name}")
                    return str(profile_escolhido)
                else:
                    print("⚠️ Número inválido!")
                    
            except ValueError:
                print("⚠️ Digite um número válido!")
            except KeyboardInterrupt:
                print("\n❌ Operação cancelada pelo usuário")
                return None
    
    def confirmar_execucao(self):
        """Confirma se o usuário quer executar"""
        print("⚠️ IMPORTANTE:")
        print("• Certifique-se de que está logado no KeyDrop")
        print("• O bot irá procurar por giveaways disponíveis")
        print("• Participação automática será realizada")
        print("• O processo pode demorar alguns minutos")
        print()
        
        while True:
            resposta = input("Deseja continuar? (s/n): ").strip().lower()
            
            if resposta in ['s', 'sim', 'y', 'yes']:
                return True
            elif resposta in ['n', 'nao', 'não', 'no']:
                return False
            else:
                print("⚠️ Digite 's' para sim ou 'n' para não")
    
    def executar_contender(self, profile_path):
        """Executa o modo CONTENDER"""
        print("🚀 EXECUTANDO MODO CONTENDER")
        print("=" * 40)
        
        try:
            from contender_corrigido import ContenderBot
            
            # Atualizar stats
            self.stats['execucoes'] += 1
            self.stats['ultima_execucao'] = datetime.now().isoformat()
            
            # Executar bot
            bot = ContenderBot()
            resultado = bot.executar_modo_contender(profile_path)
            
            if resultado:
                self.stats['sucessos'] += 1
                print("✅ Modo CONTENDER executado com sucesso!")
            else:
                self.stats['falhas'] += 1
                print("❌ Falha na execução do modo CONTENDER")
            
            # Calcular próxima execução (1 hora depois)
            proxima = datetime.now() + timedelta(hours=1)
            self.stats['proxima_execucao'] = proxima.isoformat()
            
            # Salvar stats
            self.salvar_stats()
            
            return resultado
            
        except Exception as e:
            print(f"❌ Erro crítico: {e}")
            self.stats['falhas'] += 1
            self.salvar_stats()
            return False
    
    def modo_automatico(self, profile_path):
        """Executa o modo automático (a cada 1 hora)"""
        print("🤖 MODO AUTOMÁTICO ATIVADO")
        print("▶️ Executando a cada 1 hora...")
        print("▶️ Pressione Ctrl+C para parar")
        print("=" * 40)
        
        try:
            while True:
                print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Executando...")
                
                resultado = self.executar_contender(profile_path)
                
                if resultado:
                    print("✅ Execução completa!")
                else:
                    print("❌ Execução falhou!")
                
                print("😴 Aguardando 1 hora para próxima execução...")
                print("   (Pressione Ctrl+C para parar)")
                
                # Aguardar 1 hora (3600 segundos)
                for i in range(3600, 0, -60):
                    minutos = i // 60
                    print(f"   ⏳ {minutos} minutos restantes...", end='\r')
                    time.sleep(60)
                
                print("\n" + "=" * 40)
                
        except KeyboardInterrupt:
            print("\n🛑 Modo automático interrompido pelo usuário")
            print("✅ Estatísticas salvas!")
    
    def menu_principal(self):
        """Menu principal"""
        while True:
            self.mostrar_banner()
            self.mostrar_stats()
            
            print("📋 OPÇÕES:")
            print("1. Executar uma vez")
            print("2. Modo automático (a cada 1 hora)")
            print("3. Visualizar logs")
            print("4. Limpar estatísticas")
            print("5. Sair")
            print()
            
            try:
                opcao = input("Escolha uma opção: ").strip()
                
                if opcao == '1':
                    profile_path = self.escolher_profile()
                    if profile_path and self.confirmar_execucao():
                        self.executar_contender(profile_path)
                    input("\nPressione Enter para continuar...")
                
                elif opcao == '2':
                    profile_path = self.escolher_profile()
                    if profile_path and self.confirmar_execucao():
                        self.modo_automatico(profile_path)
                    input("\nPressione Enter para continuar...")
                
                elif opcao == '3':
                    self.visualizar_logs()
                    input("\nPressione Enter para continuar...")
                
                elif opcao == '4':
                    self.limpar_stats()
                    input("\nPressione Enter para continuar...")
                
                elif opcao == '5':
                    print("👋 Saindo do modo CONTENDER...")
                    break
                
                else:
                    print("⚠️ Opção inválida!")
                    input("Pressione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n👋 Saindo do modo CONTENDER...")
                break
    
    def visualizar_logs(self):
        """Visualiza logs disponíveis"""
        print("📄 LOGS DISPONÍVEIS:")
        print("-" * 30)
        
        logs = list(self.log_dir.glob("*.log"))
        
        if not logs:
            print("❌ Nenhum log encontrado")
            return
        
        # Mostrar apenas os 10 logs mais recentes
        logs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        for i, log in enumerate(logs[:10], 1):
            tamanho = log.stat().st_size / 1024  # KB
            data = datetime.fromtimestamp(log.stat().st_mtime)
            print(f"{i}. {log.name} ({tamanho:.1f} KB) - {data.strftime('%d/%m/%Y %H:%M')}")
        
        print("-" * 30)
    
    def limpar_stats(self):
        """Limpa estatísticas"""
        resposta = input("Tem certeza que deseja limpar as estatísticas? (s/n): ").strip().lower()
        
        if resposta in ['s', 'sim', 'y', 'yes']:
            self.stats = {
                'execucoes': 0,
                'sucessos': 0,
                'falhas': 0,
                'giveaways_participados': 0,
                'ultima_execucao': None,
                'proxima_execucao': None
            }
            self.salvar_stats()
            print("✅ Estatísticas limpas!")
        else:
            print("❌ Operação cancelada")

def main():
    """Função principal"""
    executor = ContenderExecutor()
    
    try:
        executor.menu_principal()
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
