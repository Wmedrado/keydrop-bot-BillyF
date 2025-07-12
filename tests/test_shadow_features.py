import json

from bot_keydrop.testing.shadow_testing import run_shadow_test
from bot_keydrop.testing.fake_users import generate_fake_users
from bot_keydrop.testing.log_comparer import compare_logs
from ci.rollback_validator import should_trigger_rollback


def test_run_shadow_test_match():
    assert run_shadow_test(lambda x: x + 1, lambda x: x + 1, [1, 2, 3])


def test_run_shadow_test_mismatch():
    assert not run_shadow_test(lambda x: x + 1, lambda x: x + 2, [1])


def test_generate_fake_users_count():
    users = generate_fake_users(5)
    assert len(users) == 5
    assert {u["id"] for u in users} == set(range(5))


def test_compare_logs(tmp_path):
    a = tmp_path / "a.log"
    b = tmp_path / "b.log"
    a.write_text("line1\nline2")
    b.write_text("line1\nlineX")
    diffs = compare_logs(a, b)
    assert "line2" in diffs[0]


def test_should_trigger_rollback():
    files = ["src/login/main.py", "docs/readme.md"]
    assert should_trigger_rollback(files)
    assert not should_trigger_rollback(["docs/readme.md"])


def test_branch_failure_manager(tmp_path, monkeypatch):
    from ci import branch_failure_manager as bfm

    state = tmp_path / "state.json"
    bfm.STATE_FILE = state
    branch = "test/ai"
    for _ in range(3):
        bfm.update_failure(success=False, branch=branch)
    assert bfm.check_and_mark(branch)
    try:
        st_content = state.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        st_content = state.read_text(encoding="latin-1")
    data = json.loads(st_content)
    assert data[branch] == 3
