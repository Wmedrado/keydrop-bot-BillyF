from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Iterable, Union


def validar_permissoes(pastas: Iterable[Union[str, PathLike]]) -> bool:
    """Check if the given folders are writable.

    Args:
        pastas: Iterable of paths or strings representing directories.

    Returns:
        ``True`` if all directories can be created and written to, ``False`` otherwise.
    """

    if pastas is None:
        raise ValueError("Lista de pastas não pode ser None")

    for pasta in pastas:
        p = Path(pasta)
        try:
            p.mkdir(parents=True, exist_ok=True)
            test_file = p / ".perm_test"
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("test")
            test_file.unlink()
        except Exception:
            return False
    return True
