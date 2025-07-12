import sys
from typing import Dict
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.backend import premium


class MemoryStore:
    def __init__(self):
        self.data: Dict[str, Dict[str, object]] = {}

    def fetch(self, uid: str) -> Dict[str, object]:
        return self.data.get(uid, {}).copy()

    def update(self, uid: str, updates: Dict[str, object]) -> None:
        self.data.setdefault(uid, {})
        self.data[uid] = updates


class TestPremiumSystem(unittest.TestCase):
    def setUp(self):
        self.store = MemoryStore()
        self.patch_fetch = mock.patch("bot_keydrop.backend.premium.fetch_permissions", self.store.fetch)
        self.patch_update = mock.patch("bot_keydrop.backend.premium.update_permissions", self.store.update)
        self.patch_fetch_perm = mock.patch("cloud.permissions.fetch_permissions", self.store.fetch)
        self.patch_update_perm = mock.patch("cloud.permissions.update_permissions", self.store.update)
        self.patch_fetch_perm.start()
        self.patch_update_perm.start()
        self.patch_init = mock.patch("cloud.permissions.initialize_firebase", lambda: None)
        self.patch_fetch.start()
        self.patch_update.start()
        self.patch_init.start()

    def tearDown(self):
        self.patch_fetch.stop()
        self.patch_update.stop()
        self.patch_fetch_perm.stop()
        self.patch_update_perm.stop()
        self.patch_init.stop()

    def test_purchase_and_expiration(self):
        premium.purchase_product("u1", "premium_month")
        data = self.store.data
        self.assertIn("u1", data)

        # permissions should be valid immediately
        self.assertTrue(premium.has_permission("u1", "premium_access"))

        # expire by setting old date
        self.store.update("u1", {"expiration_date": "2000-01-01"})
        perms = premium.check_premium_validity("u1")
        self.assertNotIn("premium_access", perms)
        self.assertFalse(premium.has_permission("u1", "premium_access"))

    def test_purchase_frame(self):
        premium.purchase_product("u2", "frame_neon")
        self.assertIn("frame_neon", self.store.data["u2"]["items_owned"])


if __name__ == "__main__":
    unittest.main()
