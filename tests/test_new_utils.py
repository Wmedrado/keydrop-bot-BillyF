import asyncio
from pathlib import Path
from bot_keydrop.utils.async_logger import AsyncRemoteHandler
from bot_keydrop.utils.secure_store import save_secure_json, load_secure_json
from bot_keydrop.utils.smart_timeout import smart_timeout
from bot_keydrop.system_safety.browser_compat import browser_driver_compatible
from bot_keydrop.system_safety.error_analyzer import analyze_error
import logging
import pytest


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
    content = offline.read_text()
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
