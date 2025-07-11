#!/usr/bin/env python3
"""
Sistema de gerenciamento de memória otimizado para KeyDrop Bot
Inclui limpeza automática, monitoramento e prevenção de travamentos
"""

import gc
import psutil
import threading
import time
import os
from datetime import datetime, timedelta

class MemoryManager:
    def __init__(self):
        self.running = False
        self.thread = None
        self.memory_threshold = 80  # % de RAM para trigger de limpeza
        self.cleanup_interval = 300  # 5 minutos
        self.update_interval = 10  # Atualizar informações a cada 10 segundos
        self.last_cleanup = time.time()
        self.last_update = time.time()
        self.process = psutil.Process()
        self.start_time = time.time()
        self.stats = {
            'total_cleanups': 0,
            'memory_saved': 0,
            'peak_memory': 0,
            'current_memory': 0,
            'cpu_percent': 0,
            'memory_percent': 0,
            'chrome_processes': 0,
            'total_handles': 0,
            'uptime': 0,
            'memory_mb': 0,
            'virtual_memory_mb': 0,
            'system_memory_used': 0,
            'system_memory_available': 0,
            'disk_usage': 0,
            'network_io': {'bytes_sent': 0, 'bytes_recv': 0}
        }
    
    def start(self):
        """Inicia o gerenciador de memória"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()
            print("🧠 Sistema de gerenciamento de memória iniciado")
    
    def stop(self):
        """Para o gerenciador de memória"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("🧠 Sistema de gerenciamento de memória parado")
    
    def _monitor_loop(self):
        """Loop principal de monitoramento"""
        while self.running:
            try:
                # Atualizar estatísticas a cada 10 segundos
                current_time = time.time()
                if current_time - self.last_update >= self.update_interval:
                    self._update_stats()
                    self.last_update = current_time
                
                # Verificar se precisa de limpeza
                if current_time - self.last_cleanup >= self.cleanup_interval:
                    self._perform_cleanup()
                    self.last_cleanup = current_time
                
                # Verificar threshold de memória
                if self.stats['memory_percent'] > self.memory_threshold:
                    self._emergency_cleanup()
                
                time.sleep(1)  # Sleep mais curto para monitoramento mais responsivo
                
            except Exception as e:
                print(f"❌ Erro no monitoramento de memória: {e}")
                time.sleep(5)  # Aguardar menos tempo em caso de erro
    
    def _update_stats(self):
        """Atualiza estatísticas de memória com informações mais precisas"""
        try:
            # Informações do processo atual
            memory_info = self.process.memory_info()
            current_mb = memory_info.rss / 1024 / 1024  # MB
            virtual_mb = memory_info.vms / 1024 / 1024  # MB
            
            # Informações do sistema
            system_memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Informações de disco
            disk_usage = psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
            
            # Informações de rede
            net_io = psutil.net_io_counters()
            
            # Contagem de processos Chrome
            chrome_count = 0
            total_handles = 0
            
            for proc in psutil.process_iter(['pid', 'name', 'num_handles']):
                try:
                    if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                        chrome_count += 1
                    if proc.info['num_handles']:
                        total_handles += proc.info['num_handles']
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Calcular uptime
            uptime_seconds = time.time() - self.start_time
            
            # Atualizar estatísticas com informações mais precisas
            self.stats.update({
                'current_memory': current_mb,
                'memory_mb': current_mb,
                'virtual_memory_mb': virtual_mb,
                'memory_percent': system_memory.percent,
                'system_memory_used': system_memory.used / 1024 / 1024 / 1024,  # GB
                'system_memory_available': system_memory.available / 1024 / 1024 / 1024,  # GB
                'cpu_percent': cpu_percent,
                'chrome_processes': chrome_count,
                'total_handles': total_handles,
                'uptime': uptime_seconds,
                'disk_usage': disk_usage,
                'network_io': {
                    'bytes_sent': net_io.bytes_sent / 1024 / 1024,  # MB
                    'bytes_recv': net_io.bytes_recv / 1024 / 1024   # MB
                }
            })
            
            # Atualizar pico de memória
            if current_mb > self.stats['peak_memory']:
                self.stats['peak_memory'] = current_mb
                
        except Exception as e:
            print(f"❌ Erro ao atualizar estatísticas de memória: {e}")
    
    def _should_cleanup(self):
        """Verifica se deve fazer limpeza"""
        try:
            # Verificar uso geral de RAM do sistema
            system_memory = psutil.virtual_memory()
            if system_memory.percent > self.memory_threshold:
                return True
            
            # Verificar uso de memória do processo
            current_mb = self.stats['current_memory']
            if current_mb > 500:  # Mais de 500MB
                return True
            
            # Verificar intervalo desde última limpeza
            if time.time() - self.last_cleanup > self.cleanup_interval:
                return True
            
            return False
            
        except Exception:
            return False
    
    def _perform_cleanup(self):
        """Executa limpeza de memória"""
        try:
            memory_before = self.stats['current_memory']
            
            # Forçar coleta de lixo
            gc.collect()
            
            # Limpeza específica do Python
            gc.set_threshold(0)  # Desabilitar temporariamente
            collected = gc.collect()
            gc.set_threshold(700, 10, 10)  # Restaurar padrão
            
            # Atualizar estatísticas
            self._update_stats()
            memory_after = self.stats['current_memory']
            memory_saved = memory_before - memory_after
            
            if memory_saved > 0:
                self.stats['memory_saved'] += memory_saved
                self.stats['total_cleanups'] += 1
                print(f"🧹 Limpeza de memória: {memory_saved:.1f}MB liberados ({collected} objetos)")
            
            self.last_cleanup = time.time()
            
        except Exception as e:
            print(f"❌ Erro na limpeza de memória: {e}")
    
    def force_cleanup(self):
        """Força limpeza imediata"""
        print("🧹 Forçando limpeza de memória...")
        self._perform_cleanup()
    
    def get_stats(self):
        """Retorna estatísticas de memória"""
        return {
            'current_memory_mb': round(self.stats['current_memory'], 1),
            'peak_memory_mb': round(self.stats['peak_memory'], 1),
            'total_cleanups': self.stats['total_cleanups'],
            'memory_saved_mb': round(self.stats['memory_saved'], 1),
            'system_memory_percent': psutil.virtual_memory().percent,
            'available_memory_mb': round(psutil.virtual_memory().available / 1024 / 1024, 1)
        }

    def _emergency_cleanup(self):
        """Limpeza de emergência quando memória atinge threshold crítico"""
        try:
            print("🚨 Limpeza de emergência iniciada - Memória crítica!")
            
            memory_before = self.stats['current_memory']
            
            # Limpeza intensiva
            gc.collect()
            gc.collect()  # Executar duas vezes para garantir
            
            # Limpar caches do sistema
            if hasattr(gc, 'set_threshold'):
                gc.set_threshold(100, 5, 5)  # Mais agressivo
            
            # Fechar processos Chrome órfãos
            self._cleanup_chrome_orphans()
            
            # Atualizar estatísticas
            self._update_stats()
            memory_after = self.stats['current_memory']
            saved = memory_before - memory_after
            
            self.stats['total_cleanups'] += 1
            self.stats['memory_saved'] += saved
            
            print(f"✅ Limpeza de emergência concluída: {saved:.1f}MB liberados")
            
        except Exception as e:
            print(f"❌ Erro na limpeza de emergência: {e}")
    
    def _cleanup_chrome_orphans(self):
        """Remove processos Chrome órfãos"""
        try:
            orphan_count = 0
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                        cmdline = proc.info['cmdline'] or []
                        # Identificar processos órfãos (sem parent ou com cmdline específica)
                        if any('--type=renderer' in arg for arg in cmdline):
                            if not proc.parent() or proc.parent().name() != 'chrome.exe':
                                proc.terminate()
                                orphan_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if orphan_count > 0:
                print(f"🧹 Removidos {orphan_count} processos Chrome órfãos")
                
        except Exception as e:
            print(f"❌ Erro ao limpar processos Chrome órfãos: {e}")

