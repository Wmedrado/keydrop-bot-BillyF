import re
import sys
from pathlib import Path


def clean_file(path: Path) -> bool:
    """Remove simple git conflict markers, keeping the longer section."""
    text = path.read_text(encoding="utf-8")
    if "<<<<<<<" not in text:
        return False

    pattern = re.compile(
        r"<<<<<<<[^\n]*\n(.*?)\n=======\n(.*?)\n>>>>>>>[^\n]*\n",
        re.DOTALL,
    )

    def replace(match: re.Match) -> str:
        first, second = match.group(1), match.group(2)
        return first if len(first) >= len(second) else second

    new_text = pattern.sub(replace, text)
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    changed = False
    for p in repo_root.rglob('*'):
        if p.is_file() and p.suffix != '.pyc':
            try:
                if clean_file(p):
                    print(f"Cleaned conflicts in {p}")
                    changed = True
            except UnicodeDecodeError:
                continue
    return 0 if changed else 0


if __name__ == '__main__':
    sys.exit(main())
