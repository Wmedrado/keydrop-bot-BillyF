import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from startup import criar_driver, clicar_sorteio
import os
import sys

class BotManager:
    def __init__(self, num_browsers, wait_between, wait_tab, base_path):
        self.num_browsers = num_browsers
        self.wait_between = wait_between
        self.wait_tab = wait_tab
        self.base_path = base_path
        self.threads = []
        self.drivers = []
        self.running = False

    def start(self, status_callback):
        self.running = True
        self.drivers = []
        for i in range(self.num_browsers):
            perfil_dir = os.path.join(self.base_path, f"Profile-{i+1}")
            if not os.path.exists(perfil_dir):
                os.makedirs(perfil_dir)
            driver = criar_driver(perfil_dir)
            self.drivers.append(driver)
            driver.get("https://key-drop.com/pt/giveaways/list")
            status_callback(i, "Aguardando login...")
            time.sleep(2)
        messagebox.showinfo("Login", "Faça login em cada janela e clique em OK para iniciar o bot.")
        for idx, driver in enumerate(self.drivers):
            t = threading.Thread(target=self.bot_loop, args=(driver, idx, status_callback), daemon=True)
            t.start()
            self.threads.append(t)

    def bot_loop(self, driver, idx, status_callback):
        while self.running:
            try:
                status_callback(idx, "Entrando no sorteio...")
                clicar_sorteio(driver)
                status_callback(idx, f"Aguardando {self.wait_between}s...")
                for _ in range(self.wait_between):
                    if not self.running:
                        break
                    time.sleep(1)
            except Exception as e:
                status_callback(idx, f"Erro: {e}")
                time.sleep(10)

    def stop(self):
        self.running = False
        for driver in self.drivers:
            try:
                driver.quit()
            except:
                pass
        self.drivers = []
        self.threads = []

class BotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KeyDrop Bot - Configuração")
        self.root.geometry("500x400")
        self.root.configure(bg="#23272A")
        self.root.resizable(False, False)
        
        # Ícone personalizado (se existir)
        self.configurar_icone()
        
        self.manager = None
        self.status_labels = []
        self.build_gui()

    def build_gui(self):
        frame = tk.Frame(self.root, bg="#23272A", padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Quantidade de janelas:", bg="#23272A", fg="white").pack(anchor="w")
        self.num_browsers = tk.IntVar(value=2)
        tk.Spinbox(frame, from_=1, to=10, textvariable=self.num_browsers, width=5).pack(anchor="w")

        tk.Label(frame, text="Tempo entre sorteios (s):", bg="#23272A", fg="white").pack(anchor="w", pady=(10,0))
        self.wait_between = tk.IntVar(value=180)
        tk.Entry(frame, textvariable=self.wait_between, width=10).pack(anchor="w")

        tk.Label(frame, text="Tempo para trocar de guia (s):", bg="#23272A", fg="white").pack(anchor="w", pady=(10,0))
        self.wait_tab = tk.IntVar(value=2)
        tk.Entry(frame, textvariable=self.wait_tab, width=10).pack(anchor="w")

        tk.Label(frame, text="Pasta base dos perfis:", bg="#23272A", fg="white").pack(anchor="w", pady=(10,0))
        self.base_path = tk.StringVar(value=os.path.join(os.getcwd(), "data"))
        tk.Entry(frame, textvariable=self.base_path, width=40).pack(anchor="w")

        self.start_btn = tk.Button(frame, text="Iniciar Bot", command=self.start_bot, bg="#43B581", fg="white", width=20)
        self.start_btn.pack(pady=20)
        self.stop_btn = tk.Button(frame, text="Parar Bot", command=self.stop_bot, bg="#F04747", fg="white", width=20, state="disabled")
        self.stop_btn.pack()

        self.status_frame = tk.Frame(self.root, bg="#23272A")
        self.status_frame.pack(fill="x", pady=10)

    def update_status(self, idx, msg):
        if idx >= len(self.status_labels):
            lbl = tk.Label(self.status_frame, text=f"Janela {idx+1}: {msg}", bg="#23272A", fg="white")
            lbl.pack(anchor="w")
            self.status_labels.append(lbl)
        else:
            self.status_labels[idx].config(text=f"Janela {idx+1}: {msg}")

    def start_bot(self):
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        for lbl in self.status_labels:
            lbl.destroy()
        self.status_labels = []
        self.manager = BotManager(
            self.num_browsers.get(),
            self.wait_between.get(),
            self.wait_tab.get(),
            self.base_path.get()
        )
        threading.Thread(target=self.manager.start, args=(self.update_status,), daemon=True).start()

    def stop_bot(self):
        if self.manager:
            self.manager.stop()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        for idx in range(len(self.status_labels)):
            self.update_status(idx, "Parado.")

    def configurar_icone(self):
        """Configura o ícone da janela de forma robusta para executáveis"""
        try:
            # Lista de possíveis localizações do ícone
            possiveis_caminhos = [
                # Mesmo diretório do script/executável
                os.path.join(os.path.dirname(__file__), 'bot-icone.ico'),
                os.path.join(os.path.dirname(__file__), 'bot-icone.png'),
                
                # Diretório atual
                os.path.join(os.getcwd(), 'bot-icone.ico'),
                os.path.join(os.getcwd(), 'bot-icone.png'),
                
                # Diretório pai (caso esteja em startup/)
                os.path.join(os.path.dirname(__file__), '..', 'bot-icone.ico'),
                os.path.join(os.path.dirname(__file__), '..', 'bot-icone.png'),
                
                # Para executáveis PyInstaller
                os.path.join(sys._MEIPASS if hasattr(sys, '_MEIPASS') else '.', 'bot-icone.ico'),
                os.path.join(sys._MEIPASS if hasattr(sys, '_MEIPASS') else '.', 'bot-icone.png'),
            ]
            
            # Tentar carregar o ícone de cada localização
            for caminho in possiveis_caminhos:
                if os.path.exists(caminho):
                    try:
                        if caminho.endswith('.ico'):
                            self.root.iconbitmap(caminho)
                            print(f"✅ Ícone ICO carregado de: {caminho}")
                            return
                        elif caminho.endswith('.png'):
                            icon_image = tk.PhotoImage(file=caminho)
                            self.root.iconphoto(True, icon_image)
                            print(f"✅ Ícone PNG carregado de: {caminho}")
                            return
                    except Exception as e:
                        print(f"⚠️ Erro ao carregar ícone de {caminho}: {e}")
                        continue
            
            print("⚠️ Nenhum ícone encontrado, usando ícone padrão")
            
        except Exception as e:
            print(f"❌ Erro na configuração do ícone: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    BotGUI().run()
