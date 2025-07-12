# bot_keydrop.system_safety.crash_tracker

Tracks the last executed line before a fatal exception for easier debugging.

## Functions

- `log_last_line(exc: Exception) -> None` – writes the filename, line number and function name for the final stack frame of the given exception to `logs/last_crash.log`.
