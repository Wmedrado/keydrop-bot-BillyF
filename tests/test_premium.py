import json
import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.backend import premium


class TestPremiumSystem(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data_file = Path(self.tmp.name) / "data.json"
        premium.DATA_FILE = self.data_file

    def tearDown(self):
        self.tmp.cleanup()

    def test_purchase_and_expiration(self):
        premium.purchase_product("u1", "premium_month")
        data = json.loads(self.data_file.read_text())
        self.assertIn("u1", data["users"]) 

        # permissions should be valid immediately
        self.assertTrue(premium.has_permission("u1", "premium_access"))

        # expire by setting old date
        data["users"]["u1"]["expiration_date"] = "2000-01-01"
        self.data_file.write_text(json.dumps(data))
        perms = premium.check_premium_validity("u1")
        self.assertFalse(perms)
        self.assertFalse(premium.has_permission("u1", "premium_access"))

    def test_purchase_frame(self):
        premium.purchase_product("u2", "frame_gold")
        data = json.loads(self.data_file.read_text())
        self.assertIn("frame_gold", data["users"]["u2"]["items_owned"])


if __name__ == "__main__":
    unittest.main()
