"""Helper functions for GUI reliability and errors."""
from __future__ import annotations

from tkinter import messagebox
import customtkinter as ctk


def exibir_erro(mensagem: str) -> None:
    """Show an error message dialog."""
    messagebox.showerror("Erro Cr\u00edtico", mensagem)


def verificar_gui_integridade(widget: ctk.CTkBaseClass) -> bool:
    """Return ``True`` if the widget and all descendants exist."""
    if not widget.winfo_exists():
        return False
    for child in widget.winfo_children():
        if not verificar_gui_integridade(child):
            return False
    return True
