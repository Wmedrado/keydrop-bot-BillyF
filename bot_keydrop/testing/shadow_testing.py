from typing import Callable, Iterable, Any


def run_shadow_test(current: Callable[[Any], Any], new: Callable[[Any], Any], data: Iterable[Any]) -> bool:
    """Run two callables with the same input data and compare outputs."""
    results_current = [current(d) for d in data]
    results_new = [new(d) for d in data]
    return results_current == results_new


if __name__ == "__main__":
    import json
    import sys
    dataset = json.loads(sys.stdin.read())
    same = run_shadow_test(lambda x: x, lambda x: x, dataset)
    print("match" if same else "mismatch")
