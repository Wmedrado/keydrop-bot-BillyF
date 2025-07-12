"""Script para atualizar permissões de usuário no Firebase."""
from __future__ import annotations

import argparse
from typing import Dict

from cloud.permissions import update_permissions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Atualiza permissoes no Firebase")
    parser.add_argument("user_id", help="ID do usuario")
    parser.add_argument(
        "--set",
        nargs="*",
        default=[],
        metavar="KEY=VALUE",
        help="Pares de chave=valor para atualizar",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    updates: Dict[str, object] = {}
    for item in args.set:
        if "=" not in item:
            raise ValueError(f"Formato invalido: {item}")
        key, value = item.split("=", 1)
        if value.lower() in {"true", "false"}:
            updates[key] = value.lower() == "true"
        else:
            updates[key] = value
    update_permissions(args.user_id, updates)
    print("Permissoes atualizadas com sucesso")


if __name__ == "__main__":
    main()
