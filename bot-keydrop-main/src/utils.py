#!/usr/bin/env python3
"""
Módulo de utilitários para o KeyDrop Bot
"""
import os
import json
import shutil
import threading
import time
from datetime import datetime
from pathlib import Path

class ConfigManager:
    """Gerenciador de configurações"""
    
    def __init__(self, config_file='bot_config.json'):
        self.config_file = config_file
        self.default_config = {
            'num_bots': 5,
            'velocidade_navegacao': 5,
            'headless': False,
            'login_mode': False,
            'contender_mode': False,
            'discord_webhook': '',
            'relatorios_automaticos': False,
            'backup_automatico': True,
            'limpeza_automatica': True,
            'notificacoes_desktop': True,
            'tema': 'dark',
            'idioma': 'pt-BR'
        }
        
    def load_config(self):
        """Carrega configurações do arquivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Mescla com configurações padrão para garantir compatibilidade
                    merged_config = self.default_config.copy()
                    merged_config.update(config)
                    return merged_config
            else:
                return self.default_config.copy()
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            return self.default_config.copy()
    
    def save_config(self, config):
        """Salva configurações no arquivo"""
        try:
            # Fazer backup antes de salvar
            if os.path.exists(self.config_file):
                backup_file = f"{self.config_file}.backup"
                shutil.copy2(self.config_file, backup_file)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False
    
    def reset_config(self):
        """Reseta configurações para padrão"""
        return self.default_config.copy()

class FileManager:
    """Gerenciador de arquivos e pastas"""
    
    @staticmethod
    def ensure_directory(path):
        """Garante que o diretório existe"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Erro ao criar diretório {path}: {e}")
            return False
    
    @staticmethod
    def backup_file(source, backup_dir='backup'):
        """Cria backup de um arquivo"""
        try:
            FileManager.ensure_directory(backup_dir)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.basename(source)
            backup_path = os.path.join(backup_dir, f"{filename}.{timestamp}")
            shutil.copy2(source, backup_path)
            return backup_path
        except Exception as e:
            print(f"Erro ao fazer backup de {source}: {e}")
            return None
    
    @staticmethod
    def clean_old_backups(backup_dir='backup', days_to_keep=7):
        """Remove backups antigos"""
        try:
            if not os.path.exists(backup_dir):
                return
                
            cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)
            
            for filename in os.listdir(backup_dir):
                file_path = os.path.join(backup_dir, filename)
                if os.path.isfile(file_path):
                    if os.path.getmtime(file_path) < cutoff_time:
                        os.remove(file_path)
                        
        except Exception as e:
            print(f"Erro ao limpar backups: {e}")
    
    @staticmethod
    def get_file_size(path):
        """Retorna tamanho do arquivo em bytes"""
        try:
            return os.path.getsize(path)
        except:
            return 0
    
    @staticmethod
    def get_directory_size(path):
        """Retorna tamanho do diretório em bytes"""
        try:
            total = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total += FileManager.get_file_size(fp)
            return total
        except:
            return 0

class SystemMonitor:
    """Monitor de sistema"""
    
    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
        self.callbacks = []
        
    def add_callback(self, callback):
        """Adiciona callback para receber dados de monitoramento"""
        self.callbacks.append(callback)
    
    def start_monitoring(self, interval=3):
        """Inicia monitoramento"""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Para monitoramento"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def _monitor_loop(self, interval):
        """Loop de monitoramento"""
        try:
            import psutil
            
            while self.monitoring:
                try:
                    # Coleta dados do sistema
                    data = {
                        'cpu_percent': psutil.cpu_percent(interval=1),
                        'memory_percent': psutil.virtual_memory().percent,
                        'disk_percent': psutil.disk_usage('/').percent,
                        'network_io': psutil.net_io_counters(),
                        'timestamp': datetime.now()
                    }
                    
                    # Chama callbacks
                    for callback in self.callbacks:
                        try:
                            callback(data)
                        except Exception as e:
                            print(f"Erro em callback de monitoramento: {e}")
                    
                    time.sleep(interval)
                    
                except Exception as e:
                    print(f"Erro no monitoramento: {e}")
                    time.sleep(interval)
                    
        except ImportError:
            print("psutil não disponível para monitoramento")

