"""
Módulo de configuração do Bot Keydrop
Gerencia as configurações persistentes do aplicativo
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BotConfig(BaseModel):
    """Modelo de configuração do bot"""

    # Configurações principais
    num_tabs: int = Field(
        default=5, ge=1, le=100, description="Número de guias do Chrome"
    )
    execution_speed: float = Field(
        default=1.0,
        ge=0.1,
        le=10.0,
        description="Velocidade de execução (multiplicador)",
    )
    retry_attempts: int = Field(
        default=5, ge=1, le=20, description="Número de tentativas em caso de falha"
    )

    # Configurações do navegador
    headless_mode: bool = Field(default=False, description="Executar em modo headless")
    stealth_headless_mode: bool = Field(
        default=False,
        description="Executar em modo headless com proteção contra detecção",
    )
    mini_window_mode: bool = Field(
        default=False, description="Usar janelas em modo mini (200x300)"
    )
    enable_login_tabs: bool = Field(
        default=False, description="Abrir abas de login automático"
    )
    tab_proxies: Dict[int, str] = Field(
        default_factory=dict, description="Proxy por guia (tab)"
    )

    # Discord webhook
    discord_webhook_url: str = Field(
        default="", description="URL do webhook do Discord"
    )
    discord_notifications: bool = Field(
        default=True, description="Enviar notificações para Discord"
    )

    # Telegram notifications
    telegram_enabled: bool = Field(
        default=False, description="Enviar notificações pelo Telegram"
    )
    telegram_bot_token: str = Field(default="", description="Token do bot do Telegram")
    telegram_chat_id: str = Field(default="", description="Chat ID do Telegram")
    authorized_chat_ids: List[int] = Field(
        default_factory=list, description="Chats autorizados para o bot Telegram"
    )

    # Watchdog
    watchdog_enabled: bool = Field(
        default=True, description="Habilitar watchdog de abas"
    )
    watchdog_timeout: int = Field(
        default=300,
        ge=30,
        le=3600,
        description="Tempo de inatividade antes do reinício da aba (segundos)",
    )

    # URLs de destino
    keydrop_url: str = Field(
        default="https://key-drop.com/pt/", description="URL do Keydrop"
    )
    steam_login_url: str = Field(
        default="https://steamcommunity.com/login/home/?goto=",
        description="URL de login Steam",
    )

    # Configurações avançadas

    wait_time_between_actions: float = Field(
        default=2.0,
        ge=0.5,
        le=30.0,
        description="Tempo de espera entre ações (segundos)",
    )
    iteration_delay: float = Field(
        default=5.0,
        ge=0.5,
        le=60.0,
        description="Delay entre participações de cada guia (segundos)",
    )
    amateur_lottery_wait_time: int = Field(
        default=180,
        ge=60,
        le=600,
        description="Tempo de espera para sorteios AMATEUR (segundos)",
    )
    page_load_timeout: int = Field(
        default=30,
        ge=10,
        le=120,
        description="Timeout para carregamento de páginas (segundos)",
    )
    proxy_pool: List[str] = Field(
        default_factory=list,
        description="Lista de proxies disponíveis para rotacao",
    )
    proxy_timeout: int = Field(
        default=30,
        ge=5,
        le=120,
        description="Timeout para conexoes via proxy (segundos)",
    )

    # Reagendamento inteligente
    failure_reschedule_threshold: int = Field(
        default=2,
        ge=1,
        le=10,
        description="Falhas consecutivas para acionar reagendamento",
    )
    failure_reschedule_delay: int = Field(
        default=180,
        ge=60,
        le=600,
        description="Aguardar (segundos) antes de reagendar após falhas",
    )
    

    # Configurações de sistema
    max_memory_usage_mb: int = Field(
        default=2048, ge=512, le=8192, description="Uso máximo de memória (MB)"
    )
    enable_cache_clearing: bool = Field(
        default=True, description="Habilitar limpeza automática de cache"
    )

    class Config:
        """Configuração do Pydantic"""

        json_encoders = {
            # Encoders customizados se necessário
        }


class ConfigManager:
    """Gerenciador de configurações do bot"""

    def __init__(self, config_dir: Optional[str] = None):
        """
        Inicializa o gerenciador de configurações

        Args:
            config_dir: Diretório para armazenar configurações (opcional)
        """
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent
        self.config_file = self.config_dir / "bot_config.json"
        self._config: Optional[BotConfig] = None

        # Criar diretório se não existir
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Carregar configurações existentes ou criar padrão
        self.load_config()

    def load_config(self) -> BotConfig:
        """
        Carrega configurações do arquivo JSON

        Returns:
            Objeto BotConfig com configurações carregadas
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                self._config = BotConfig(**config_data)
                logger.info(f"Configurações carregadas de {self.config_file}")
            else:
                self._config = BotConfig()
                self.save_config()  # Salvar configurações padrão
                logger.info("Configurações padrão criadas")

        except Exception as e:
            logger.error(f"Erro ao carregar configurações: {e}")
            self._config = BotConfig()  # Usar configurações padrão em caso de erro

        return self._config

    def save_config(self) -> bool:
        """
        Salva configurações no arquivo JSON

        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            config_dict = self._config.dict()
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            logger.info(f"Configurações salvas em {self.config_file}")
            return True

        except Exception as e:
            logger.error(f"Erro ao salvar configurações: {e}")
            return False

    def update_config(self, **kwargs) -> bool:
        """
        Atualiza configurações com novos valores

        Args:
            **kwargs: Valores de configuração para atualizar

        Returns:
            True se atualizou com sucesso, False caso contrário
        """
        try:
            # Atualizar apenas campos válidos
            config_dict = self._config.dict()
            config_dict.update(kwargs)
            self._config = BotConfig(**config_dict)
            return self.save_config()

        except Exception as e:
            logger.error(f"Erro ao atualizar configurações: {e}")
            return False

    def get_config(self) -> BotConfig:
        """
        Retorna as configurações atuais

        Returns:
            Objeto BotConfig atual
        """
        if self._config is None:
            self.load_config()
        return self._config

    def reset_to_defaults(self) -> bool:
        """
        Reseta configurações para os valores padrão

        Returns:
            True se resetou com sucesso, False caso contrário
        """
        try:
            self._config = BotConfig()
            return self.save_config()

        except Exception as e:
            logger.error(f"Erro ao resetar configurações: {e}")
            return False

    def export_config(self, file_path: str) -> bool:
        """
        Exporta configurações para um arquivo específico

        Args:
            file_path: Caminho do arquivo para exportar

        Returns:
            True se exportou com sucesso, False caso contrário
        """
        try:
            config_dict = self._config.dict()
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            logger.info(f"Configurações exportadas para {file_path}")
            return True

        except Exception as e:
            logger.error(f"Erro ao exportar configurações: {e}")
            return False

    def import_config(self, file_path: str) -> bool:
        """
        Importa configurações de um arquivo específico

        Args:
            file_path: Caminho do arquivo para importar

        Returns:
            True se importou com sucesso, False caso contrário
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            self._config = BotConfig(**config_data)
            self.save_config()
            logger.info(f"Configurações importadas de {file_path}")
            return True

        except Exception as e:
            logger.error(f"Erro ao importar configurações: {e}")
            return False

    def validate_config(self) -> Dict[str, Any]:
        """
        Valida as configurações atuais

        Returns:
            Dicionário com resultado da validação
        """
        try:
            # Tenta criar um novo objeto para validar
            BotConfig(**self._config.dict())
            return {"valid": True, "errors": [], "warnings": []}

        except Exception as e:
            return {"valid": False, "errors": [str(e)], "warnings": []}


# Instância global do gerenciador de configurações
config_manager = ConfigManager()


def get_config() -> BotConfig:
    """
    Função utilitária para obter configurações

    Returns:
        Configurações atuais do bot
    """
    return config_manager.get_config()


def save_config(**kwargs) -> bool:
    """
    Função utilitária para salvar configurações

    Args:
        **kwargs: Configurações para atualizar

    Returns:
        True se salvou com sucesso
    """
    return config_manager.update_config(**kwargs)
