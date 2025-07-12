import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import time

# Required headings in the PR template
HEADINGS = [
    "### 🌐 Objetivo da alteração",
    "### 📂 Arquivos principais alterados",
    "### 🔍 Impacto em outros módulos",
    "### 🧪 Testes existentes cobrem essa lógica?",
    "### 🔒 Algum risco de segurança?",
    "### ✅ Justificativa no history_of_decisions.md",
]

# Mapping from headings to required checkboxes (kept for future extension)
REQUIRED_CHECKS: Dict[str, List[str]] = {}


def parse_sections(body: str) -> Dict[str, str]:
    """Return mapping from heading to its content."""
    sections: Dict[str, str] = {}
    lower_body = body.lower()
    for i, heading in enumerate(HEADINGS):
        start = lower_body.find(heading.lower())
        if start == -1:
            sections[heading] = ""
            continue
        start += len(heading)
        next_idx = len(body)
        for next_heading in HEADINGS[i + 1 :]:
            idx = lower_body.find(next_heading.lower(), start)
            if idx != -1:
                next_idx = idx
                break
        sections[heading] = body[start:next_idx].strip()
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
    start = time.perf_counter()
    sections = parse_sections(body)
    heading_lines = find_heading_lines(body)
    ok = True
    missing: List[str] = []
    malformed: List[str] = []
    report_lines = ["# PR Structure Report", ""]

    for heading in HEADINGS:
        text = sections.get(heading, "")
        line_no = heading_lines.get(heading, -1)
        if text:
            report_lines.append(f"- {heading}: OK (line {line_no})")
        else:
            msg = f"- {heading}: MISSING (line {line_no})"
            report_lines.append(msg)
            missing.append(heading)
            ok = False
        required = REQUIRED_CHECKS.get(heading)
        if required:
            checks = parse_checkboxes(text, line_no)
            for label in required:
                checked, ln = checks.get(label, (False, -1))
                status = "OK" if checked else "NOT CHECKED"
                report_lines.append(f"  - {label}: {status} (line {ln})")
                if not checked:
                    malformed.append(label)
                    ok = False

    elapsed = time.perf_counter() - start
    report_lines.append("")
    report_lines.append("## Resumo")
    report_lines.append(f"- Blocos verificados: {len(HEADINGS)}")
    report_lines.append(f"- Blocos ausentes: {len(missing)}")
    report_lines.append(f"- Blocos mal preenchidos: {len(malformed)}")
    report_lines.append(f"- Tempo de execução: {elapsed:.2f}s")

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
