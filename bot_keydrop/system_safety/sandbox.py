import multiprocessing
from typing import Any, Callable


def _runner(
    queue: multiprocessing.Queue, func: Callable[..., Any], *args, **kwargs
) -> None:
    try:
        queue.put(("result", func(*args, **kwargs)))
    except Exception as exc:  # pragma: no cover - runtime errors
        queue.put(("error", str(exc)))


def run_in_sandbox(
    func: Callable[..., Any], *args, timeout: float = 30.0, **kwargs
) -> Any:
    """Execute ``func`` in a separate process with a timeout."""
    queue: multiprocessing.Queue = multiprocessing.Queue()
    proc = multiprocessing.Process(
        target=_runner, args=(queue, func, *args), kwargs=kwargs
    )
    proc.start()
    proc.join(timeout)
    if proc.is_alive():
        proc.terminate()
        raise TimeoutError("Sandboxed process timed out")
    if queue.empty():
        raise RuntimeError("Sandboxed process returned no result")
    status, value = queue.get()
    if status == "error":
        raise RuntimeError(value)
    return value
