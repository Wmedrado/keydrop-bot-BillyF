import os
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")


def send_telegram(msg: str) -> None:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=5)
    except Exception as exc:
        print("Telegram notification failed", exc)


def send_discord(msg: str) -> None:
    if not DISCORD_WEBHOOK_URL:
        return
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg}, timeout=5)
    except Exception as exc:
        print("Discord notification failed", exc)


def main(status: str, details: str = "") -> int:
    message = f"Build status: {status}\n{details}"
    send_telegram(message)
    send_discord(message)
    return 0


if __name__ == "__main__":
    import sys

    st = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    detail = sys.argv[2] if len(sys.argv) > 2 else ""
    raise SystemExit(main(st, detail))
