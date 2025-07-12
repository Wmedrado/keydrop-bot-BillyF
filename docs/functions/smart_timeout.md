# bot_keydrop.utils.smart_timeout

Decorator `smart_timeout(seconds, retries=3)` wraps an async function,
aborting with `asyncio.wait_for` and retrying automatically up to the
specified number of attempts.
