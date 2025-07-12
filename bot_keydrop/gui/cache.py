"""Simple in-memory cache for GUI assets."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple
from PIL import Image, ImageTk

FALLBACK_ICON = Path(__file__).resolve().parent.parent / "bot-icone.png"

_cache: Dict[Tuple[str, Tuple[int, int] | None], ImageTk.PhotoImage] = {}


def load_icon(
    path: Path,
    size: Tuple[int, int] | None = None,
    fallback: Path | None = FALLBACK_ICON,
) -> ImageTk.PhotoImage:
    """Load an icon from disk with optional resizing and caching."""
    key = (str(path), size)
    if key not in _cache:
        try:
            img = Image.open(path)
        except Exception:
            if fallback and fallback.exists():
                try:
                    img = Image.open(fallback)
                except Exception:
                    img = Image.new("RGBA", size or (32, 32), (150, 150, 150, 255))
            else:
                img = Image.new("RGBA", size or (32, 32), (150, 150, 150, 255))
        if size:
            img = img.resize(size, Image.LANCZOS)
        _cache[key] = ImageTk.PhotoImage(img)
    return _cache[key]


def clear_cache() -> None:
    """Clear all cached assets."""
    _cache.clear()
