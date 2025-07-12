"""Helper functions for GUI reliability and errors."""
from __future__ import annotations

from tkinter import messagebox
import logging
from pathlib import Path
from typing import Any, Callable, Tuple, Union

import customtkinter as ctk
from PIL import Image, ImageTk


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


def safe_widget_call(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Call a widget function catching exceptions to avoid crashes."""
    try:
        return func(*args, **kwargs)
    except Exception as exc:  # pragma: no cover - Tkinter errors vary
        logging.getLogger(__name__).exception("Widget call failed")
        messagebox.showerror("Erro", f"Falha ao atualizar interface.\n{exc}")
        return None


def safe_load_image(
    source: Union[str, Path],
    size: Tuple[int, int] | None = None,
    placeholder: Path | None = None,
) -> ImageTk.PhotoImage:
    """Load an image from ``source`` returning a placeholder on failure."""
    img = None
    try:
        if str(source).startswith("http"):
            import requests

            with requests.get(source, timeout=60, stream=True) as resp:
                resp.raise_for_status()
                img = Image.open(resp.raw)
        else:
            img = Image.open(source)
    except Exception:
        if placeholder and Path(placeholder).exists():
            try:
                img = Image.open(placeholder)
            except Exception:
                img = None
    if img is None:
        img = Image.new("RGB", size or (32, 32), color=(200, 200, 200))

    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)
