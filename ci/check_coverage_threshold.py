import argparse
import sys
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_coverage(xml_path: Path) -> tuple[float, list[tuple[str, float]]]:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    total_lines = int(root.get("lines-valid", 0))
    covered = int(root.get("lines-covered", 0))
    overall = (covered / total_lines * 100) if total_lines else 0.0
    files: list[tuple[str, float]] = []
    for cls in root.findall(".//class"):
        filename = cls.get("filename", "")
        rate = float(cls.get("line-rate", 0)) * 100
        files.append((filename, rate))
    return round(overall, 2), files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min", type=float, default=0.0)
    parser.add_argument("--file", default="tests/coverage.xml")
    args = parser.parse_args()
    xml_path = Path(args.file)
    if not xml_path.exists():
        print(f"Coverage file not found: {xml_path}")
        return 1
    overall, files = parse_coverage(xml_path)
    print(f"Total coverage: {overall:.2f}%")
    low = [(f, r) for f, r in files if r < args.min]
    if low:
        print("Files below threshold:")
        for f, r in low:
            print(f"  {f}: {r:.2f}%")
    if overall < args.min:
        print(f"Coverage {overall:.2f}% below threshold {args.min}%")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
