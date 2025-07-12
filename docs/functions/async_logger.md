# bot_keydrop.utils.async_logger

Provides `AsyncRemoteHandler` which sends logs to an HTTP endpoint using a background thread.
If the request fails, the log message is appended to `logs/offline.log` for later flush via `flush_offline()`.
