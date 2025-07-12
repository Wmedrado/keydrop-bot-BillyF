import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
import logging

from . import builder


class TextHandler(logging.Handler):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        msg = self.format(record)
        self.widget.after(0, lambda: (self.widget.insert(tk.END, msg + "\n"), self.widget.see(tk.END)))

def start_build(mode, arch, text):
    def _run():
        cfg = builder.load_config()
        version = builder.get_version(cfg)
        builder.perform_build(cfg, version, debug=(mode=='debug'), arch=arch)
    threading.Thread(target=_run, daemon=True).start()


def main():
    root = tk.Tk()
    root.title("Gerador de Executável")

    frm = ttk.Frame(root, padding=10)
    frm.pack(fill="both", expand=True)

    mode_var = tk.StringVar(value="release")
    ttk.Label(frm, text="Modo:").grid(column=0, row=0, sticky="w")
    ttk.Radiobutton(frm, text="Produção", variable=mode_var, value="release").grid(column=1, row=0, sticky="w")
    ttk.Radiobutton(frm, text="Debug", variable=mode_var, value="debug").grid(column=2, row=0, sticky="w")

    arch_var = tk.StringVar(value="x64")
    ttk.Label(frm, text="Arquitetura:").grid(column=0, row=1, sticky="w")
    for i, arch in enumerate(["x86", "x64", "both"]):
        ttk.Radiobutton(frm, text=arch, variable=arch_var, value=arch).grid(column=1+i, row=1, sticky="w")

    log_box = scrolledtext.ScrolledText(frm, width=80, height=20)
    log_box.grid(column=0, row=2, columnspan=4, pady=10)

    handler = TextHandler(log_box)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logging.getLogger('builder').addHandler(handler)

    def on_generate():
        text = log_box
        text.delete("1.0", tk.END)
        arch = arch_var.get()
        if arch == 'both':
            for a in ('x86', 'x64'):
                start_build(mode_var.get(), a, text)
        else:
            start_build(mode_var.get(), arch, text)

    ttk.Button(frm, text="Gerar", command=on_generate).grid(column=0, row=3, pady=5, sticky="w")

    root.mainloop()


if __name__ == "__main__":
    import logging
    main()

