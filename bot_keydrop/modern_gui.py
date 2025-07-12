import threading
import time
import requests
import dearpygui.dearpygui as dpg

API_URL = "http://localhost:8000"

STATUS_TAG = "status_text"
CPU_TAG = "cpu_text"
RAM_TAG = "ram_text"


def send_action(action: str):
    try:
        requests.post(f"{API_URL}/bot/control", json={"action": action}, timeout=2)
    except Exception as e:
        print(f"Erro ao enviar ação {action}: {e}")


def update_loop():
    while dpg.is_dearpygui_running():
        try:
            r = requests.get(f"{API_URL}/bot/status", timeout=2)
            if r.ok:
                status = r.json().get("status", "--")
                dpg.set_value(STATUS_TAG, f"Status: {status}")
        except Exception:
            dpg.set_value(STATUS_TAG, "Status: erro")

        try:
            r = requests.get(f"{API_URL}/stats/system", timeout=2)
            if r.ok:
                data = r.json()
                cpu = data.get("cpu_percent", 0)
                mem = data.get("memory_percent", 0)
                dpg.set_value(CPU_TAG, f"CPU: {cpu}%")
                dpg.set_value(RAM_TAG, f"RAM: {mem}%")
        except Exception:
            pass
        time.sleep(2)


# Themes
with dpg.theme() as THEME_DARK:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (45, 45, 48))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 220, 220))

with dpg.theme() as THEME_LIGHT:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (240, 240, 240))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (32, 32, 32))

CURRENT_THEME = THEME_DARK


def toggle_theme():
    global CURRENT_THEME
    CURRENT_THEME = THEME_LIGHT if CURRENT_THEME == THEME_DARK else THEME_DARK
    dpg.bind_theme(CURRENT_THEME)


def run_modern_gui(api_url: str = API_URL):
    global API_URL
    API_URL = api_url

    dpg.create_context()
    dpg.create_viewport(title="Keydrop Bot - Interface Moderna", width=500, height=350)

    with dpg.window(label="Keydrop Bot", width=480, height=320):
        dpg.add_text("Keydrop Bot - Interface Moderna", color=(0, 200, 255))
        with dpg.group(horizontal=True):
            dpg.add_button(label="Iniciar", width=80, callback=lambda: send_action("start"))
            dpg.add_button(label="Parar", width=80, callback=lambda: send_action("stop"))
            dpg.add_button(label="Pausar", width=80, callback=lambda: send_action("pause"))
            dpg.add_button(label="Continuar", width=80, callback=lambda: send_action("resume"))
        dpg.add_button(label="Parada Emergência", callback=lambda: send_action("emergency_stop"))
        dpg.add_separator()
        dpg.add_text("Status: --", tag=STATUS_TAG)
        dpg.add_text("CPU: --", tag=CPU_TAG)
        dpg.add_text("RAM: --", tag=RAM_TAG)
        dpg.add_separator()
        dpg.add_button(label="Alternar Tema", callback=toggle_theme)

    dpg.bind_theme(CURRENT_THEME)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    thread = threading.Thread(target=update_loop, daemon=True)
    thread.start()

    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    run_modern_gui()
