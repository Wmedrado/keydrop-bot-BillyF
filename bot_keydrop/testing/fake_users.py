from __future__ import annotations

import random
from typing import List, Dict, Any


def generate_fake_users(count: int) -> List[Dict[str, Any]]:
    """Return a list of fake user dictionaries for testing."""
    users = []
    for i in range(count):
        users.append({
            "id": i,
            "username": f"user_{i}",
            "balance": random.randint(0, 1000),
            "bot": bool(random.getrandbits(1)),
        })
    return users
