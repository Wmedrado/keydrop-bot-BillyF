from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from reviewer_ai.auto_review_engine import main as run_review  # noqa: E402


def test_auto_review_file_created(tmp_path):
    review_file = ROOT / "ci" / "auto_review.md"
    if review_file.exists():
        review_file.unlink()
    run_review()
    assert review_file.exists()
    try:
        content = review_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = review_file.read_text(encoding="latin-1")
    assert content.strip()
