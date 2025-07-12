import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ci import pr_commenter as pc  # noqa: E402
from ci import pr_changelog_generator as cg  # noqa: E402


def test_pr_commenter(tmp_path, monkeypatch):
    out = tmp_path / 'c.md'
    monkeypatch.setattr(pc, 'OUTPUT', out)
    monkeypatch.setattr(pc, 'get_changed_files', lambda: ['a.py'])
    pc.main()
    assert '- a.py' in out.read_text()


def test_changelog_generator(tmp_path, monkeypatch):
    out = tmp_path / 'ch.md'
    monkeypatch.setattr(cg, 'OUTPUT', out)
    monkeypatch.setattr(cg, 'generate_changelog', lambda: '# Changelog\n\n- Test')
    cg.main()
    assert out.read_text().startswith('# Changelog')
