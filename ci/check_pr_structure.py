import json
import os
import re
from pathlib import Path
from typing import Dict, List
import time

REQUIRED_HEADINGS = {
    "objective": "### 🌐 Objetivo da alteração",
    "files": "### 📂 Arquivos principais alterados",
    "impact": "### 🔍 Impacto em outros módulos",
    "tests": "### 🧪 Testes existentes cobrem essa lógica?",
    "security": "### 🔒 Algum risco de segurança?",
    "history": "### ✅ Justificativa no history_of_decisions.md",
}


def parse_blocks(body: str) -> Dict[str, str]:
    """Return mapping from heading keys to block text."""
    blocks: Dict[str, str] = {}
    lower_body = body.lower()
    headings = list(REQUIRED_HEADINGS.values())
    for i, (key, heading) in enumerate(REQUIRED_HEADINGS.items()):
        start = lower_body.find(heading.lower())
        if start == -1:
            blocks[key] = ""
            continue
        start += len(heading)
        next_idx = len(body)
        for next_heading in headings[i + 1 :]:
            idx = lower_body.find(next_heading.lower(), start)
            if idx != -1:
                next_idx = idx
                break
        blocks[key] = body[start:next_idx].strip()
    return blocks


def validate_body(body: str, report_path: Path) -> bool:
    start = time.perf_counter()
    blocks = parse_blocks(body)
    missing: List[str] = []
    report_lines = ["# PR Structure Validation", ""]
    for key, heading in REQUIRED_HEADINGS.items():
        text = blocks[key]
        if text:
            report_lines.append(f"- {heading}: OK")
        else:
            report_lines.append(f"- {heading}: MISSING")
            missing.append(heading)
    elapsed = time.perf_counter() - start
    report_lines.append("")
    report_lines.append("## Resumo")
    report_lines.append(f"- Blocos verificados: {len(REQUIRED_HEADINGS)}")
    report_lines.append(f"- Blocos ausentes: {len(missing)}")
    report_lines.append(f"- Tempo de execução: {elapsed:.2f}s")
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    if missing:
        print("Missing or empty sections: " + ", ".join(missing))
        return False
    print("PR structure valid")
    return True


def load_pr_body(event_path: Path | None) -> str:
    if event_path and event_path.exists():
        with event_path.open(encoding="utf-8") as f:
            data = json.load(f)
        return data.get("pull_request", {}).get("body", "") or ""
    return ""


def main() -> int:
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        print("Not a pull_request event")
        return 0
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    body = load_pr_body(Path(event_path) if event_path else None)
    root = Path(__file__).resolve().parents[1]
    report_path = root / "ci" / "pr_structure_report.md"
    valid = validate_body(body, report_path)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
