import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(name: str, logs_dir: str = "logs", level: int = logging.DEBUG) -> logging.Logger:
    """Return a configured logger with rotating file handler."""
    path = Path(logs_dir)
    path.mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    # Include file name and line number in messages
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"
    )

    log_filename = f"{name.replace('.', '_')}.log"
    file_handler = RotatingFileHandler(
        path / log_filename, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)
    return logger
