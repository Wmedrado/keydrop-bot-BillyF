import sys
from pathlib import Path

CHECKLIST_FILE = Path(__file__).resolve().parent / "pr_checklist.md"
REPORT_FILE = Path(__file__).resolve().parent / "checklist_status.md"


def parse_checklist(text: str):
    items = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [") and "]" in stripped:
            checked = stripped.startswith("- [x]")
            label = stripped[stripped.index("]") + 1:].strip()
            items.append((label, checked))
    return items


def main() -> int:
    if not CHECKLIST_FILE.exists():
        print("Checklist file ci/pr_checklist.md not found")
        return 1

    items = parse_checklist(CHECKLIST_FILE.read_text())
    if not items:
        print("Checklist file has no items")
        return 1

    lines = ["# Checklist Status", ""]
    all_marked = True
    for label, checked in items:
        symbol = "✅" if checked else "❌"
        lines.append(f"- {symbol} {label}")
        if not checked:
            all_marked = False
    REPORT_FILE.write_text("\n".join(lines) + "\n")

    if not all_marked:
        print("Checklist incomplete: mark all items with [x] in ci/pr_checklist.md")
        return 1
    print("Checklist complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
