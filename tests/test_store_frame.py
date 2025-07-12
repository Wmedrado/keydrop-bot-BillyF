import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import unittest
from bot_keydrop.gui.store_frame import StoreFrame


class TestStoreFrame(unittest.TestCase):
    def test_frame_creation(self):
        try:
            import customtkinter as ctk

            root = ctk.CTk()
        except Exception:
            self.skipTest("Tk not available")
        frame = StoreFrame(root, user_id="u1")
        self.assertIsNotNone(frame)
        root.destroy()


if __name__ == "__main__":
    unittest.main()
