from __future__ import annotations

import hashlib
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("critical_hashes.json")


def compute_hash(path: Path) -> str:
    """Return SHA256 of *path*."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_hashes() -> bool:
    """Check critical file hashes against the stored values."""
    if not DATA_FILE.exists():
        return True
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    ok = True
    for rel, expected in data.items():
        path = Path(rel)
        if not path.exists():
            print(f"Missing {path}")
            ok = False
            continue
        if compute_hash(path) != expected:
            print(f"Hash mismatch for {path}")
            ok = False
    return ok
