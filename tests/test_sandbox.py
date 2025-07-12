import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from bot_keydrop.system_safety import run_in_sandbox  # noqa: E402


def echo(x):
    return x


def test_run_in_sandbox():
    result = run_in_sandbox(echo, 5)
    assert result == 5
