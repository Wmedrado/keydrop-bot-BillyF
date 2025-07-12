import os
import sys
import time
import subprocess
from pathlib import Path

BACKEND_DIR = Path(__file__).parent / "bot_keydrop" / "backend"
GUI_SCRIPT = Path(__file__).parent / "bot_keydrop" / "keydrop_bot_complete.py"


def start_gui() -> subprocess.Popen:
    """Start the desktop GUI in a separate process."""
    cmd = [sys.executable, str(GUI_SCRIPT)]
    return subprocess.Popen(cmd)


def start_api() -> subprocess.Popen:
    """Start the FastAPI backend in a separate process."""
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "main:app",
        "--host",
        "localhost",
        "--port",
        "8000",
    ]
    return subprocess.Popen(cmd, cwd=BACKEND_DIR)


def main() -> None:
    print("Selecione o modo de execução:")
    print("1 - Iniciar GUI local")
    print("2 - Iniciar API com WebSocket")
    print("3 - Iniciar ambos")
    choice = input("Opção [1/2/3]: ").strip()

    processes = []
    try:
        if choice == "1":
            processes.append(start_gui())
        elif choice == "2":
            processes.append(start_api())
        else:
            processes.append(start_api())
            time.sleep(2)
            processes.append(start_gui())

        # keep running until user interrupts
        print("Pressione Ctrl+C para encerrar.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEncerrando...")
    finally:
        for proc in processes:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()


if __name__ == "__main__":
    main()
