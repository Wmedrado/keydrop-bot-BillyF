"""
Módulo de integração com Discord
Gerencia notificações via webhook do Discord
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from discord_webhook import DiscordWebhook, DiscordEmbed
import json

from ..notifications.notification_worker import OfflineNotificationQueue

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class NotificationData:
    """Dados para notificação do Discord"""
    title: str
    description: str
    color: int = 0x3498db  # Azul padrão
    fields: Optional[List[Dict[str, Any]]] = None
    timestamp: Optional[datetime] = None
    footer_text: Optional[str] = None
    thumbnail_url: Optional[str] = None
    author_name: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.fields is None:
            self.fields = []


class DiscordNotifier:
    """Classe para gerenciar notificações do Discord"""
    
    # Cores para diferentes tipos de notificação
    COLORS = {
        'success': 0x2ecc71,  # Verde
        'error': 0xe74c3c,    # Vermelho
        'warning': 0xf39c12,  # Laranja
        'info': 0x3498db,     # Azul
        'system': 0x9b59b6    # Roxo
    }
    
    def __init__(self, webhook_url: Optional[str] = None):
        """
        Inicializa o notificador do Discord
        
        Args:
            webhook_url: URL do webhook do Discord
        """
        self.webhook_url = webhook_url
        self.enabled = bool(webhook_url)
        self.bot_name = "Keydrop Bot Professional"
        self.bot_version = "2.1.0"
        self.developer_credit = "William Medrado (wmedrado) github"
        
        if self.enabled:
            logger.info("Discord notifier inicializado com webhook configurado")
        else:
            logger.warning("Discord notifier inicializado sem webhook - notificações desabilitadas")
    
    def update_webhook_url(self, webhook_url: Optional[str]) -> None:
        """
        Atualiza a URL do webhook
        
        Args:
            webhook_url: Nova URL do webhook
        """
        self.webhook_url = webhook_url
        self.enabled = bool(webhook_url)
        
        if self.enabled:
            logger.info("Webhook do Discord atualizado")
        else:
            logger.info("Webhook do Discord removido - notificações desabilitadas")
    
    async def send_notification(self, notification: NotificationData) -> bool:
        """
        Envia notificação para o Discord
        
        Args:
            notification: Dados da notificação
            
        Returns:
            True se enviou com sucesso, False caso contrário
        """
        if not self.enabled:
            logger.debug("Notificação Discord ignorada - webhook não configurado")
            return False
        
        try:
            # Criar webhook
            webhook = DiscordWebhook(url=self.webhook_url, username=self.bot_name)
            
            # Criar embed
            embed = DiscordEmbed(
                title=notification.title,
                description=notification.description,
                color=notification.color,
                timestamp=notification.timestamp
            )
            
            # Adicionar campos
            if notification.fields:
                for field in notification.fields:
                    embed.add_embed_field(
                        name=field.get('name', ''),
                        value=field.get('value', ''),
                        inline=field.get('inline', False)
                    )
            
            # Configurar footer
            footer_text = notification.footer_text or f"{self.bot_name} v{self.bot_version} | {self.developer_credit}"
            embed.set_footer(text=footer_text)
            
            # Configurar thumbnail se fornecido
            if notification.thumbnail_url:
                embed.set_thumbnail(url=notification.thumbnail_url)
            
            # Configurar autor se fornecido
            if notification.author_name:
                embed.set_author(name=notification.author_name)
            
            # Adicionar embed ao webhook
            webhook.add_embed(embed)
            
            # Enviar notificação
            response = webhook.execute()
            
            if response.status_code == 200:
                logger.debug(f"Notificação Discord enviada: {notification.title}")
                return True
            else:
                logger.error(f"Erro ao enviar notificação Discord: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao enviar notificação Discord: {e}")
            return False
    
    async def send_bot_start_notification(self, config_data: Dict[str, Any]) -> bool:
        """
        Envia notificação de início do bot
        
        Args:
            config_data: Dados de configuração do bot
            
        Returns:
            True se enviou com sucesso
        """
        notification = NotificationData(
            title="🚀 Bot Iniciado",
            description="O Keydrop Bot foi iniciado com sucesso!",
            color=self.COLORS['success'],
            fields=[
                {
                    'name': '📊 Configuração',
                    'value': f"**Guias:** {config_data.get('num_tabs', 'N/A')}\n"
                           f"**Velocidade:** {config_data.get('execution_speed', 'N/A')}x\n"
                           f"**Tentativas:** {config_data.get('retry_attempts', 'N/A')}",
                    'inline': True
                },
                {
                    'name': '⚙️ Modo',
                    'value': f"**Headless:** {'✅' if config_data.get('headless_mode') else '❌'}\n"
                           f"**Stealth Headless:** {'✅' if config_data.get('stealth_headless_mode') else '❌'}\n"
                           f"**Mini Window:** {'✅' if config_data.get('mini_window_mode') else '❌'}\n"
                           f"**Login Tabs:** {'✅' if config_data.get('enable_login_tabs') else '❌'}",
                    'inline': True
                },
                {
                    'name': '🕐 Horário de Início',
                    'value': datetime.now().strftime('%d/%m/%Y às %H:%M:%S'),
                    'inline': False
                }
            ]
        )
        
        return await self.send_notification(notification)
    
    async def send_bot_stop_notification(self, stats: Optional[Dict[str, Any]] = None) -> bool:
        """
        Envia notificação de parada do bot
        
        Args:
            stats: Estatísticas da sessão (opcional)
            
        Returns:
            True se enviou com sucesso
        """
        description = "O Keydrop Bot foi parado."
        fields = []
        
        if stats:
            description = "O Keydrop Bot foi parado. Aqui está o resumo da sessão:"
            fields.extend([
                {
                    'name': '📈 Estatísticas da Sessão',
                    'value': f"**Participações:** {stats.get('total_participations', 0)}\n"
                           f"**Sucessos:** {stats.get('successful_participations', 0)}\n"
                           f"**Falhas:** {stats.get('failed_participations', 0)}",
                    'inline': True
                },
                {
                    'name': '⏱️ Tempo Total',
                    'value': stats.get('session_duration', 'N/A'),
                    'inline': True
                }
            ])
        
        fields.append({
            'name': '🕐 Horário de Parada',
            'value': datetime.now().strftime('%d/%m/%Y às %H:%M:%S'),
            'inline': False
        })
        
        notification = NotificationData(
            title="⏹️ Bot Parado",
            description=description,
            color=self.COLORS['warning'],
            fields=fields
        )
        
        return await self.send_notification(notification)
    
    async def send_error_notification(self, error_message: str, tab_id: Optional[int] = None, details: Optional[Dict[str, Any]] = None) -> bool:
        """
        Envia notificação de erro
        
        Args:
            error_message: Mensagem de erro
            tab_id: ID da guia onde ocorreu o erro (opcional)
            details: Detalhes adicionais do erro (opcional)
            
        Returns:
            True se enviou com sucesso
        """
        fields = []
        
        if tab_id is not None:
            fields.append({
                'name': '🏷️ Guia',
                'value': f"ID: {tab_id}",
                'inline': True
            })
        
        if details:
            for key, value in details.items():
                fields.append({
                    'name': f'📋 {key.title()}',
                    'value': str(value),
                    'inline': True
                })
        
        fields.append({
            'name': '🕐 Horário do Erro',
            'value': datetime.now().strftime('%d/%m/%Y às %H:%M:%S'),
            'inline': False
        })
        
        notification = NotificationData(
            title="❌ Erro Detectado",
            description=f"**Erro:** {error_message}",
            color=self.COLORS['error'],
            fields=fields
        )
        
        return await self.send_notification(notification)
    
    async def send_success_notification(self, message: str, tab_id: Optional[int] = None, details: Optional[Dict[str, Any]] = None) -> bool:
        """
        Envia notificação de sucesso
        
        Args:
            message: Mensagem de sucesso
            tab_id: ID da guia (opcional)
            details: Detalhes adicionais (opcional)
            
        Returns:
            True se enviou com sucesso
        """
        fields = []
        
        if tab_id is not None:
            fields.append({
                'name': '🏷️ Guia',
                'value': f"ID: {tab_id}",
                'inline': True
            })
        
        if details:
            for key, value in details.items():
                fields.append({
                    'name': f'📋 {key.title()}',
                    'value': str(value),
                    'inline': True
                })
        
        notification = NotificationData(
            title="✅ Sucesso",
            description=message,
            color=self.COLORS['success'],
            fields=fields
        )
        
        return await self.send_notification(notification)
    
    async def send_system_report(self, system_metrics: Dict[str, Any]) -> bool:
        """
        Envia relatório de sistema
        
        Args:
            system_metrics: Métricas do sistema
            
        Returns:
            True se enviou com sucesso
        """
        notification = NotificationData(
            title="📊 Relatório do Sistema",
            description="Métricas atuais de performance do sistema:",
            color=self.COLORS['system'],
            fields=[
                {
                    'name': '🖥️ CPU',
                    'value': f"**Uso:** {system_metrics.get('cpu_percent', 'N/A')}\n"
                           f"**Cores:** {system_metrics.get('cpu_cores', 'N/A')}\n"
                           f"**Freq:** {system_metrics.get('cpu_frequency', 'N/A')}",
                    'inline': True
                },
                {
                    'name': '💾 Memória',
                    'value': f"**Usada:** {system_metrics.get('memory_used', 'N/A')}\n"
                           f"**Total:** {system_metrics.get('memory_total', 'N/A')}\n"
                           f"**Uso:** {system_metrics.get('memory_percent', 'N/A')}",
                    'inline': True
                },
                {
                    'name': '💽 Disco',
                    'value': f"**Usado:** {system_metrics.get('disk_used', 'N/A')}\n"
                           f"**Total:** {system_metrics.get('disk_total', 'N/A')}\n"
                           f"**Uso:** {system_metrics.get('disk_percent', 'N/A')}",
                    'inline': True
                },
                {
                    'name': '🌐 Rede',
                    'value': f"**Enviado:** {system_metrics.get('network_sent', 'N/A')}\n"
                           f"**Recebido:** {system_metrics.get('network_received', 'N/A')}",
                    'inline': True
                },
                {
                    'name': '⏰ Sistema',
                    'value': f"**Uptime:** {system_metrics.get('uptime', 'N/A')}\n"
                           f"**Timestamp:** {system_metrics.get('timestamp', 'N/A')}",
                    'inline': True
                }
            ]
        )
        
        return await self.send_notification(notification)
    
    async def send_participation_report(self, report_data: Dict[str, Any]) -> bool:
        """
        Envia relatório de participações
        
        Args:
            report_data: Dados do relatório
            
        Returns:
            True se enviou com sucesso
        """
        success_rate = 0
        if report_data.get('total_attempts', 0) > 0:
            success_rate = (report_data.get('successful_participations', 0) / report_data.get('total_attempts', 1)) * 100
        
        notification = NotificationData(
            title="📈 Relatório de Participações",
            description="Resumo das atividades do bot:",
            color=self.COLORS['info'],
            fields=[
                {
                    'name': '🎯 Participações',
                    'value': f"**Total:** {report_data.get('total_attempts', 0)}\n"
                           f"**Sucessos:** {report_data.get('successful_participations', 0)}\n"
                           f"**Falhas:** {report_data.get('failed_participations', 0)}",
                    'inline': True
                },
                {
                    'name': '📊 Taxa de Sucesso',
                    'value': f"{success_rate:.1f}%",
                    'inline': True
                },
                {
                    'name': '🕐 Período',
                    'value': f"**Início:** {report_data.get('start_time', 'N/A')}\n"
                           f"**Duração:** {report_data.get('duration', 'N/A')}",
                    'inline': False
                }
            ]
        )
        
        if 'profits' in report_data and report_data['profits']:
            notification.fields.append({
                'name': '💰 Lucros',
                'value': str(report_data['profits']),
                'inline': True
            })
        
        return await self.send_notification(notification)
    
    async def send_custom_notification(self, title: str, description: str, notification_type: str = 'info', **kwargs) -> bool:
        """
        Envia notificação personalizada
        
        Args:
            title: Título da notificação
            description: Descrição da notificação
            notification_type: Tipo da notificação (success, error, warning, info, system)
            **kwargs: Argumentos adicionais
            
        Returns:
            True se enviou com sucesso
        """
        color = self.COLORS.get(notification_type, self.COLORS['info'])
        
        notification = NotificationData(
            title=title,
            description=description,
            color=color,
            **kwargs
        )
        
        return await self.send_notification(notification)


# Instância global do notificador
discord_notifier = DiscordNotifier()


async def send_discord_notification_now(title: str, description: str, notification_type: str = 'info', **kwargs) -> bool:
    """Send a Discord notification immediately."""
    return await discord_notifier.send_custom_notification(title, description, notification_type, **kwargs)

async def send_discord_notification(title: str, description: str, notification_type: str = 'info', **kwargs) -> bool:
    """
    Função utilitária para enviar notificação
    
    Args:
        title: Título da notificação
        description: Descrição
        notification_type: Tipo da notificação
        **kwargs: Argumentos adicionais
        
    Returns:
        True se mensagem foi adicionada à fila
    """
    critical = kwargs.pop('critical', False)
    notification = {
        "type": "discord",
        "data": {
            "title": title,
            "description": description,
            "notification_type": notification_type,
            "kwargs": kwargs,
        },
        "critical": critical,
        "retries": 0,
    }
    OfflineNotificationQueue.enqueue(notification, priority=critical)
    return True

def configure_discord_webhook(webhook_url: Optional[str]) -> None:
    """
    Configura o webhook do Discord
    
    Args:
        webhook_url: URL do webhook
    """
    discord_notifier.update_webhook_url(webhook_url)
