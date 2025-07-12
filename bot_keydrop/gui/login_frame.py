"""Login frame component."""
from __future__ import annotations

import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Progressbar

from log_utils import setup_logger

logger = setup_logger("login_frame")

from .utils import exibir_erro


class LoginFrame(ctk.CTkFrame):
    """Simple login form."""

    def __init__(self, master: ctk.CTk, on_login, on_register, **kwargs):
        super().__init__(master, **kwargs)
        self.on_login = on_login
        self.on_register = on_register
        self.email_var = ctk.StringVar()
        self.senha_var = ctk.StringVar()
        self.progress = None
        self._build()

    def _build(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self, text="Email:", font=("Arial", 14)).grid(row=0, column=0, pady=5, sticky="ew")
        ctk.CTkEntry(self, textvariable=self.email_var).grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        ctk.CTkLabel(self, text="Senha:", font=("Arial", 14)).grid(row=2, column=0, pady=5, sticky="ew")
        ctk.CTkEntry(self, textvariable=self.senha_var, show="*").grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        btn = ctk.CTkButton(self, text="Entrar", command=self._handle_login)
        btn.grid(row=4, column=0, pady=10)
        self.login_button = btn

        ctk.CTkButton(self, text="Cadastrar", command=self.on_register).grid(row=5, column=0)
        self.pack_propagate(False)

    def _simulate_loading(self) -> None:
        if not self.progress:
            self.progress = Progressbar(self, mode="indeterminate")
            self.progress.grid(row=6, column=0, pady=5, sticky="ew", padx=20)
        self.progress.start(10)
        self.after(1500, self.progress.stop)

    def _handle_login(self) -> None:
        email = self.email_var.get().strip()
        senha = self.senha_var.get().strip()
        if not email or not senha:
            exibir_erro("Informe email e senha")
            return
        logger.info("Tentativa de login para %s", email)
        self.login_button.configure(state="disabled")
        self._simulate_loading()
        self.after(3000, lambda: self.login_button.configure(state="normal"))
        try:
            self.on_login(email, senha)
            logger.info("Login realizado com sucesso para %s", email)
        except Exception as exc:  # pragma: no cover
            logger.exception("Erro no login de %s", email)
            messagebox.showerror("Falha no login", str(exc))