class ProcessOptimizer:
    """Otimizador de processos Chrome"""
    
    @staticmethod
    def optimize_chrome_args():
        """Retorna argumentos otimizados para Chrome"""
        return [
            # Memória
            "--memory-pressure-off",
            "--max_old_space_size=4096",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            
            # CPU
            "--disable-background-mode",
            "--disable-background-networking",
            "--disable-background-sync",
            
            # Rede
            "--disable-features=VizDisplayCompositor",
            "--disable-ipc-flooding-protection",
            
            # Gráficos
            "--disable-gpu-process-crash-limit",
            "--disable-software-rasterizer",
            
            # Recursos desnecessários
            "--disable-extensions",
            "--disable-plugins",
            "--disable-images",
            "--disable-javascript",
            "--disable-web-security",
            "--disable-notifications",
            "--disable-geolocation",
            "--disable-media-stream",
            
            # Performance
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-default-apps",
            "--disable-sync",
            "--disable-translate",
            
            # Sandbox (pode ser necessário para alguns sistemas)
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
    
    @staticmethod
    def set_process_priority(pid, priority='below_normal'):
        """Define prioridade do processo"""
        try:
            process = psutil.Process(pid)
            if priority == 'below_normal':
                process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == 'nt' else 10)
            elif priority == 'low':
                process.nice(psutil.IDLE_PRIORITY_CLASS if os.name == 'nt' else 19)
            print(f"📊 Prioridade do processo {pid} definida para {priority}")
            return True
        except Exception as e:
            print(f"❌ Erro ao definir prioridade do processo {pid}: {e}")
            return False
    
    @staticmethod
    def limit_process_memory(pid, limit_mb=500):
        """Limita uso de memória do processo (Windows apenas)"""
        try:
            if os.name == 'nt':
                import win32api
                import win32process
                import win32con
                
                handle = win32api.OpenProcess(win32con.PROCESS_SET_QUOTA, False, pid)
                win32process.SetProcessWorkingSetSize(handle, -1, limit_mb * 1024 * 1024)
                win32api.CloseHandle(handle)
                print(f"📊 Limite de memória do processo {pid} definido para {limit_mb}MB")
                return True
            else:
                print("⚠️ Limitação de memória disponível apenas no Windows")
                return False
        except Exception as e:
            print(f"❌ Erro ao limitar memória do processo {pid}: {e}")
            return False

