# bot_keydrop.utils.secure_store

Helpers for AES encryption of sensitive data.

- `encrypt_data(data: bytes, key: bytes) -> bytes`
- `decrypt_data(data: bytes, key: bytes) -> bytes`
- `save_secure_json(path: Path, obj: dict, key: bytes) -> None`
- `load_secure_json(path: Path, key: bytes) -> dict`
