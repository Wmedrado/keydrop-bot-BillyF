"""Theme utilities for customtkinter interfaces."""
from __future__ import annotations

import json
from pathlib import Path
import customtkinter as ctk

CONFIG_PATH = Path("config.json")
DEFAULT_THEME = "Dark"


def apply_theme(theme: str) -> None:
    """Apply the given theme using customtkinter."""
    if theme not in {"Light", "Dark", "System"}:
        theme = DEFAULT_THEME
    ctk.set_appearance_mode(theme)


def load_theme(path: Path = CONFIG_PATH) -> str:
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            return data.get("theme", DEFAULT_THEME)
        except Exception:
            return DEFAULT_THEME
    return DEFAULT_THEME


def save_theme(theme: str, path: Path = CONFIG_PATH) -> None:
    data = {}
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            data = {}
    data["theme"] = theme
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def apply_saved_theme(path: Path = CONFIG_PATH) -> str:
    theme = load_theme(path)
    apply_theme(theme)
    return theme


def toggle_theme(path: Path = CONFIG_PATH) -> str:
    current = load_theme(path)
    new = "Light" if current == "Dark" else "Dark"
    apply_theme(new)
    save_theme(new, path)
    return new
