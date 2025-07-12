import concurrent.futures
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def dummy_bot(_):
    # Simulate lightweight bot work
    time.sleep(0.01)
    return True


def test_stress_multiple_bots():
    bots = 50
    with concurrent.futures.ThreadPoolExecutor(max_workers=bots) as exc:
        results = list(exc.map(dummy_bot, range(bots)))
    assert results.count(True) == bots
