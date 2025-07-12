# -*- coding: utf-8 -*-
"""User interface modules for Keydrop Bot.

This file defines Tkinter frames for user login, registration,
profile visualization and global ranking. Firebase is used for
persistence. The interface uses ``customtkinter`` for a modern look.
"""

from __future__ import annotations

import json
import logging
import threading
from pathlib import Path
from typing import Dict, Optional, Any

import customtkinter as ctk
from tkinter import messagebox, filedialog
# Pillow is required for tkhtmlview but direct imports aren't needed here
from tkhtmlview import HTMLLabel
from bot_keydrop.gui.utils import safe_load_image, safe_widget_call

import pyrebase
from firebase_admin import db

from cloud.firebase_client import (
    initialize_firebase,
    salvar_perfil,
    upload_foto_perfil,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Firebase helpers
# ---------------------------------------------------------------------------

_FIREBASE_CONFIG = Path("firebase_config.json")
_SESSION_FILE = Path("user_session.json")
_PLACEHOLDER_IMAGE = Path(__file__).resolve().parent / "bot_keydrop" / "bot-icone.png"


def _load_pyrebase() -> pyrebase.pyrebase.Firebase:
    """Initialize a Pyrebase client using ``firebase_config.json``."""
    if not _FIREBASE_CONFIG.exists():
        raise FileNotFoundError(
            "Firebase configuration not found at firebase_config.json"
        )
    with open(_FIREBASE_CONFIG, "r", encoding="utf-8") as fh:
        config = json.load(fh)
    return pyrebase.initialize_app(config)


def _save_session(user: Dict[str, Any]) -> None:
    data = {
        "idToken": user.get("idToken"),
        "refreshToken": user.get("refreshToken"),
        "localId": user.get("localId"),
    }
    with open(_SESSION_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


def autenticar_usuario(email: str, senha: str) -> Dict[str, Any]:
    """Authenticate the user using Firebase email/password."""
    firebase = _load_pyrebase()
    user = firebase.auth().sign_in_with_email_and_password(email, senha)
    _save_session(user)
    return user


def registrar_usuario(email: str, senha: str) -> Dict[str, Any]:
    """Register a new user and return its auth data."""
    firebase = _load_pyrebase()
    user = firebase.auth().create_user_with_email_and_password(email, senha)
    _save_session(user)
    return user


def carregar_dados_usuario(user_id: str) -> Optional[Dict[str, Any]]:
    """Load a user's profile data from Firebase."""
    initialize_firebase()
    ref = db.reference(f"users/{user_id}")
    return ref.get()


def sincronizar_perfil(
    user_id: str,
    nome: str,
    lucro_total: float,
    tempo_total_min: int,
    bots_ativos_max: int,
) -> None:
    """Persist user profile and ranking information."""
    salvar_perfil(user_id, nome, lucro_total, tempo_total_min, bots_ativos_max)


# ---------------------------------------------------------------------------
# Tkinter frames
# ---------------------------------------------------------------------------

class LoginFrame(ctk.CTkFrame):
    """Tela de login com campos de email e senha."""

    def __init__(self, master: ctk.CTk, on_login, on_register, **kwargs):
        super().__init__(master, **kwargs)
        self.on_login = on_login
        self.on_register = on_register
        self.email_var = ctk.StringVar()
        self.senha_var = ctk.StringVar()
        self._build()

    def _build(self) -> None:
        ctk.CTkLabel(self, text="Email:").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.email_var).pack(pady=5)

        ctk.CTkLabel(self, text="Senha:").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.senha_var, show="*").pack(pady=5)

        ctk.CTkButton(self, text="Entrar", command=self._handle_login).pack(pady=10)
        ctk.CTkButton(self, text="Cadastrar", command=self.on_register).pack()

    def _handle_login(self) -> None:
        email = self.email_var.get().strip()
        senha = self.senha_var.get().strip()
        if not email or not senha:
            messagebox.showerror("Erro", "Informe email e senha")
            return
        try:
            user = autenticar_usuario(email, senha)
            self.on_login(user)
        except Exception as exc:  # pragma: no cover - network errors
            messagebox.showerror("Falha no login", str(exc))


