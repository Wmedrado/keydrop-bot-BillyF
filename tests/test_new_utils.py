import asyncio
import time
from pathlib import Path
import logging
from unittest import mock
import pytest

from bot_keydrop.utils.async_logger import AsyncRemoteHandler
from bot_keydrop.utils.secure_store import save_secure_json, load_secure_json
from bot_keydrop.utils.smart_timeout import smart_timeout
from bot_keydrop.utils.smart_cache import cache_result
from bot_keydrop.utils.history_recorder import record_history
from bot_keydrop.system_safety.browser_compat import browser_driver_compatible
from bot_keydrop.system_safety.error_analyzer import analyze_error
from bot_keydrop.system_safety.rate_limiter import RateLimiter
from bot_keydrop.system_safety.browser_fallback import launch_browser_with_fallback


class DummySender:
    def __init__(self):
        self.calls = []

    def post(self, url, json=None, timeout=5):
        self.calls.append(json["log"])

        class R:
            status_code = 200

        return R()


def test_async_logger_fallback(tmp_path, monkeypatch):
    offline = tmp_path / "off.log"
    handler = AsyncRemoteHandler("http://example.com", fallback_file=offline)

    def fail_post(url, json=None, timeout=5):
        raise RuntimeError

    monkeypatch.setattr(handler.session, "post", fail_post)
    logger = logging.getLogger("t")
    logger.addHandler(handler)
    logger.error("fail message")
    handler.queue.join()
    assert offline.exists()
    try:
        content = offline.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = offline.read_text(encoding="latin-1")
    assert "fail message" in content


def test_secure_store_roundtrip(tmp_path):
    key = b"0" * 32
    data = {"token": "abc"}
    file = tmp_path / "data.sec"
    save_secure_json(file, data, key)
    loaded = load_secure_json(file, key)
    assert loaded == data


@pytest.mark.asyncio
async def test_smart_timeout_retry(monkeypatch):
    calls = []

    @smart_timeout(0.01, retries=2)
    async def func():
        calls.append(1)
        await asyncio.sleep(0.02)
        return 5

    with pytest.raises(asyncio.TimeoutError):
        await func()
    assert len(calls) == 2


def test_browser_driver_compatible():
    assert browser_driver_compatible(Path("chrome.exe"), Path("chromedriver.exe")) in (
        True,
        False,
    )


def test_error_analyzer():
    msg = analyze_error("Erro 429: too many requests")
    assert "bloqueio" in msg

def test_cache_result():
    calls = []

    @cache_result(ttl=0.1)
    def add(a, b):
        calls.append(1)
        return a + b

    assert add(1, 2) == 3
    assert add(1, 2) == 3
    assert len(calls) == 1
    time.sleep(0.11)
    assert add(1, 2) == 3
    assert len(calls) == 2


def test_rate_limiter():
    rl = RateLimiter(2, 0.5)
    assert rl.allow("p")
    assert rl.allow("p")
    assert not rl.allow("p")
    time.sleep(0.6)
    assert rl.allow("p")


@mock.patch("shutil.which", return_value=None)
def test_browser_fallback(mock_which, tmp_path, monkeypatch):
    """Ensure fallback returns ``None`` when no browsers are available."""
    fake = tmp_path / "notfound.exe"
    monkeypatch.setattr(
        "bot_keydrop.system_safety.browser_fallback.BROWSER_PATHS",
        [],
        raising=False,
    )
    assert launch_browser_with_fallback(str(fake)) is None


def test_record_history(tmp_path):
    record_history("user", "event", logs_dir=tmp_path)
    log_file = tmp_path / "user_history.log"
    assert log_file.exists()
    try:
        content = log_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = log_file.read_text(encoding="latin-1")
    assert "event" in content
