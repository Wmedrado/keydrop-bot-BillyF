import os
import json
import asyncio
from typing import Optional

import logging
import requests

from discord_integration import configure_discord_webhook, send_discord_notification


GITHUB_API_RELEASE_URL = "https://api.github.com/repos/{repo}/releases/latest"
STATE_FILE = os.path.join(os.path.dirname(__file__), "release_state.json")

logger = logging.getLogger(__name__)


def get_latest_release(repo: str, token: Optional[str] = None) -> dict:
    """Fetch latest release info from GitHub."""
    url = GITHUB_API_RELEASE_URL.format(repo=repo)
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logger.warning("Erro ao buscar versão mais recente: %s", e)
        return {"error": "Erro ao buscar atualização"}
    except ValueError as e:
        logger.warning("Resposta malformada: %s", e)
        return {"error": "Resposta malformada"}
    return data


def load_last_tag() -> Optional[str]:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("tag_name")
        except Exception:
            return None
    return None


def save_last_tag(tag: str) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"tag_name": tag}, f)


def format_release_news(release: dict) -> str:
    name = release.get("name") or release.get("tag_name")
    body = release.get("body", "Sem notas de release.").strip()
    return f"**{name}**\n\n{body}"


async def notify_discord(release: dict, webhook_url: Optional[str]) -> None:
    if webhook_url:
        configure_discord_webhook(webhook_url)
    description = format_release_news(release)
    fields = [
        {"name": "Vers\u00e3o", "value": release.get("tag_name", "N/A"), "inline": True},
        {"name": "Data", "value": release.get("published_at", "N/A"), "inline": True},
        {"name": "Link", "value": release.get("html_url", ""), "inline": False},
    ]
    await send_discord_notification(
        title="\U0001F4F0 Nova Release Dispon\u00edvel",
        description=description,
        notification_type="system",
        fields=fields,
    )


async def main() -> None:
    repo = os.getenv("GITHUB_REPO", "Wmedrado/keydrop-bot-v3")
    token = os.getenv("GITHUB_TOKEN")
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    release = get_latest_release(repo, token)
    current_tag = release.get("tag_name")
    last_tag = load_last_tag()

    if current_tag != last_tag:
        await notify_discord(release, webhook_url)
        save_last_tag(current_tag)
    else:
        print("No new release detected.")


if __name__ == "__main__":
    asyncio.run(main())
