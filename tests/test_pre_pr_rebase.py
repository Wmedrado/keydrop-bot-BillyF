from ci.pre_pr_rebase import is_ai_branch


def test_is_ai_branch():
    assert is_ai_branch("codex/feature")
    assert is_ai_branch("bot/update")
    assert not is_ai_branch("feature/foo")
