import hashlib
import json
import logging
import os
import sys
import traceback
from collections import Counter
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Callable, Optional, Dict
import socket
import platform
import uuid
import requests

TEST_ENV_VAR = "PYTEST_CURRENT_TEST"
IS_TEST_ENV_VAR = "IS_TEST_ENV"


def _is_test_env() -> bool:
    """Return True when running under pytest or CI test environment."""
    return (
        TEST_ENV_VAR in os.environ
        or os.getenv(IS_TEST_ENV_VAR, "").lower() == "true"
    )


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
        db_file: Path = Path("logs/error_stats.json"),
        send_callback: Optional[Callable[[str, str], None]] = None,
        resolution_minutes: int = 60,
    ):
        self.log_file = log_file
        self.pending_file = pending_file
        self.db_file = db_file
        self.send_callback = send_callback
        self.resolution_minutes = resolution_minutes
        self.counters = Counter()
        self.log_file.parent.mkdir(exist_ok=True)
        self.pending_file.parent.mkdir(exist_ok=True)
        self.db_file.parent.mkdir(exist_ok=True)
        self.logger = logging.getLogger("error_reporter")
        self.db: Dict[str, Dict] = self._load_db()
        self.last_notified: Dict[str, datetime] = {}

    # ------------------------------------------------------------------
    def _load_db(self) -> Dict[str, Dict]:
        if self.db_file.exists():
            try:
                return json.loads(self.db_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"errors": {}}

    def _save_db(self) -> None:
        try:
            with open(self.db_file, "w", encoding="utf-8") as fh:
                json.dump(self.db, fh, ensure_ascii=False, indent=2)
        except Exception as exc:
            self.logger.warning("Failed to save db: %s", exc)

    def register_global_handler(self) -> None:
        """Register sys.excepthook for automatic error capture."""
        sys.excepthook = self.handle_exception

    # ------------------------------------------------------------------
    def _check_resolved(self) -> None:
        now = datetime.utcnow()
        expired = []
        for key, data in self.db.get("errors", {}).items():
            if not data.get("resolved"):
                try:
                    last = datetime.fromisoformat(data["last_seen"])
                except Exception:
                    continue
                if (now - last) > timedelta(minutes=self.resolution_minutes):
                    data["resolved"] = True
                    expired.append((key, data))
        if expired:
            self._save_db()
            for key, info in expired:
                self._send_resolution(key, info)

    # ------------------------------------------------------------------
    def _identify_user(self) -> str:
        email = os.environ.get("USER_EMAIL") or os.environ.get("EMAIL")
        if email:
            return email
        try:
            ip = socket.gethostbyname(socket.gethostname())
            if ip:
                return ip
        except Exception:
            pass
        host = platform.node() or str(uuid.getnode())
        return host or "Usuário desconhecido"

    # ------------------------------------------------------------------
    def _send_resolution(self, key: str, info: Dict) -> None:
        embed = {
            "title": "✅ Erro Resolvido!",
            "color": 0x2ECC71,
            "fields": [
                {"name": "Arquivo", "value": key.split(":")[0], "inline": True},
                {"name": "Linha", "value": key.split(":")[1], "inline": True},
                {"name": "Mensagem anterior", "value": info.get("message", ""), "inline": False},
                {"name": "Última ocorrência", "value": info.get("last_seen", ""), "inline": False},
            ],
        }
        payload = {"embeds": [embed]}
        try:
            requests.post(self.WEBHOOK_URL, json=payload, timeout=10)
        except Exception:
            pass

    # ------------------------------------------------------------------
    def handle_exception(self, exc_type, exc, tb) -> None:
        """Global exception handler that logs and reports."""
        # pragma: no cover
        exception = exc if isinstance(exc, Exception) else Exception(str(exc))
        exception.__traceback__ = tb
        self.capture_exception(exception)

    def capture_exception(self, exc: Exception) -> str:
        """Capture an exception, store it and return its hash."""
        self._check_resolved()
        tb = "".join(
            traceback.format_exception(
                type(exc),
                exc,
                exc.__traceback__,
            )
        )
        stack = traceback.extract_tb(exc.__traceback__)
        file_name = Path(stack[-1].filename).name if stack else "unknown"
        line_no = stack[-1].lineno if stack else 0
        key = f"{file_name}:{line_no}:{type(exc).__name__}"
        error_hash = hashlib.sha256(
            f"{file_name}{line_no}{type(exc).__name__}{exc}".encode()
        ).hexdigest()[:8]
        self.counters[error_hash] += 1

        entry = f"#{error_hash} {self.counters[error_hash]}x\n{tb}\n"
        with open(self.log_file, "a", encoding="utf-8") as fh:
            fh.write(entry)

        # update db
        rec = self.db.setdefault("errors", {}).setdefault(
            key,
            {"last_seen": "", "count": 0, "resolved": False, "message": str(exc)},
        )
        rec["last_seen"] = datetime.utcnow().isoformat()
        rec["count"] += 1
        rec["resolved"] = False
        rec["message"] = str(exc)
        self._save_db()

        info = self._build_error_data(exc, tb)
        now = datetime.utcnow()
        notify = True
        last = self.last_notified.get(key)
        if last and (now - last).total_seconds() < 600:
            notify = False

        if not _is_test_env() and notify:
            self._flush_pending()
            if not self._send_discord(info):
                self._save_pending(info)
            self.last_notified[key] = now

            if self.send_callback:
                try:
                    self.send_callback(error_hash, tb)
                except Exception as e:
                    self.logger.warning("Failed to send error: %s", e)

        return error_hash

    # ------------------------------------------------------------------
    def _build_error_data(self, exc: Exception, tb: str) -> dict:
        stack = traceback.extract_tb(exc.__traceback__)
        file_name = stack[-1].filename if stack else "unknown"
        line_no = stack[-1].lineno if stack else 0
        return {
            "timestamp": datetime.now(ZoneInfo("America/Sao_Paulo")).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "file": file_name,
            "line": line_no,
            "message": f"{type(exc).__name__}: {exc}",
            "stacktrace": tb,
            "user": self._identify_user(),
            "ip": socket.gethostbyname(socket.gethostname()),
            "machine": platform.node(),
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
            ("\ud83d\udcbb IP", info.get("ip", ""), True),
            ("\ud83d\udcbb Máquina", info.get("machine", ""), True),
            ("\ud83d\udcbb Versão", info["executable"], True),
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
