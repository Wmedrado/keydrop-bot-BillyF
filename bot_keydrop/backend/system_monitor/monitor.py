"""
Módulo de monitoramento de sistema
Coleta dados de performance do computador usando psutil
"""

import psutil
import time
import asyncio
from log_utils import setup_logger
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

# Configuração de logging
logger = setup_logger(__name__)


@dataclass
class SystemMetrics:
    """Classe para armazenar métricas do sistema"""
    
    # CPU
    cpu_percent: float
    cpu_count: int
    cpu_freq_current: float
    cpu_freq_max: float
    
    # Memória
    memory_total: int  # bytes
    memory_available: int  # bytes
    memory_used: int  # bytes
    memory_percent: float
    
    # Disco
    disk_total: int  # bytes
    disk_used: int  # bytes
    disk_free: int  # bytes
    disk_percent: float
    
    # Rede
    network_bytes_sent: int
    network_bytes_recv: int
    network_packets_sent: int
    network_packets_recv: int
    
    # Sistema
    boot_time: float
    uptime: float
    timestamp: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return asdict(self)
    
    def to_human_readable(self) -> Dict[str, str]:
        """Converte para formato legível por humanos"""
        return {
            'cpu_percent': f"{self.cpu_percent:.1f}%",
            'cpu_cores': str(self.cpu_count),
            'cpu_frequency': f"{self.cpu_freq_current:.0f} MHz",
            'memory_total': self._bytes_to_gb(self.memory_total),
            'memory_used': self._bytes_to_gb(self.memory_used),
            'memory_available': self._bytes_to_gb(self.memory_available),
            'memory_percent': f"{self.memory_percent:.1f}%",
            'disk_total': self._bytes_to_gb(self.disk_total),
            'disk_used': self._bytes_to_gb(self.disk_used),
            'disk_free': self._bytes_to_gb(self.disk_free),
            'disk_percent': f"{self.disk_percent:.1f}%",
            'network_sent': self._bytes_to_gb(self.network_bytes_sent),
            'network_received': self._bytes_to_gb(self.network_bytes_recv),
            'uptime': self._seconds_to_time(self.uptime),
            'timestamp': datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @staticmethod
    def _bytes_to_gb(bytes_value: int) -> str:
        """Converte bytes para GB"""
        gb_value = bytes_value / (1024 ** 3)
        return f"{gb_value:.2f} GB"
    
    @staticmethod
    def _seconds_to_time(seconds: float) -> str:
        """Converte segundos para formato de tempo legível"""
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class SystemMonitor:
    """Monitor de sistema em tempo real"""
    
    def __init__(self, update_interval: float = 1.0):
        """
        Inicializa o monitor de sistema
        
        Args:
            update_interval: Intervalo de atualização em segundos
        """
        self.update_interval = update_interval
        self.is_monitoring = False
        self._metrics_history: List[SystemMetrics] = []
        self._max_history_size = 100  # Manter últimas 100 medições
        self._boot_time = psutil.boot_time()
        
        # Métricas iniciais de rede para calcular delta
        net_io = psutil.net_io_counters()
        self._initial_bytes_sent = net_io.bytes_sent
        self._initial_bytes_recv = net_io.bytes_recv
        self._initial_packets_sent = net_io.packets_sent
        self._initial_packets_recv = net_io.packets_recv
        
        logger.info("Monitor de sistema inicializado")
    
    def get_current_metrics(self) -> SystemMetrics:
        """
        Coleta métricas atuais do sistema
        
        Returns:
            Objeto SystemMetrics com dados atuais
        """
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            cpu_freq_current = cpu_freq.current if cpu_freq else 0
            cpu_freq_max = cpu_freq.max if cpu_freq else 0
            
            # Memória
            memory = psutil.virtual_memory()
            
            # Disco (pasta raiz)
            disk = psutil.disk_usage('/')
            
            # Rede
            net_io = psutil.net_io_counters()
            
            # Sistema
            current_time = time.time()
            uptime = current_time - self._boot_time
            
            metrics = SystemMetrics(
                cpu_percent=cpu_percent,
                cpu_count=cpu_count,
                cpu_freq_current=cpu_freq_current,
                cpu_freq_max=cpu_freq_max,
                memory_total=memory.total,
                memory_available=memory.available,
                memory_used=memory.used,
                memory_percent=memory.percent,
                disk_total=disk.total,
                disk_used=disk.used,
                disk_free=disk.free,
                disk_percent=(disk.used / disk.total) * 100,
                network_bytes_sent=net_io.bytes_sent - self._initial_bytes_sent,
                network_bytes_recv=net_io.bytes_recv - self._initial_bytes_recv,
                network_packets_sent=net_io.packets_sent - self._initial_packets_sent,
                network_packets_recv=net_io.packets_recv - self._initial_packets_recv,
                boot_time=self._boot_time,
                uptime=uptime,
                timestamp=current_time
            )
            
            # Adicionar ao histórico
            self._add_to_history(metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Erro ao coletar métricas do sistema: {e}")
            # Retornar métricas zeradas em caso de erro
            return SystemMetrics(
                cpu_percent=0.0, cpu_count=0, cpu_freq_current=0.0, cpu_freq_max=0.0,
                memory_total=0, memory_available=0, memory_used=0, memory_percent=0.0,
                disk_total=0, disk_used=0, disk_free=0, disk_percent=0.0,
                network_bytes_sent=0, network_bytes_recv=0,
                network_packets_sent=0, network_packets_recv=0,
                boot_time=0.0, uptime=0.0, timestamp=time.time()
            )
    
    def _add_to_history(self, metrics: SystemMetrics) -> None:
        """
        Adiciona métricas ao histórico
        
        Args:
            metrics: Métricas para adicionar
        """
        self._metrics_history.append(metrics)
        
        # Manter apenas os últimos registros
        if len(self._metrics_history) > self._max_history_size:
            self._metrics_history.pop(0)
    
    def get_metrics_history(self, last_n: Optional[int] = None) -> List[SystemMetrics]:
        """
        Retorna histórico de métricas
        
        Args:
            last_n: Número de últimas métricas (opcional)
            
        Returns:
            Lista de métricas históricas
        """
        if last_n is None:
            return self._metrics_history.copy()
        else:
            return self._metrics_history[-last_n:]
    
    def get_average_metrics(self, time_window_minutes: int = 5) -> Optional[SystemMetrics]:
        """
        Calcula métricas médias em uma janela de tempo
        
        Args:
            time_window_minutes: Janela de tempo em minutos
            
        Returns:
            Métricas médias ou None se não há dados suficientes
        """
        if not self._metrics_history:
            return None
        
        current_time = time.time()
        cutoff_time = current_time - (time_window_minutes * 60)
        
        # Filtrar métricas na janela de tempo
        recent_metrics = [
            m for m in self._metrics_history 
            if m.timestamp >= cutoff_time
        ]
        
        if not recent_metrics:
            return None
        
        # Calcular médias
        avg_cpu = sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
        avg_memory_percent = sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
        avg_disk_percent = sum(m.disk_percent for m in recent_metrics) / len(recent_metrics)
        
        # Usar dados mais recentes para valores absolutos
        latest = recent_metrics[-1]
        
        return SystemMetrics(
            cpu_percent=avg_cpu,
            cpu_count=latest.cpu_count,
            cpu_freq_current=latest.cpu_freq_current,
            cpu_freq_max=latest.cpu_freq_max,
            memory_total=latest.memory_total,
            memory_available=latest.memory_available,
            memory_used=latest.memory_used,
            memory_percent=avg_memory_percent,
            disk_total=latest.disk_total,
            disk_used=latest.disk_used,
            disk_free=latest.disk_free,
            disk_percent=avg_disk_percent,
            network_bytes_sent=latest.network_bytes_sent,
            network_bytes_recv=latest.network_bytes_recv,
            network_packets_sent=latest.network_packets_sent,
            network_packets_recv=latest.network_packets_recv,
            boot_time=latest.boot_time,
            uptime=latest.uptime,
            timestamp=latest.timestamp
        )
    
    async def start_monitoring(self, callback=None):
        """
        Inicia monitoramento contínuo
        
        Args:
            callback: Função a ser chamada a cada atualização (opcional)
        """
        self.is_monitoring = True
        logger.info("Monitoramento de sistema iniciado")
        
        while self.is_monitoring:
            try:
                metrics = self.get_current_metrics()
                
                if callback:
                    await callback(metrics)
                
                await asyncio.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"Erro durante monitoramento: {e}")
                await asyncio.sleep(self.update_interval)
    
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.is_monitoring = False
        logger.info("Monitoramento de sistema parado")
    
    def get_process_info(self, process_name: str) -> List[Dict[str, Any]]:
        """
        Obtém informações de processos específicos
        
        Args:
            process_name: Nome do processo a buscar
            
        Returns:
            Lista de informações dos processos encontrados
        """
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                if process_name.lower() in proc.info['name'].lower():
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_mb': proc.info['memory_info'].rss / (1024 * 1024) if proc.info['memory_info'] else 0
                    })
                    
        except Exception as e:
            logger.error(f"Erro ao buscar processos {process_name}: {e}")
        
        return processes
    
    def get_chrome_processes(self) -> List[Dict[str, Any]]:
        """
        Obtém informações específicas dos processos do Chrome
        
        Returns:
            Lista de processos do Chrome
        """
        return self.get_process_info("chrome")


# Instância global do monitor
system_monitor = SystemMonitor()

async def get_system_metrics() -> SystemMetrics:
    """
    Função utilitária para obter métricas atuais
    
    Returns:
        Métricas atuais do sistema
    """
    return system_monitor.get_current_metrics()

async def start_system_monitoring(callback=None):
    """
    Inicia monitoramento global do sistema
    
    Args:
        callback: Função de callback para receber métricas
    """
    await system_monitor.start_monitoring(callback)

def stop_system_monitoring():
    """Para o monitoramento global do sistema"""
    system_monitor.stop_monitoring()
