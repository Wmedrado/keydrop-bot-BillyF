import hashlib
import logging
import os
import traceback
from collections import Counter
from pathlib import Path
from typing import Callable, Optional

TEST_ENV_VAR = "PYTEST_CURRENT_TEST"

class ErrorReporter:
    """Collect exceptions and optionally send them elsewhere."""

    def __init__(self, log_file: Path = Path("logs/error_report.log"), send_callback: Optional[Callable[[str, str], None]] = None):
        self.log_file = log_file
        self.send_callback = send_callback
        self.counters = Counter()
        self.log_file.parent.mkdir(exist_ok=True)
        self.logger = logging.getLogger("error_reporter")

    def capture_exception(self, exc: Exception) -> str:
        """Capture an exception, store it and return its hash."""
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        hsh = hashlib.sha256(tb.encode()).hexdigest()[:8]
        self.counters[hsh] += 1
        entry = f"#{hsh} {self.counters[hsh]}x\n{tb}\n"
        with open(self.log_file, "a", encoding="utf-8") as fh:
            fh.write(entry)
        # Avoid sending notifications during automated tests
        if self.send_callback and TEST_ENV_VAR not in os.environ:
            try:
                self.send_callback(hsh, tb)
            except Exception as e:
                self.logger.warning("Failed to send error: %s", e)
        return hsh

error_reporter = ErrorReporter()
