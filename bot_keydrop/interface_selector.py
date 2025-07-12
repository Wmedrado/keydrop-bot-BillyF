import os
import threading
import time
import requests
import webbrowser
from pathlib import Path

import uvicorn

BACKEND_PORT = 8000
BACKEND_URL = f"http://localhost:{BACKEND_PORT}"


def start_backend():
    """Start FastAPI server in a background thread."""
    backend_dir = Path(__file__).parent / "backend"

    def run():
        os.chdir(backend_dir)
        uvicorn.run("main:app", host="localhost", port=BACKEND_PORT, log_level="info")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread


def wait_for_backend(max_retries: int = 30) -> bool:
    for _ in range(max_retries):
        try:
            requests.get(f"{BACKEND_URL}/health", timeout=1)
            return True
        except Exception:
            time.sleep(1)
    return False


def choose_interface() -> str:
    print("Selecione a interface de usuário:")
    print("1 - Interface Clássica (Web)")
    print("2 - Interface Moderna (DearPyGUI)")
    choice = input("Opção [1/2]: ").strip()
    return "modern" if choice == "2" else "classic"


def run_classic():
    webbrowser.open(BACKEND_URL)
    print(f"Interface web disponível em {BACKEND_URL}")
    print("Pressione Ctrl+C para encerrar.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


def run_modern():
    from modern_gui import run_modern_gui
    run_modern_gui(BACKEND_URL)


def main():
    start_backend()
    if not wait_for_backend():
        print("Erro ao iniciar o backend.")
        return

    interface = choose_interface()
    if interface == "modern":
        run_modern()
    else:
        run_classic()


if __name__ == "__main__":
    main()
