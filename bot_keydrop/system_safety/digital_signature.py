from __future__ import annotations

import hmac
import hashlib
from pathlib import Path


def sign_file(path: Path, key: bytes) -> bytes:
    """Return HMAC-SHA256 signature for *path* using *key*."""
    h = hmac.new(key, digestmod=hashlib.sha256)
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.digest()


def verify_file(path: Path, signature: bytes, key: bytes) -> bool:
    """Verify file matches *signature* using *key*."""
    return hmac.compare_digest(sign_file(path, key), signature)
