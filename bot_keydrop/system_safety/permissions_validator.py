from pathlib import Path


def validar_permissoes(pastas) -> bool:
    """Check if the given folders are writable."""
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

