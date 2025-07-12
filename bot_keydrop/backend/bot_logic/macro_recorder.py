import json
import time
from pathlib import Path
from typing import Any, List
from playwright.async_api import Page

class MacroRecorder:
    """Simple macro recorder to capture basic browser interactions."""

    def __init__(self, page: Page):
        self.page = page
        self.events: List[dict] = []
        self.recording = False
        self.paused = False
        self.last_timestamp: float | None = None

    async def start(self):
        if self.recording:
            return
        self.events.clear()
        self.recording = True
        self.paused = False
        self.last_timestamp = time.time()
        await self.page.expose_binding("py_record_event", self._record_event)
        await self.page.evaluate(_JS_START_LISTENERS)

    async def _record_event(self, source: Any, data: dict):
        if not self.recording or self.paused:
            return
        now = time.time()
        delay = 0 if self.last_timestamp is None else now - self.last_timestamp
        self.last_timestamp = now
        data["delay"] = delay
        self.events.append(data)

    async def pause(self):
        self.paused = True

    async def resume(self):
        self.paused = False

    async def stop(self):
        if not self.recording:
            return
        await self.page.evaluate(_JS_REMOVE_LISTENERS)
        self.recording = False

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.events, fh, ensure_ascii=False, indent=2)

_JS_START_LISTENERS = """
(() => {
    const getSel = el => {
        if (!el) return '';
        if (el.id) return '#' + el.id;
        if (el.className && el.className.toString().trim()) {
            return el.tagName.toLowerCase() + '.' + Array.from(el.classList).join('.');
        }
        return el.tagName.toLowerCase();
    };
    window._macroHandlers = {
        click: e => window.py_record_event({type:'click', x:e.clientX, y:e.clientY, selector:getSel(e.target)}),
        input: e => window.py_record_event({type:'input', value:e.target.value, selector:getSel(e.target)}),
        scroll: e => window.py_record_event({type:'scroll', x:window.scrollX, y:window.scrollY})
    };
    document.addEventListener('click', window._macroHandlers.click, true);
    document.addEventListener('input', window._macroHandlers.input, true);
    document.addEventListener('scroll', window._macroHandlers.scroll, true);
})();
"""

_JS_REMOVE_LISTENERS = """
(() => {
    if (!window._macroHandlers) return;
    document.removeEventListener('click', window._macroHandlers.click, true);
    document.removeEventListener('input', window._macroHandlers.input, true);
    document.removeEventListener('scroll', window._macroHandlers.scroll, true);
    delete window._macroHandlers;
})();
"""
