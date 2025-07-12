# bot_keydrop.resilience_utils

Utility helpers for building resilient functions.

## Components

- `CircuitBreaker` – tracks consecutive failures and raises `CircuitOpen` when the threshold is exceeded.
- `LoopDetector` – incrementally checks for excessive loop iterations and raises an error when the limit is surpassed.
- `average_time_monitor(threshold, window=5)` – decorator that logs a warning when the moving average execution time goes above the specified threshold.
- `retry_with_backoff(max_attempts=3, base_delay=0.1)` – decorator implementing retry with exponential backoff on exceptions.
