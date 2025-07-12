"""User dashboard frame showing profile info."""
from __future__ import annotations

from typing import Dict, Any
import logging
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from firebase_admin import db
from cloud.firebase_client import initialize_firebase, upload_foto_perfil

logger = logging.getLogger(__name__)


def carregar_dados_usuario(user_id: str) -> Dict[str, Any]:
    initialize_firebase()
    ref = db.reference(f"users/{user_id}")
    return ref.get() or {}


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, user_id: str, **kwargs):
        super().__init__(master, **kwargs)
        self.user_id = user_id
        self.data: Dict[str, Any] = {}
        self.img_container = ctk.CTkLabel(self)
        self._build()
        self.refresh()

    def _build(self) -> None:
        self.columnconfigure(0, weight=1)
        self.name_var = ctk.StringVar()
        self.lucro_var = ctk.StringVar()
        self.tempo_var = ctk.StringVar()
        self.bots_var = ctk.StringVar()

        ctk.CTkLabel(self, textvariable=self.name_var, font=("Arial", 16)).grid(row=0, column=0, pady=4)
        self.img_container.grid(row=1, column=0, pady=4)
        ctk.CTkLabel(self, textvariable=self.lucro_var).grid(row=2, column=0)
        ctk.CTkLabel(self, textvariable=self.tempo_var).grid(row=3, column=0)
        ctk.CTkLabel(self, textvariable=self.bots_var).grid(row=4, column=0)
        ctk.CTkButton(self, text="Atualizar", command=self.refresh).grid(row=5, column=0, pady=10)
        ctk.CTkButton(self, text="Enviar Foto", command=self.upload_photo).grid(row=6, column=0)
        self.pack_propagate(False)

    def refresh(self) -> None:
        try:
            data = carregar_dados_usuario(self.user_id)
        except Exception as e:
            logger.exception("Erro ao carregar dados do usuário")
            messagebox.showerror("Erro", f"Falha ao carregar dados do perfil.\n{e}")
            return
        self.data = data
        self.name_var.set(data.get("nome", "-"))
        self.lucro_var.set(f"Lucro total: R$ {data.get('lucro_total', 0):.2f}")
        self.tempo_var.set(f"Tempo de uso: {data.get('tempo_total_min', 0)} min")
        self.bots_var.set(f"Bots simult\u00e2neos: {data.get('bots_ativos_max', 0)}")
        foto_url = data.get("foto_url")
        if foto_url:
            try:
                from urllib.request import urlopen
                with urlopen(foto_url) as resp:
                    img = Image.open(resp)
                    img = img.resize((80, 80))
                    photo = ImageTk.PhotoImage(img)
                    self.img_container.configure(image=photo)
                    self.img_container.image = photo
            except Exception:
                self.img_container.configure(image=None)

    def upload_photo(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if not path:
            return
        def worker() -> None:
            try:
                url = upload_foto_perfil(self.user_id, path)
                self.after(0, lambda: self._on_upload_success(url))
            except Exception as exc:  # pragma: no cover - network errors
                logger.exception("Falha ao enviar foto de perfil")
                self.after(0, lambda: messagebox.showerror("Erro", f"Falha ao enviar foto.\n{exc}"))

        threading.Thread(target=worker, daemon=True).start()

    def _on_upload_success(self, url: str) -> None:
        messagebox.showinfo("Upload", f"Foto enviada para {url}")
        self.refresh()
