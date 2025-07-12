import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from bot_keydrop.system_safety import enforce_timeout, TimeoutException  # noqa: E402


@enforce_timeout(0.5)
def slow_function():
    time.sleep(1)


def test_enforce_timeout():
    start = time.time()
    try:
        slow_function()
    except TimeoutException:
        elapsed = time.time() - start
        assert elapsed < 1.5
    else:
        raise AssertionError("Timeout not triggered")
