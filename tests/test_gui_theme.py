import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.gui.theming import apply_theme, toggle_theme, load_theme


class TestTheme(unittest.TestCase):
    def test_toggle_theme(self):
        tmp = Path('tmp_theme.json')
        if tmp.exists():
            tmp.unlink()
        apply_theme('Dark')
        toggle_theme(tmp)
        self.assertEqual(load_theme(tmp), 'Light')
        toggle_theme(tmp)
        self.assertEqual(load_theme(tmp), 'Dark')
        tmp.unlink()

if __name__ == '__main__':
    unittest.main()