class PerformanceMonitor:
    """Monitor de performance do sistema"""
    
    def __init__(self):
        self.history = []
        self.max_history = 100
    
    def capture_snapshot(self):
        """Captura snapshot da performance"""
        try:
            snapshot = {
                'timestamp': datetime.now(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'memory_available_mb': psutil.virtual_memory().available / 1024 / 1024,
                'disk_usage_percent': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent,
                'chrome_processes': len([p for p in psutil.process_iter(['name']) if p.info['name'] and 'chrome' in p.info['name'].lower()])
            }
            
            self.history.append(snapshot)
            if len(self.history) > self.max_history:
                self.history.pop(0)
            
            return snapshot
            
        except Exception as e:
            print(f"❌ Erro ao capturar snapshot de performance: {e}")
            return None
    
    def get_average_stats(self, minutes=5):
        """Retorna estatísticas médias dos últimos minutos"""
        try:
            if not self.history:
                return None
            
            cutoff_time = datetime.now() - timedelta(minutes=minutes)
            recent_snapshots = [s for s in self.history if s['timestamp'] > cutoff_time]
            
            if not recent_snapshots:
                return None
            
            return {
                'avg_cpu_percent': sum(s['cpu_percent'] for s in recent_snapshots) / len(recent_snapshots),
                'avg_memory_percent': sum(s['memory_percent'] for s in recent_snapshots) / len(recent_snapshots),
                'avg_chrome_processes': sum(s['chrome_processes'] for s in recent_snapshots) / len(recent_snapshots),
                'min_available_memory': min(s['memory_available_mb'] for s in recent_snapshots),
                'sample_count': len(recent_snapshots)
            }
            
        except Exception as e:
            print(f"❌ Erro ao calcular estatísticas médias: {e}")
            return None

# Instância global do gerenciador de memória
memory_manager = MemoryManager()
process_optimizer = ProcessOptimizer()
performance_monitor = PerformanceMonitor()

if __name__ == "__main__":
    # Teste do sistema
    print("🧠 Iniciando teste do sistema de gerenciamento de memória...")
    
    memory_manager.start()
    
    try:
        # Capturar algumas métricas
        for i in range(5):
            stats = memory_manager.get_stats()
            print(f"📊 Iteração {i+1}: {stats}")
            time.sleep(2)
        
        # Forçar limpeza
        memory_manager.force_cleanup()
        
        # Estatísticas finais
        final_stats = memory_manager.get_stats()
        print(f"📊 Estatísticas finais: {final_stats}")
        
    except KeyboardInterrupt:
        print("⏹️ Teste interrompido pelo usuário")
    finally:
        memory_manager.stop()
        print("✅ Teste concluído")
