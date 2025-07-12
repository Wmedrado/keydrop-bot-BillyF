from ci.log_suggestions import generate_suggestions, tail_lines
from pathlib import Path


def test_generate_suggestions():
    lines = ["INFO all good", "ERROR 429: too many requests", "Exception: TimeoutError"]
    suggestions = generate_suggestions(lines)
    joined = " ".join(suggestions).lower()
    assert "bloqueio" in joined
    assert "tempo" in joined


def test_tail_lines(tmp_path: Path):
    log = tmp_path / "log.txt"
    log.write_text("\n".join(str(i) for i in range(20)), encoding="utf-8")
    result = tail_lines(log, 5)
    assert result == [str(i) for i in range(15, 20)]
