import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
from pathlib import Path
import atexit

# Early CLI handling for optional watch mode
if "--watch" in sys.argv:
    from bot_keydrop.live_monitor import watch

    watch()
    sys.exit(0)

from bot_keydrop.system_safety import (
    LockFile,
    install_crash_debug,
    send_log_to_discord,
)
import diagnostic

if os.getenv("MODO_DEBUG") == "1" or Path(sys.argv[0]).stem.endswith("_DEBUG"):
    os.environ["MODO_DEBUG"] = "1"
    install_crash_debug()
    try:
        if not diagnostic.run_diagnostic():
            messagebox.showerror(
                "Diagn\u00f3stico", "Falha na verifica\u00e7\u00e3o do sistema"
            )
            sys.exit(1)
        import debug_tester

        debug_tester.main()
        send_log_to_discord(Path("logs/bot_engine.log"))
    except Exception as exc:
        print(f"Falha ao executar debug_tester: {exc}")

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent

BACKEND_DIR = BASE_DIR / "bot_keydrop" / "backend"
GUI_SCRIPT = BASE_DIR / "bot_keydrop" / "keydrop_bot_desktop.py"

lock = LockFile()
if not lock.acquire():
    messagebox.showerror("Erro", "O Keydrop Bot já está em execução!")
    sys.exit(1)
atexit.register(lock.release)

selected_mode = None


def run_api():
    """Execute only the FastAPI backend."""
    try:
        return subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "main:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
            ],
            cwd=BACKEND_DIR,
        )
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


def on_select(mode: str) -> None:
    """Callback to store selected mode and close the selection window."""
    global selected_mode
    selected_mode = mode
    root.destroy()


root = tk.Tk()
root.title("Keydrop Bot - Selecione o Modo")
root.geometry("420x250")
root.resizable(False, False)

# Use packaged directory when running as executable
icon_path = BASE_DIR / "bot-icone.ico"
if icon_path.exists():
    try:
        root.iconbitmap(icon_path)
    except Exception:
        pass

main_label = ttk.Label(
    root, text="Keydrop Bot - Selecione o Modo", font=("Arial", 14, "bold")
)
main_label.pack(pady=10)

tooltip_var = tk.StringVar(value="Passe o cursor sobre um botão para detalhes")

btn_gui = ttk.Button(
    root, text="Interface Gráfica (GUI)", command=lambda: on_select("gui")
)
btn_api = ttk.Button(root, text="API WebSocket", command=lambda: on_select("api"))
btn_both = ttk.Button(root, text="GUI + API", command=lambda: on_select("both"))

for btn in (btn_gui, btn_api, btn_both):
    btn.pack(pady=5, ipadx=10, fill="x", padx=40)

tt_label = ttk.Label(root, textvariable=tooltip_var, foreground="gray")
tt_label.pack(pady=10)


def open_logs(_event=None) -> None:
    log = Path("logs/bot_engine.log")
    if not log.exists():
        messagebox.showinfo("Logs", f"Arquivo {log} nao encontrado")
        return
    try:
        if os.name == "nt":
            os.startfile(log)
        else:
            subprocess.Popen(["xdg-open", str(log)])
    except Exception as exc:
        messagebox.showerror("Erro", f"Falha ao abrir log: {exc}")


if os.getenv("MODO_DEBUG") == "1":
    root.bind("<F12>", open_logs)


def bind_tip(widget: "tk.Widget", text: str) -> None:
    """Display a tooltip when hovering over a widget."""
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
