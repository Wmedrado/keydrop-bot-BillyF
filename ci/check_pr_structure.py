import json
import os
import re
from pathlib import Path
from typing import Dict, List

REQUIRED_HEADINGS = {
    "objective": "### 🧠 Objetivo da alteração",
    "files": "### 📍 Arquivos principais alterados",
    "impact": "### 🔁 Impacto em outros módulos",
    "tests": "### 🧪 Testes existentes cobrem essa lógica?",
    "security": "### 🔐 Algum risco de segurança?",
    "history": "### ✅ Justificativa no history_of_decisions.md?",
}


def parse_blocks(body: str) -> Dict[str, str]:
    """Return mapping from heading keys to block text."""
    blocks = {}
    for key, heading in REQUIRED_HEADINGS.items():
        pattern = rf"{re.escape(heading)}\s+(.*?)(?=\n### |\Z)"
        m = re.search(pattern, body, flags=re.DOTALL)
        if m:
            blocks[key] = m.group(1).strip()
        else:
            blocks[key] = ""
    return blocks


def validate_body(body: str, report_path: Path) -> bool:
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
