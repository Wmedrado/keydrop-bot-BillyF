import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import user_interface

class TestProfileFrame(unittest.TestCase):
    def test_refresh_placeholder_image(self):
        try:
            import customtkinter as ctk
            root = ctk.CTk()
        except Exception:
            self.skipTest('Tk not available')
        user_interface.carregar_dados_usuario = lambda uid: {"foto_url": "http://bad.url/img.png"}
        import urllib.request
        def fail(_):
            raise Exception('fail')
        mp = __import__('pytest').MonkeyPatch()
        mp.setattr(urllib.request, 'urlopen', fail)
        try:
            frame = user_interface.ProfileFrame(root, user_id='x')
            self.assertIsNotNone(frame.img_container.image)
        finally:
            root.destroy()
            mp.undo()

if __name__ == '__main__':
    unittest.main()
