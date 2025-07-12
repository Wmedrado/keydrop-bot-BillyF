"""Premium permission helpers relying on Firebase."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict

from cloud.permissions import fetch_permissions, update_permissions

PREMIUM_PRODUCTS = {
    "telegram_month": {"permission": "telegram_access", "duration_days": 30},
    "premium_month": {"permission": "premium_access", "duration_days": 30},
    "premium_year": {"permission": "premium_access", "duration_days": 365},
    "frame_gold": {"item": "frame_gold"},
    "frame_shadow": {"item": "frame_shadow"},
    "frame_animated": {"item": "frame_animated"},
}


def purchase_product(user_id: str, product_id: str) -> None:
    """Update permission data for the purchased product."""
    if product_id not in PREMIUM_PRODUCTS:
        raise ValueError("Produto inválido")
    prod = PREMIUM_PRODUCTS[product_id]
    perms = fetch_permissions(user_id)
    items = set(perms.get("items_owned", []))
    updates: Dict[str, object] = {}
    if "duration_days" in prod:
        exp = datetime.now(timezone.utc) + timedelta(days=prod["duration_days"])
        updates["expiration_date"] = exp.isoformat()
        updates[prod["permission"]] = True
    if "item" in prod:
        items.add(prod["item"])
        updates["items_owned"] = list(items)
    update_permissions(user_id, updates)


def check_premium_validity(user_id: str) -> Dict:
    """Return the latest permissions after validating expiration."""
    perms = fetch_permissions(user_id)
    exp = perms.get("expiration_date")
    if exp:
        exp_dt = datetime.fromisoformat(exp.replace("Z", "+00:00")).astimezone(timezone.utc)
        if datetime.now(timezone.utc) > exp_dt:
            perms.pop("premium_access", None)
            perms.pop("telegram_access", None)
            perms["expiration_date"] = None
            update_permissions(user_id, perms)
    return perms


def has_permission(user_id: str, permission: str) -> bool:
    """Check if user currently has the given permission."""
    perms = check_premium_validity(user_id)
    return bool(perms.get(permission))
