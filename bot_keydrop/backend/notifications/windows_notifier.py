import logging

try:
    from win10toast import ToastNotifier
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    ToastNotifier = None

logger = logging.getLogger(__name__)

_toaster = ToastNotifier() if ToastNotifier else None

def send_windows_notification(title: str, message: str, duration: int = 5) -> bool:
    """Envia notificação nativa do Windows."""
    if _toaster is None:
        logger.warning("win10toast não está instalado; ignorando notificação")
        return False
    try:
        _toaster.show_toast(title, message, duration=duration)
        return True
    except Exception as e:  # pragma: no cover - apenas log
        logger.error(f"Erro ao exibir notificação Windows: {e}")
        return False
