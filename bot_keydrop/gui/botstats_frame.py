"""Display system stats like CPU and RAM usage."""
from __future__ import annotations

import customtkinter as ctk
from tkinter import ttk
import psutil


class BotStatsFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, **kwargs):
        super().__init__(master, **kwargs)
        self.cpu_var = ctk.StringVar(value="CPU: 0%")
        self.ram_var = ctk.StringVar(value="RAM: 0%")
        self.progress = ttk.Progressbar(self, mode="determinate")
        self._build()
        self.update_stats()

    def _build(self) -> None:
        ctk.CTkLabel(self, textvariable=self.cpu_var).pack(pady=2)
        ctk.CTkLabel(self, textvariable=self.ram_var).pack(pady=2)
        self.progress.pack(fill="x", padx=10, pady=5)
        self.pack_propagate(False)

    def update_stats(self) -> None:
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        self.cpu_var.set(f"CPU: {cpu}%")
        self.ram_var.set(f"RAM: {mem}%")
        self.progress.configure(value=cpu)
        self.after(2000, self.update_stats)
