import logging
from datetime import datetime, timezone
from typing import Any, Dict

try:
    from firebase_admin import db
except Exception:  # pragma: no cover - optional dependency
    db = None  # type: ignore

from .firebase_client import initialize_firebase

logger = logging.getLogger(__name__)


def fetch_permissions(user_id: str) -> Dict[str, Any]:
    """Return permission data for the given user from Firebase."""
    if db is None:
        raise ImportError("firebase_admin is required for Firebase operations")

    initialize_firebase()
    ref = db.reference(f"permissions/{user_id}")
    return ref.get() or {}


def update_permissions(user_id: str, data: Dict[str, Any]) -> None:
    """Update permission data for a user on Firebase."""
    if db is None:
        raise ImportError("firebase_admin is required for Firebase operations")

    initialize_firebase()
    ref = db.reference(f"permissions/{user_id}")
    ref.update(data)


def _parse_date(date_str: str) -> datetime:
    return datetime.fromisoformat(date_str.replace("Z", "+00:00")).astimezone(timezone.utc)


def subscription_active(perms: Dict[str, Any]) -> bool:
    """Check if the permissions contain a valid, non expired subscription."""
    exp = perms.get("expiration_date")
    if not exp:
        return False
    try:
        return _parse_date(exp) > datetime.now(timezone.utc)
    except Exception:  # pragma: no cover - invalid format
        logger.error("Invalid expiration_date format: %s", exp)
        return False


def has_premium_access(perms: Dict[str, Any]) -> bool:
    """Return ``True`` if premium features are enabled."""
    return bool(perms.get("premium_access") and subscription_active(perms))


def has_telegram_access(perms: Dict[str, Any]) -> bool:
    """Return ``True`` if Telegram access is allowed."""
    return bool(perms.get("telegram_access") and subscription_active(perms))
