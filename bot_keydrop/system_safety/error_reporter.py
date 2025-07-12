import hashlib
import json
import logging
import os
import sys
import traceback
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

TEST_ENV_VAR = "PYTEST_CURRENT_TEST"
import getpass

import requests


class ErrorReporter:
    """Collect exceptions and optionally send them elsewhere."""

    WEBHOOK_URL = (
        "https://discord.com/api/webhooks/1393540798359801856/"
        "aIWcdtx4C6PLlQWet7j43Q9RdOS_XO8r48wP5UuHnq1-"
        "AlpYSo6k7nay1oFaIxWDCXeH"
    )

    def __init__(
        self,
        log_file: Path = Path("logs/error_report.log"),
        pending_file: Path = Path("logs/errors_pending.json"),
        send_callback: Optional[Callable[[str, str], None]] = None,
    ):
        self.log_file = log_file
        self.pending_file = pending_file
        self.send_callback = send_callback
        self.counters = Counter()
        self.log_file.parent.mkdir(exist_ok=True)
        self.pending_file.parent.mkdir(exist_ok=True)
        self.logger = logging.getLogger("error_reporter")

    def register_global_handler(self) -> None:
        """Register sys.excepthook for automatic error capture."""
        sys.excepthook = self.handle_exception

    # ------------------------------------------------------------------
    def handle_exception(self, exc_type, exc, tb) -> None:
        """Global exception handler that logs and reports."""
        # pragma: no cover
        exception = exc if isinstance(exc, Exception) else Exception(str(exc))
        exception.__traceback__ = tb
        self.capture_exception(exception)

    def capture_exception(self, exc: Exception) -> str:
        """Capture an exception, store it and return its hash."""
        tb = "".join(
            traceback.format_exception(
                type(exc),
                exc,
                exc.__traceback__,
            )
        )
        hsh = hashlib.sha256(tb.encode()).hexdigest()[:8]
        self.counters[hsh] += 1
        entry = f"#{hsh} {self.counters[hsh]}x\n{tb}\n"
        with open(self.log_file, "a", encoding="utf-8") as fh:
            fh.write(entry)

        # Avoid sending notifications during automated tests
        if self.send_callback and TEST_ENV_VAR not in os.environ:

        info = self._build_error_data(exc, tb)
        self._flush_pending()
        if not self._send_discord(info):
            self._save_pending(info)

        if self.send_callback:
            try:
                self.send_callback(hsh, tb)
            except Exception as e:
                self.logger.warning("Failed to send error: %s", e)
        return hsh

    # ------------------------------------------------------------------
    def _build_error_data(self, exc: Exception, tb: str) -> dict:
        stack = traceback.extract_tb(exc.__traceback__)
        file_name = stack[-1].filename if stack else "unknown"
        line_no = stack[-1].lineno if stack else 0
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file": file_name,
            "line": line_no,
            "message": f"{type(exc).__name__}: {exc}",
            "stacktrace": tb,
            "user": getpass.getuser(),
            "executable": Path(sys.argv[0]).name,
        }

    # ------------------------------------------------------------------
    def _send_discord(self, info: dict) -> bool:
        if not self.WEBHOOK_URL:
            return False
        embed = self._build_embed(info)
        payload = {"embeds": [embed]}
        try:
            resp = requests.post(self.WEBHOOK_URL, json=payload, timeout=10)
            return resp.status_code in (200, 204)
        except Exception as e:  # pragma: no cover - network may fail
            self.logger.warning(
                "Failed to send Discord webhook, fallback to queue: %s", e
            )
            return False

    # ------------------------------------------------------------------
    def _build_embed(self, info: dict) -> dict:
        stack = f"```{info['stacktrace'][:1800]}```"
        parts = [
            ("\ud83d\udd52 Data/Hora", info["timestamp"], True),
            ("\ud83d\udcc4 Arquivo", info["file"], True),
            ("\ud83d\udd0d Linha", str(info["line"]), True),
            ("\ud83d\udcac Mensagem", info["message"], False),
            ("\ud83e\udde0 Stacktrace", stack, False),
            ("\ud83d\udc64 Usu\u00e1rio", info["user"], True),
            ("\ud83d\udcbb Vers\u00e3o", info["executable"], True),
        ]

        fields = [{"name": n, "value": v, "inline": i} for n, v, i in parts]
        return {
            "title": "\ud83d\udded Erro capturado no App Desktop!",
            "color": 0xE74C3C,
            "fields": fields,
        }

    # ------------------------------------------------------------------
    def _save_pending(self, info: dict) -> None:
        try:
            queue = []
            if self.pending_file.exists():
                queue = json.loads(
                    self.pending_file.read_text(encoding="utf-8"),
                )
            queue.append(info)
            with open(self.pending_file, "w", encoding="utf-8") as fh:
                json.dump(queue, fh, ensure_ascii=False, indent=2)
        except Exception as e:  # pragma: no cover - disk may fail
            self.logger.warning("Failed to save pending error: %s", e)

    # ------------------------------------------------------------------
    def _flush_pending(self) -> None:
        if not self.pending_file.exists():
            return
        try:
            queue = json.loads(
                self.pending_file.read_text(encoding="utf-8"),
            )
        except Exception:
            return
        remaining = []
        for item in queue:
            if not self._send_discord(item):
                remaining.append(item)
        if remaining:
            with open(self.pending_file, "w", encoding="utf-8") as fh:
                json.dump(remaining, fh, ensure_ascii=False, indent=2)
        else:
            try:
                self.pending_file.unlink()
            except Exception:
                pass


error_reporter = ErrorReporter()
error_reporter.register_global_handler()
