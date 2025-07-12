from typing import Optional


def safe_int(value: str, default: Optional[int] = None) -> Optional[int]:
    """Safely convert a string to int.

    Returns ``default`` if conversion fails.
    """
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def safe_float(value: str, default: Optional[float] = None) -> Optional[float]:
    """Safely convert a string to float.

    Returns ``default`` if conversion fails.
    """
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def sanitize_str(value: str) -> str:
    """Return a sanitized string without surrounding whitespace."""
    return str(value).strip() if value is not None else ""
