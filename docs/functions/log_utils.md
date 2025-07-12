# log_utils.py

Utility for creating configured loggers with rotating file handlers. Logs are
stored under the `logs/` directory and also streamed to stdout.

The formatter includes timestamp, level, logger name, module, line number and
message to aid debugging.

## Functions
- `setup_logger(name: str, logs_dir: str = "logs", level: int = logging.DEBUG) -> logging.Logger`
  Creates and returns a logger that writes to a rotating file and to the
  console. The logger directory is created if missing.
