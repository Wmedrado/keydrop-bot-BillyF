import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Required headings in the PR template
HEADINGS = [
    "## 📌 Objetivo do PR",
    "## ✅ Alterações principais",
    "## 🧪 Testes executados",
    "## 🧠 Contexto técnico",
    "## 📎 Arquivos afetados",
    "## 🧼 Checklist automático",
]

# Mapping from headings to required checkboxes
REQUIRED_CHECKS: Dict[str, List[str]] = {
    "## 🧪 Testes executados": ["Teste A", "Teste B"],
    "## 🧼 Checklist automático": [
        "PR validado localmente",
        "Build est\u00e1 passando",
        "Nenhum arquivo de conflito inclu\u00eddo",
    ],
}


def parse_sections(body: str) -> Dict[str, str]:
    """Return mapping from heading to its content."""
    sections: Dict[str, str] = {}
    for heading in HEADINGS:
        pattern = rf"{re.escape(heading)}\s*(.*?)(?=\n## |\Z)"
        m = re.search(pattern, body, flags=re.DOTALL)
        sections[heading] = m.group(1).strip() if m else ""
    return sections


def find_heading_lines(body: str) -> Dict[str, int]:
    lines = body.splitlines()
    numbers: Dict[str, int] = {}
    for i, line in enumerate(lines, 1):
        for heading in HEADINGS:
            if heading.lower() in line.lower():
                numbers[heading] = i
    return numbers


def parse_checkboxes(
    text: str,
    start_line: int,
) -> Dict[str, Tuple[bool, int]]:
    """Return mapping from checkbox label to (checked, line number)."""
    result: Dict[str, Tuple[bool, int]] = {}
    for offset, line in enumerate(text.splitlines(), 1):
        m = re.match(r"- \[(x| )\]\s*(.+)", line.strip(), re.I)
        if m:
            checked = m.group(1).lower() == "x"
            label = m.group(2).strip()
            result[label] = (checked, start_line + offset)
    return result


def validate_body(body: str, report_path: Path) -> bool:
    sections = parse_sections(body)
    heading_lines = find_heading_lines(body)
    ok = True
    report_lines = ["# PR Structure Report", ""]

    for heading in HEADINGS:
        text = sections.get(heading, "")
        line_no = heading_lines.get(heading, -1)
        if text:
            report_lines.append(f"- {heading}: OK (line {line_no})")
        else:
            msg = f"- {heading}: MISSING or EMPTY (line {line_no})"
            report_lines.append(msg)
            ok = False
        required = REQUIRED_CHECKS.get(heading)
        if required:
            checks = parse_checkboxes(text, line_no)
            for label in required:
                checked, ln = checks.get(label, (False, -1))
                status = "OK" if checked else "NOT CHECKED"
                report_lines.append(f"  - {label}: {status} (line {ln})")
                if not checked:
                    ok = False

    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    if ok:
        print("PR structure validation passed")
    else:
        print("PR structure validation failed")
    return ok


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
    event = os.environ.get("GITHUB_EVENT_PATH")
    body = load_pr_body(Path(event) if event else None)
    root = Path(__file__).resolve().parents[1]
    report = root / "ci" / "pr_structure_report.md"
    valid = validate_body(body, report)
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