class RegisterFrame(ctk.CTkFrame):
    """Tela de cadastro de novo usuário."""

    def __init__(self, master: ctk.CTk, on_register_success, **kwargs):
        super().__init__(master, **kwargs)
        self.on_register_success = on_register_success
        self.email_var = ctk.StringVar()
        self.pass_var = ctk.StringVar()
        self.confirm_var = ctk.StringVar()
        self._build()

    def _build(self) -> None:
        ctk.CTkLabel(self, text="Cadastro").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.email_var, placeholder_text="Email").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.pass_var, placeholder_text="Senha", show="*").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.confirm_var, placeholder_text="Confirmar Senha", show="*").pack(pady=5)
        ctk.CTkButton(self, text="Registrar", command=self._do_register).pack(pady=10)

    def _do_register(self) -> None:
        email = self.email_var.get().strip()
        senha = self.pass_var.get().strip()
        confirm = self.confirm_var.get().strip()
        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos")
            return
        if senha != confirm:
            messagebox.showerror("Erro", "Senhas não conferem")
            return
        try:
            user = registrar_usuario(email, senha)
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso")
            self.on_register_success(user)
        except Exception as exc:  # pragma: no cover - network errors
            messagebox.showerror("Falha", str(exc))


class ProfileFrame(ctk.CTkFrame):
    """Exibição do perfil do usuário autenticado."""

    def __init__(self, master: ctk.CTk, user_id: str, **kwargs):
        super().__init__(master, **kwargs)
        self.user_id = user_id
        self.data: Dict[str, Any] = {}
        self.img_container = ctk.CTkLabel(self)
        self._build()
        self.refresh()

    def _build(self) -> None:
        self.name_var = ctk.StringVar()
        self.lucro_var = ctk.StringVar()
        self.tempo_var = ctk.StringVar()
        self.bots_var = ctk.StringVar()

        ctk.CTkLabel(self, textvariable=self.name_var, font=("Arial", 16)).pack(pady=4)
        self.img_container.pack(pady=4)
        ctk.CTkLabel(self, textvariable=self.lucro_var).pack()
        ctk.CTkLabel(self, textvariable=self.tempo_var).pack()
        ctk.CTkLabel(self, textvariable=self.bots_var).pack()
        ctk.CTkButton(self, text="Atualizar", command=self.refresh).pack(pady=10)
        ctk.CTkButton(self, text="Enviar Foto", command=self.upload_photo).pack()

    def refresh(self) -> None:
        try:
            data = carregar_dados_usuario(self.user_id) or {}
        except Exception as e:
            logger.exception("Erro ao carregar dados do usuário")
            messagebox.showerror("Erro", f"Falha ao carregar dados do perfil.\n{e}")
            return
        self.data = data
        self.name_var.set(data.get("nome", "-"))
        self.lucro_var.set(f"Lucro total: R$ {data.get('lucro_total', 0):.2f}")
        self.tempo_var.set(f"Tempo de uso: {data.get('tempo_total_min', 0)} min")
        self.bots_var.set(f"Bots simultâneos: {data.get('bots_ativos_max', 0)}")
        foto_url = data.get("foto_url")
        photo = safe_load_image(
            foto_url or _PLACEHOLDER_IMAGE,
            size=(80, 80),
            placeholder=_PLACEHOLDER_IMAGE,
        )
        safe_widget_call(self.img_container.configure, image=photo)
        self.img_container.image = photo

    def upload_photo(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if not path:
            return
        def worker() -> None:
            try:
                url = upload_foto_perfil(self.user_id, path)
                self.img_container.after(0, lambda: self._on_upload_success(url))
            except Exception as exc:  # pragma: no cover - network errors
                logger.exception("Falha ao enviar foto de perfil")
                self.img_container.after(
                    0,
                    lambda exc=exc: messagebox.showerror(
                        "Erro", f"Falha ao enviar foto.\n{exc}"
                    ),
                )

        threading.Thread(target=worker, daemon=True).start()

    def _on_upload_success(self, url: str) -> None:
        messagebox.showinfo("Upload", f"Foto enviada para {url}")
        self.refresh()


class RankingFrame(ctk.CTkFrame):
    """Lista dos usuários com maior lucro."""

    def __init__(self, master: ctk.CTk, **kwargs):
        super().__init__(master, **kwargs)
        self.html_label = HTMLLabel(self, html="")
        self.html_label.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self) -> None:
        try:
            initialize_firebase()
            ref = db.reference("rankings/top_lucro")
            ranking = ref.order_by_value().limit_to_last(10).get() or {}
        except Exception as e:
            logger.exception("Erro ao obter ranking do Firebase")
            messagebox.showerror("Erro", f"Falha ao carregar ranking.\n{e}")
            return
        sorted_items = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
        html = ["<h3>Ranking Global</h3><ol>"]
        for idx, (uid, lucro) in enumerate(sorted_items, start=1):
            medal = "🥇" if idx == 1 else ("🥈" if idx == 2 else ("🥉" if idx == 3 else ""))
            highlight = "🔥" if idx == 1 else ("💰" if lucro > 500 else "")
            html.append(f"<li>{medal} {uid} - R$ {lucro:.2f} {highlight}</li>")
        html.append("</ol>")
        safe_widget_call(self.html_label.set_html, "".join(html))
