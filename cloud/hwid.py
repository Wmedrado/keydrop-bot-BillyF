import hashlib
import uuid
from typing import Optional

from . import permissions

import psutil


def generate_hwid() -> str:
    """Generate a machine-specific hardware ID."""
    cpu = uuid.getnode()
    disk = psutil.disk_partitions()[0].device
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    raw = f"{cpu}-{disk}-{mac}".encode()
    return hashlib.sha256(raw).hexdigest()


def validate_hwid(current: str, stored: Optional[str]) -> bool:
    """Return ``True`` if stored ID matches current."""
    return stored is None or stored == current


def validate_user_hwid(user_id: str) -> bool:
    """Compare current HWID with the one stored in Firebase."""
    stored = permissions.fetch_hwid(user_id)
    current = generate_hwid()
    if stored is None:
        permissions.save_hwid(user_id, current)
        return True
    return validate_hwid(current, stored)
