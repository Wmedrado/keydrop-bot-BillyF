import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.gui.utils import verificar_gui_integridade


class FakeWidget:
    def __init__(self, children=None, exists=True):
        self._children = children or []
        self._exists = exists

    def winfo_exists(self):
        return self._exists

    def winfo_children(self):
        return self._children


class TestGuiIntegrity(unittest.TestCase):
    def test_integridade_valida(self):
        child = FakeWidget()
        root = FakeWidget([child])
        self.assertTrue(verificar_gui_integridade(root))

    def test_integridade_invalida(self):
        bad = FakeWidget(exists=False)
        root = FakeWidget([bad])
        self.assertFalse(verificar_gui_integridade(root))


if __name__ == "__main__":
    unittest.main()
