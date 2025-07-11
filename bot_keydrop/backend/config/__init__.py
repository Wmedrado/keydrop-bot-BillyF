"""
Inicializador do módulo de configuração
"""

from .config_manager import ConfigManager, BotConfig, get_config, save_config

__all__ = ['ConfigManager', 'BotConfig', 'get_config', 'save_config']