class Logger:
    """Sistema de logs"""
    
    def __init__(self, log_file='bot.log', max_size=10*1024*1024):  # 10MB
        self.log_file = log_file
        self.max_size = max_size
        self.callbacks = []
        
    def add_callback(self, callback):
        """Adiciona callback para receber logs"""
        self.callbacks.append(callback)
    
    def log(self, level, message):
        """Registra log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # Escreve no arquivo
        try:
            self._write_to_file(log_entry)
        except Exception as e:
            print(f"Erro ao escrever log: {e}")
        
        # Chama callbacks
        for callback in self.callbacks:
            try:
                callback(level, message, timestamp)
            except Exception as e:
                print(f"Erro em callback de log: {e}")
    
    def _write_to_file(self, log_entry):
        """Escreve entrada no arquivo de log"""
        # Verifica tamanho do arquivo
        if os.path.exists(self.log_file):
            if os.path.getsize(self.log_file) > self.max_size:
                # Rotaciona o log
                backup_name = f"{self.log_file}.old"
                if os.path.exists(backup_name):
                    os.remove(backup_name)
                os.rename(self.log_file, backup_name)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def info(self, message):
        """Log de informação"""
        self.log('INFO', message)
    
    def warning(self, message):
        """Log de aviso"""
        self.log('WARNING', message)
    
    def error(self, message):
        """Log de erro"""
        self.log('ERROR', message)
    
    def debug(self, message):
        """Log de debug"""
        self.log('DEBUG', message)

class ValidationUtils:
    """Utilitários de validação"""
    
    @staticmethod
    def validate_webhook_url(url):
        """Valida URL do webhook do Discord"""
        if not url:
            return False
        return url.startswith('https://discord.com/api/webhooks/') or \
               url.startswith('https://discordapp.com/api/webhooks/')
    
    @staticmethod
    def validate_number_range(value, min_val, max_val):
        """Valida se número está no intervalo"""
        try:
            num = int(value)
            return min_val <= num <= max_val
        except ValueError:
            return False
    
    @staticmethod
    def validate_config(config):
        """Valida configuração completa"""
        errors = []
        
        # Validar número de bots
        if not ValidationUtils.validate_number_range(config.get('num_bots', 0), 1, 200):
            errors.append("Número de bots deve estar entre 1 e 200")
        
        # Validar velocidade de navegação
        if not ValidationUtils.validate_number_range(config.get('velocidade_navegacao', 0), 1, 10):
            errors.append("Velocidade de navegação deve estar entre 1 e 10")
        
        # Validar webhook do Discord
        webhook = config.get('discord_webhook', '')
        if webhook and not ValidationUtils.validate_webhook_url(webhook):
            errors.append("URL do webhook do Discord inválida")
        
        return errors

class FormatUtils:
    """Utilitários de formatação"""
    
    @staticmethod
    def format_bytes(bytes_value):
        """Formata bytes em unidades legíveis"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} TB"
    
    @staticmethod
    def format_duration(seconds):
        """Formata duração em formato legível"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    @staticmethod
    def format_currency(value):
        """Formata valor monetário"""
        try:
            return f"R$ {float(value):.2f}".replace('.', ',')
        except:
            return "R$ 0,00"
    
    @staticmethod
    def format_percentage(value):
        """Formata porcentagem"""
        try:
            return f"{float(value):.1f}%"
        except:
            return "0.0%"

# Singleton do logger global
_global_logger = None

def get_logger():
    """Retorna logger global"""
    global _global_logger
    if _global_logger is None:
        _global_logger = Logger()
    return _global_logger

def setup_project_structure():
    """Configura estrutura de pastas do projeto"""
    directories = [
        'src',
        'docs',
        'tests',
        'scripts',
        'backup',
        'logs',
        'profiles',
        'data'
    ]
    
    for directory in directories:
        FileManager.ensure_directory(directory)
    
    print("Estrutura de pastas configurada com sucesso!")

if __name__ == "__main__":
    # Teste básico dos utilitários
    setup_project_structure()
    
    # Teste do ConfigManager
    config_manager = ConfigManager()
    config = config_manager.load_config()
    print(f"Configuração carregada: {config}")
    
    # Teste do Logger
    logger = get_logger()
    logger.info("Sistema de utilitários iniciado")
    
    print("Utilitários testados com sucesso!")
