import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "bot_keydrop" / "backend"
GUI_SCRIPT = BASE_DIR / "bot_keydrop" / "keydrop_bot_desktop.py"

selected_mode = None


def run_api():
    """Execute only the FastAPI backend."""
    try:
        return subprocess.Popen([
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ], cwd=BACKEND_DIR)
    except Exception as exc:
        messagebox.showerror("Erro", f"Falha ao iniciar API:\n{exc}")
        return None


def run_gui():
    """Execute only the desktop GUI."""
    try:
        return subprocess.Popen([sys.executable, str(GUI_SCRIPT)])
    except Exception as exc:
        messagebox.showerror("Erro", f"Falha ao iniciar GUI:\n{exc}")
        return None


def run_both():
    """Run GUI and API concurrently."""
    api_proc = run_api()
    if not api_proc:
        return
    gui_proc = run_gui()
    if gui_proc:
        try:
            gui_proc.wait()
        finally:
            api_proc.terminate()
            api_proc.wait()
    else:
        api_proc.terminate()
        api_proc.wait()


def on_select(mode: str):
    global selected_mode
    selected_mode = mode
    root.destroy()


root = tk.Tk()
root.title("Keydrop Bot - Selecione o Modo")
root.geometry("420x250")
root.resizable(False, False)

main_label = ttk.Label(root, text="Keydrop Bot - Selecione o Modo", font=("Arial", 14, "bold"))
main_label.pack(pady=10)

tooltip_var = tk.StringVar(value="Passe o cursor sobre um botão para detalhes")

btn_gui = ttk.Button(root, text="Interface Gráfica (GUI)", command=lambda: on_select("gui"))
btn_api = ttk.Button(root, text="API WebSocket", command=lambda: on_select("api"))
btn_both = ttk.Button(root, text="GUI + API", command=lambda: on_select("both"))

for btn in (btn_gui, btn_api, btn_both):
    btn.pack(pady=5, ipadx=10, fill="x", padx=40)

tt_label = ttk.Label(root, textvariable=tooltip_var, foreground="gray")
tt_label.pack(pady=10)


def bind_tip(widget, text):
    widget.bind("<Enter>", lambda _e, t=text: tooltip_var.set(t))
    widget.bind("<Leave>", lambda _e: tooltip_var.set(""))

bind_tip(btn_gui, "Executa somente a interface desktop do bot")
bind_tip(btn_api, "Inicia apenas a API FastAPI/WebSocket")
bind_tip(btn_both, "Executa GUI e API em paralelo")

root.mainloop()

# Start selected mode
if selected_mode == "gui":
    proc = run_gui()
    if proc:
        proc.wait()
elif selected_mode == "api":
    proc = run_api()
    if proc:
        proc.wait()
elif selected_mode == "both":
    run_both()

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
