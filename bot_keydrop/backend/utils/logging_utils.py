import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime, timedelta
import gzip
import shutil

LOG_DIR = Path("logs")


def setup_logging(max_bytes: int = 5 * 1024 * 1024, backup_count: int = 3, retention_days: int = 7) -> Path:
    """Configure logging with rotating file handler and cleanup."""
    LOG_DIR.mkdir(exist_ok=True)
    today = datetime.now().date()
    index = 0
    while True:
        file_name = f"bot_{index}_{today}.log"
        log_file = LOG_DIR / file_name
        if not log_file.exists():
            break
        index += 1

    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    handler.setFormatter(formatter)

    logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)
    cleanup_old_logs(retention_days)
    return log_file


def cleanup_old_logs(retention_days: int = 7) -> None:
    """Compress logs older than retention_days."""
    cutoff = datetime.now() - timedelta(days=retention_days)
    for log_file in LOG_DIR.glob("bot_*.log"):
        if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff:
            compressed = log_file.with_suffix(log_file.suffix + ".gz")
            with open(log_file, "rb") as f_in, gzip.open(compressed, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
            log_file.unlink()
