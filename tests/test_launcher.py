import importlib
import sys
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_launcher_importable():
    dummy = mock.MagicMock()
    with mock.patch.multiple("tkinter", Tk=dummy, StringVar=dummy), \
         mock.patch.multiple("tkinter.ttk", Label=dummy, Button=dummy):
        module = importlib.import_module("launcher")
    assert hasattr(module, "run_gui")
    assert hasattr(module, "run_api")
