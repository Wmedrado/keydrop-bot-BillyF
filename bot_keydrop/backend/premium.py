"""Premium product management for Keydrop Bot."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

DATA_FILE = Path(__file__).resolve().parent / "premium_data.json"

PREMIUM_PRODUCTS = {
    "telegram_month": {
        "price": 10.0,
        "permission": "telegram_access",
        "duration_days": 30,
    },
    "premium_month": {
        "price": 49.99,
        "permission": "premium_access",
        "duration_days": 30,
    },
    "premium_year": {
        "price": 539.90,
        "permission": "premium_access",
        "duration_days": 365,
    },
    "frame_gold": {"price": 4.99, "item": "frame_gold"},
    "frame_shadow": {"price": 9.99, "item": "frame_shadow"},
    "frame_animated": {"price": 14.99, "item": "frame_animated"},
}


def _load_data() -> Dict:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {"users": {}}


def _save_data(data: Dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def purchase_product(user_id: str, product_id: str) -> None:
    """Register a product purchase for a user."""
    if product_id not in PREMIUM_PRODUCTS:
        raise ValueError("Produto inválido")
    data = _load_data()
    user = data.setdefault("users", {}).setdefault(user_id, {
        "permissions": {},
        "items_owned": [],
        "expiration_date": None,
    })
    prod = PREMIUM_PRODUCTS[product_id]
    if "duration_days" in prod:
        user["expiration_date"] = (
            datetime.utcnow() + timedelta(days=prod["duration_days"])
        ).strftime("%Y-%m-%d")
        user["permissions"][prod["permission"]] = True
    elif "item" in prod:
        if prod["item"] not in user["items_owned"]:
            user["items_owned"].append(prod["item"])
    _save_data(data)


def check_premium_validity(user_id: str) -> Dict:
    """Return current permissions after validating expiration."""
    data = _load_data()
    user = data.setdefault("users", {}).get(user_id, {})
    perm = user.get("permissions", {})
    exp = user.get("expiration_date")
    if exp:
        exp_date = datetime.strptime(exp, "%Y-%m-%d")
        if datetime.utcnow() > exp_date:
            perm = {}
            user["permissions"] = perm
            user["expiration_date"] = None
            _save_data(data)
    return perm


def has_permission(user_id: str, permission: str) -> bool:
    perms = check_premium_validity(user_id)
    return perms.get(permission, False)
