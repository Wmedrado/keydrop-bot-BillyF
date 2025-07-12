import sys
from pathlib import Path

import pytest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.keydrop_bot_desktop_v4 import check_initial_resources, KeydropBotGUI


def test_missing_files_warn(monkeypatch, tmp_path):
    msgs = []
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr('tkinter.messagebox.showwarning', lambda t, m: msgs.append((t, m)))
    check_initial_resources()
    assert msgs, 'warning should be shown when files are missing'


def test_gui_instantiation(monkeypatch):
    dummy = mock.MagicMock()
    monkeypatch.setattr('tkinter.Tk', dummy)
    monkeypatch.setattr('tkinter.StringVar', dummy)
    monkeypatch.setattr('tkinter.BooleanVar', dummy)
    monkeypatch.setattr(KeydropBotGUI, 'start_monitoring', lambda self: None)
    gui = KeydropBotGUI()
    assert dummy.called
