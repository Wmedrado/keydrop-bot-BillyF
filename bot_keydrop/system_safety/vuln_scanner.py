from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import List


def scan_requirements(req_file: Path) -> List[str]:
    """Return list of vulnerable packages using pip-audit if available."""
    try:
        result = subprocess.run(
            ["pip-audit", "-r", str(req_file), "--format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return []
    if result.returncode != 0:
        return []
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []
    vulns = {d["name"] for d in data}
    return sorted(vulns)
