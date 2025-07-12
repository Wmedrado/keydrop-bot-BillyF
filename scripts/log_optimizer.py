from pathlib import Path

LOG_DIR = Path("logs")


def analyze() -> list[str]:
    suggestions = []
    for log in LOG_DIR.glob("*.log"):
        text = log.read_text(errors="ignore")
        if text.count("Exception") > 5:
            suggestions.append(f"{log.name}: many exceptions")
        if "duplicate" in text.lower():
            suggestions.append(f"{log.name}: possible duplication spotted")
    return suggestions


def main() -> int:
    sugg = analyze()
    for s in sugg:
        print("Suggestion:", s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
