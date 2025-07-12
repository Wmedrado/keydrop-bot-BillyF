import socket
import time

def verificar_conexao_internet(host="8.8.8.8", port=53, timeout=3, retries=3, delay=5):
    """Check internet connectivity by attempting a TCP connection."""
    for _ in range(retries):
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            time.sleep(delay)
    return False
