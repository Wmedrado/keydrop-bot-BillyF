import logging
import requests

logger = logging.getLogger(__name__)


def send_telegram_message(token: str, chat_id: str, text: str) -> bool:
    """Envia mensagem para um bot do Telegram."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, data={'chat_id': chat_id, 'text': text})
        if resp.status_code == 200:
            data = resp.json()
            return data.get('ok', False)
        return False
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem Telegram: {e}")
        return False
