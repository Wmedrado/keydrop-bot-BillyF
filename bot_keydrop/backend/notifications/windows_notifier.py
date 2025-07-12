import logging
from win10toast import ToastNotifier

logger = logging.getLogger(__name__)

_toaster = ToastNotifier()

def send_windows_notification(title: str, message: str, duration: int = 5) -> bool:
    """Envia notificação nativa do Windows."""
    try:
        _toaster.show_toast(title, message, duration=duration)
        return True
    except Exception as e:
        logger.error(f"Erro ao exibir notificação Windows: {e}")
        return False
