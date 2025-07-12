import asyncio
import logging
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bot_keydrop.system_safety import diagnostic, error_reporter


def test_diagnostic_sync_logging(tmp_path, caplog):
    error_reporter.log_file = tmp_path / "err.log"
    error_reporter.counters.clear()

    @diagnostic
    def add(a, b):
        return a + b

    with caplog.at_level(logging.DEBUG):
        result = add(1, 2)

    assert result == 3
    messages = [r.message for r in caplog.records]
    assert any("Entering" in m for m in messages)
    assert any("Exiting" in m for m in messages)

    @diagnostic
    def fail():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        with caplog.at_level(logging.DEBUG):
            fail()

    assert error_reporter.log_file.exists()
    content = error_reporter.log_file.read_text()
    assert "boom" in content


@pytest.mark.asyncio
async def test_diagnostic_async_logging(tmp_path, caplog):
    error_reporter.log_file = tmp_path / "err_async.log"
    error_reporter.counters.clear()

    @diagnostic
    async def double(x):
        await asyncio.sleep(0.01)
        return x * 2

    with caplog.at_level(logging.DEBUG):
        result = await double(3)

    assert result == 6
    messages = [r.message for r in caplog.records]
    assert any("Entering" in m for m in messages)
    assert any("Exiting" in m for m in messages)
