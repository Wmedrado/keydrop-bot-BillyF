from __future__ import annotations

import re
from typing import List


INVALID = re.compile(r"[;&|`$<>]")


def sanitize_cli_args(args: List[str]) -> List[str]:
    """Raise ValueError if *args* contain potentially dangerous characters."""
    for arg in args:
        if INVALID.search(arg):
            raise ValueError(f"Invalid argument: {arg}")
    return args
