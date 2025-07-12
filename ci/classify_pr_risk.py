#!/usr/bin/env python3
"""CI helper to classify Pull Request risk based on changed files."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List
import sys

HIGH_PATTERNS = [
    "participation_engine",
    "contingency_engine",
    "browser_manager",
    "macro_recorder",
    "config/",
    "config.json",
]

MEDIUM_PATTERNS = [
    "frontend",
    "ui",
    "report",
    "stat",
    "monitoring",
    "collect",
]


def run_git_diff(base_ref: str, repo_root: Path) -> List[str]:
    """Return list of files changed between base_ref and HEAD."""
    subprocess.run(["git", "fetch", "origin", base_ref], cwd=repo_root, check=False)
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def classify_files(files: List[str]) -> str:
    modules = {f.split("/")[0] for f in files if "/" in f}
    if any(any(p in f for p in HIGH_PATTERNS) for f in files) or len(modules) > 5:
        return "Alto Risco"
    if any(any(p in f for p in MEDIUM_PATTERNS) for f in files):
        return "Médio Risco"
    return "Baixo Risco"


def generate_report(files: List[str], classification: str, repo_root: Path) -> Path:
    justifications = {
        "Alto Risco": "Mudanças em componentes críticos ou vários módulos simultaneamente.",
        "Médio Risco": "Altera interface do usuário ou componentes de coleta de dados.",
        "Baixo Risco": "Ajustes menores ou documentação.",
    }
    actions = {
        "Alto Risco": [
            "Validação duplicada por revisor automatizado",
            "Justificativa completa no history_of_decisions.md",
            "Testes atualizados e validados manualmente, se necessário",
        ],
        "Médio Risco": [
            "Rodar testes de UI",
            "Confirmar integridade de coleta de métricas",
        ],
        "Baixo Risco": ["Verificar documentação atualizada"],
    }

    report_path = repo_root / "ci" / "pr_risk_report.md"
    lines = [f"\N{bar chart} Classificação do PR: {classification}", "", "\N{open file folder} Arquivos afetados:"]
    lines.extend(f"- {f}" for f in files)
    lines.extend(["", "\N{round pushpin} Justificativa:", justifications[classification], "", "\N{shield} Ações exigidas:"])
    lines.extend(actions[classification])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main(base_ref: str = "origin/clean-main") -> int:
    repo_root = Path(__file__).resolve().parents[1]
    files = run_git_diff(base_ref, repo_root)
    classification = classify_files(files)
    report = generate_report(files, classification, repo_root)
    print(f"PR classified as: {classification}")
    print(f"Report generated at: {report}")
    return 0


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/clean-main"
    sys.exit(main(base))
