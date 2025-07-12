#!/usr/bin/env python3
"""Generate a simple comment summarizing PR impact."""
from __future__ import annotations

import subprocess
from pathlib import Path


def changed_files(base_ref: str = "origin/clean-main") -> list[str]:
    subprocess.run(["git", "fetch", "origin", base_ref], check=False)
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"], capture_output=True, text=True
    )
    return [f for f in result.stdout.splitlines() if f]


def generate_comment(files: list[str]) -> str:
    modules = sorted({Path(f).parts[0] for f in files if "/" in f})
    lines = ["### Impacto do PR", "", "Arquivos modificados:"]
    lines.extend(f"- {f}" for f in files)
    lines.append("")
    lines.append("Módulos afetados: " + ", ".join(modules))
    return "\n".join(lines)


def main() -> int:
    files = changed_files()
    text = generate_comment(files)
    out = Path("ci/pr_impact_comment.md")
    out.write_text(text, encoding="utf-8")
    print(f"Comment saved to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

