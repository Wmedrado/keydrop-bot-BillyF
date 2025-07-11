#!/usr/bin/env python3
"""
Sistema de Gerenciamento de Relatórios - KeyDrop Bot Professional Edition
Gerencia relatórios automáticos para Discord e Telegram
"""

import threading
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional
import psutil

class ReportManager:
    """Gerenciador de relatórios automáticos"""
    
    def __init__(self, bot_manager=None):
        self.bot_manager = bot_manager
        self.running = False
        self.report_thread = None
        self.config = self.load_config()
        
        # Configurações padrão
        self.discord_webhook = self.config.get('discord_webhook', '')
        self.discord_report_hours = self.config.get('discord_report_hours', 12)
        self.telegram_token = self.config.get('telegram_token', '')
        
        # Estatísticas acumuladas
        self.stats = {
            'amateur_total': 0,
            'contender_total': 0,
            'erros_total': 0,
            'ganho_total': 0.0,
            'saldo_total_atual': 0.0,
            'bots_ativos': 0,
            'bots_total': 0,
            'total_skins': 0,
            'guias_reiniciadas': 0,
            'inicio_periodo': datetime.now(),
            'ultima_coleta': datetime.now()
        }
        
        # Métricas do sistema
        self.system_metrics = {
            'cpu_history': [],
            'ram_history': [],
            'network_start': None,
            'chrome_processes': 0
        }
        
        self.telegram_bot = None
        
    def load_config(self):
        """Carrega configurações do arquivo"""
        try:
            if os.path.exists('bot_config.json'):
                with open('bot_config.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
        return {}
    
    def start(self):
        """Inicia o sistema de relatórios"""
        if self.running:
            return
        
        self.running = True
        self.stats['inicio_periodo'] = datetime.now()
        
        # Inicializar métricas do sistema
        if self.system_metrics['network_start'] is None:
            try:
                net_io = psutil.net_io_counters()
                self.system_metrics['network_start'] = net_io.bytes_sent + net_io.bytes_recv
            except:
                self.system_metrics['network_start'] = 0
        
        # Iniciar thread de relatórios
        self.report_thread = threading.Thread(target=self._report_loop, daemon=True)
        self.report_thread.start()
        
        # Iniciar bot do Telegram se configurado
        if self.telegram_token:
            self.start_telegram_bot()
        
        print("📊 Sistema de relatórios iniciado")
    
    def stop(self):
        """Para o sistema de relatórios"""
        self.running = False
        if self.telegram_bot:
            self.telegram_bot.stop()
        print("📊 Sistema de relatórios parado")
    
    def start_telegram_bot(self):
        """Inicia o bot do Telegram"""
        try:
            from src.telegram_integration import TelegramBot
            
            self.telegram_bot = TelegramBot(self.telegram_token, self.bot_manager)
            self.telegram_bot.start()
            print("🤖 Bot do Telegram iniciado")
            
        except Exception as e:
            print(f"❌ Erro ao iniciar bot do Telegram: {e}")
    
    def _report_loop(self):
        """Loop principal de relatórios"""
        last_discord_report = datetime.now()
        
        while self.running:
            try:
                # Coletar estatísticas atuais
                self.collect_current_stats()
                
                # Verificar se é hora de enviar relatório Discord
                now = datetime.now()
                hours_since_last = (now - last_discord_report).total_seconds() / 3600
                
                if hours_since_last >= self.discord_report_hours and self.discord_webhook:
                    self.send_discord_report()
                    last_discord_report = now
                
                # Atualizar métricas do sistema
                self.update_system_metrics()
                
                # Aguardar próxima coleta (a cada 5 minutos)
                time.sleep(300)
                
            except Exception as e:
                print(f"❌ Erro no loop de relatórios: {e}")
                time.sleep(60)  # Aguardar 1 minuto em caso de erro
    
    def collect_current_stats(self):
        """Coleta estatísticas atuais dos bots"""
        if not self.bot_manager:
            return
        
        try:
            # Reset para nova coleta
            self.stats['amateur_total'] = 0
            self.stats['contender_total'] = 0
            self.stats['erros_total'] = 0
            self.stats['ganho_total'] = 0.0
            self.stats['saldo_total_atual'] = 0.0
            self.stats['bots_ativos'] = 0
            self.stats['bots_total'] = len(self.bot_manager.bots)
            self.stats['total_skins'] = 0
            self.stats['guias_reiniciadas'] = 0
            
            # Coletar dados de todos os bots
            for bot in self.bot_manager.bots:
                if bot.running:
                    self.stats['bots_ativos'] += 1
                
                # Somar estatísticas do bot
                bot_stats = bot.stats
                self.stats['amateur_total'] += bot_stats.get('amateur_total', 0)
                self.stats['contender_total'] += bot_stats.get('contender_total', 0)
                self.stats['erros_total'] += bot_stats.get('erros_total', 0)
                self.stats['ganho_total'] += bot_stats.get('ganho_total', 0.0)
                self.stats['saldo_total_atual'] += bot_stats.get('saldo_atual', 0.0)
                self.stats['total_skins'] += bot_stats.get('total_skins', 0)
                self.stats['guias_reiniciadas'] += bot_stats.get('guias_reiniciadas', 0)
            
            self.stats['ultima_coleta'] = datetime.now()
            
        except Exception as e:
            print(f"❌ Erro ao coletar estatísticas: {e}")
    
    def update_system_metrics(self):
        """Atualiza métricas do sistema"""
        try:
            # CPU e RAM
            cpu_percent = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            
            # Manter histórico das últimas 12 medições (1 hora)
            self.system_metrics['cpu_history'].append(cpu_percent)
            self.system_metrics['ram_history'].append(ram.percent)
            
            if len(self.system_metrics['cpu_history']) > 12:
                self.system_metrics['cpu_history'].pop(0)
            if len(self.system_metrics['ram_history']) > 12:
                self.system_metrics['ram_history'].pop(0)
            
            # Contar processos Chrome
            chrome_count = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                        chrome_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            self.system_metrics['chrome_processes'] = chrome_count
            
        except Exception as e:
            print(f"❌ Erro ao atualizar métricas: {e}")
    
    def get_system_info(self):
        """Obtém informações do sistema"""
        try:
            # Médias de CPU e RAM
            cpu_avg = sum(self.system_metrics['cpu_history']) / len(self.system_metrics['cpu_history']) if self.system_metrics['cpu_history'] else 0
            ram_avg = sum(self.system_metrics['ram_history']) / len(self.system_metrics['ram_history']) if self.system_metrics['ram_history'] else 0
            
            # Uso de rede desde o início
            network_usage = 0
            if self.system_metrics['network_start']:
                try:
                    net_io = psutil.net_io_counters()
                    current_bytes = net_io.bytes_sent + net_io.bytes_recv
                    network_usage = (current_bytes - self.system_metrics['network_start']) / (1024 * 1024)  # MB
                except:
                    pass
            
            # Uso de disco
            disk_usage = psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
            
            return {
                'cpu_usage': cpu_avg,
                'ram_usage': ram_avg,
                'chrome_processes': self.system_metrics['chrome_processes'],
                'network_usage': network_usage,
                'disk_usage': disk_usage,
                'guias_reiniciadas': self.stats['guias_reiniciadas']
            }
        except Exception as e:
            print(f"❌ Erro ao obter info do sistema: {e}")
            return {
                'cpu_usage': 0,
                'ram_usage': 0,
                'chrome_processes': 0,
                'network_usage': 0,
                'disk_usage': 0,
                'guias_reiniciadas': 0
            }
    
    def send_discord_report(self):
        """Envia relatório para o Discord"""
        if not self.discord_webhook:
            return
        
        try:
            from discord_notify import send_enhanced_report
            
            # Calcular horas desde o início do período
            period_hours = (datetime.now() - self.stats['inicio_periodo']).total_seconds() / 3600
            
            # Obter informações do sistema
            system_info = self.get_system_info()
            
            # Enviar relatório
            success = send_enhanced_report(
                self.discord_webhook,
                self.stats,
                period_hours,
                system_info
            )
            
            if success:
                print(f"📊 Relatório Discord enviado ({period_hours:.1f}h)")
                
                # Notificar Telegram se disponível
                if self.telegram_bot:
                    try:
                        self.telegram_bot.notify_discord_report_sent(period_hours)
                    except:
                        pass
            else:
                print("❌ Falha ao enviar relatório Discord")
                
        except Exception as e:
            print(f"❌ Erro ao enviar relatório Discord: {e}")
    
    def update_config(self, new_config):
        """Atualiza configurações"""
        self.config.update(new_config)
        self.discord_webhook = self.config.get('discord_webhook', '')
        self.discord_report_hours = self.config.get('discord_report_hours', 12)
        self.telegram_token = self.config.get('telegram_token', '')
        
        # Reiniciar bot do Telegram se token mudou
        if self.telegram_token and not self.telegram_bot:
            self.start_telegram_bot()
    
    def get_current_stats(self):
        """Retorna estatísticas atuais"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reseta estatísticas para novo período"""
        self.stats['inicio_periodo'] = datetime.now()
        print("📊 Estatísticas resetadas para novo período")

# Instância global do gerenciador
report_manager = None

def get_report_manager():
    """Obtém instância do gerenciador de relatórios"""
    global report_manager
    return report_manager

def init_report_manager(bot_manager=None):
    """Inicializa o gerenciador de relatórios"""
    global report_manager
    if report_manager is None:
        report_manager = ReportManager(bot_manager)
    return report_manager
