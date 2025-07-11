"""
Inicializador do módulo de integração com Discord
"""

from .notifier import DiscordNotifier, NotificationData, send_discord_notification, configure_discord_webhook

__all__ = ['DiscordNotifier', 'NotificationData', 'send_discord_notification', 'configure_discord_webhook']
