import os
import json
import requests
from datetime import datetime

WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

def main() -> int:
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        print("No event data")
        return 1
    with open(event_path, "r", encoding="utf-8") as fh:
        event = json.load(fh)

    pr = event.get("pull_request", {})
    if not pr.get("merged"):
        print("PR not merged")
        return 0

    base = pr.get("base", {}).get("ref")
    if base not in {"main", "clean-main", "homologacao"}:
        print("Branch not monitored")
        return 0

    author = pr.get("merged_by", {}).get("login") or pr.get("user", {}).get("login")
    title = pr.get("title")
    head = pr.get("head", {}).get("ref")
    url = pr.get("html_url")
    merged_at = pr.get("merged_at") or datetime.utcnow().isoformat()

    if WEBHOOK:
        msg = (
            "\u2705 Novo Pull Request Integrado!\n\n"
            f"\ud83d\udc64 Aprovado e mesclado por: {author}  \n"
            f"\ud83d\udd04 Branch: {head} → {base}  \n"
            f"\ud83d\udccd Título: {title}  \n"
            f"\ud83d\udcc5 Data: {merged_at}  \n"
            f"\ud83d\udd0d Link: {url}  \n"
        )
        try:
            requests.post(WEBHOOK, json={"content": msg}, timeout=10)
        except Exception as exc:
            print("Failed to notify", exc)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
