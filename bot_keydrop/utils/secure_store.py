"""Simple AES encryption helpers for storing sensitive data."""

from __future__ import annotations

import json
import os
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend

BLOCK = 128


def _get_cipher(key: bytes, iv: bytes) -> Cipher:
    return Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())


def encrypt_data(data: bytes, key: bytes) -> bytes:
    iv = os.urandom(16)
    cipher = _get_cipher(key, iv)
    padder = PKCS7(BLOCK).padder()
    padded = padder.update(data) + padder.finalize()
    ct = cipher.encryptor().update(padded) + cipher.encryptor().finalize()
    return iv + ct


def decrypt_data(data: bytes, key: bytes) -> bytes:
    iv, ct = data[:16], data[16:]
    cipher = _get_cipher(key, iv)
    pt = cipher.decryptor().update(ct) + cipher.decryptor().finalize()
    unpadder = PKCS7(BLOCK).unpadder()
    return unpadder.update(pt) + unpadder.finalize()


def save_secure_json(path: Path | str, obj: dict, key: bytes) -> None:
    raw = json.dumps(obj).encode("utf-8")
    enc = encrypt_data(raw, key)
    Path(path).write_bytes(enc)


def load_secure_json(path: Path | str, key: bytes) -> dict:
    enc = Path(path).read_bytes()
    data = decrypt_data(enc, key)
    return json.loads(data.decode("utf-8"))
