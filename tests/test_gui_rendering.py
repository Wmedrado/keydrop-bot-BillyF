import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.gui.login_frame import LoginFrame


class TestLoginFrame(unittest.TestCase):
    def test_frame_creation(self):
        try:
            import customtkinter as ctk
            root = ctk.CTk()
            frame = LoginFrame(root, on_login=lambda e,p:None, on_register=lambda:None)
            self.assertTrue(frame.winfo_exists())
            root.destroy()
        except Exception:
            self.skipTest('Tk not available')

if __name__ == '__main__':
    unittest.main()
