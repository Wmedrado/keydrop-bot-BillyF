"""Simple Discord OAuth utilities.

This module provides helpers for performing OAuth2 login
and assigning roles to a user in a guild. Environment variables are
used to configure the Discord application credentials and guild data.
"""

from __future__ import annotations

import os
import webbrowser
import http.server
import socketserver
from urllib.parse import urlencode, urlparse, parse_qs
from typing import Dict, Optional

import requests

CLIENT_ID = os.getenv("DISCORD_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI", "http://localhost:53245/callback")
SCOPES = ["identify", "email", "guilds.join"]

GUILD_ID = os.getenv("DISCORD_GUILD_ID", "")
VIP_ROLE_ID = os.getenv("DISCORD_VIP_ROLE_ID", "")
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")


class _CodeHandler(http.server.BaseHTTPRequestHandler):
    code: Optional[str] = None

    def do_GET(self) -> None:  # pragma: no cover - used during OAuth flow
        qs = parse_qs(urlparse(self.path).query)
        _CodeHandler.code = qs.get("code", [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Login concluido. Pode fechar esta janela.")

    def log_message(self, format: str, *args: object) -> None:  # pragma: no cover
        return


def _get_code(auth_url: str) -> str:
    with socketserver.TCPServer(("127.0.0.1", 0), _CodeHandler) as srv:
        port = srv.server_address[1]
        url = auth_url.replace("{REDIRECT}", f"http://127.0.0.1:{port}/callback")
        webbrowser.open(url)
        srv.handle_request()
        if not _CodeHandler.code:
            raise RuntimeError("OAuth cancelado")
        return _CodeHandler.code  # type: ignore


def oauth_login() -> Dict[str, str]:
    """Perform Discord OAuth2 login and return user info and token."""
    if not CLIENT_ID or not CLIENT_SECRET:
        raise RuntimeError("Discord OAuth nao configurado")
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": "{REDIRECT}",
        "response_type": "code",
        "scope": " ".join(SCOPES),
    }
    auth_url = f"https://discord.com/api/oauth2/authorize?{urlencode(params)}"
    code = _get_code(auth_url)
    token_resp = requests.post(
        "https://discord.com/api/oauth2/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    token_resp.raise_for_status()
    access_token = token_resp.json()["access_token"]
    user_resp = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    user_resp.raise_for_status()
    data = user_resp.json()
    return {
        "token": access_token,
        "id": data.get("id"),
        "username": data.get("username"),
        "email": data.get("email"),
    }


def add_vip_role(user_id: str, access_token: str) -> None:
    """Add the authenticated user to the guild and assign VIP role."""
    if not all([GUILD_ID, VIP_ROLE_ID, BOT_TOKEN]):
        raise RuntimeError("Discord guild configuration ausente")

    base = "https://discord.com/api"
    headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
    join_resp = requests.put(
        f"{base}/guilds/{GUILD_ID}/members/{user_id}",
        headers=headers,
        json={"access_token": access_token},
        timeout=10,
    )
    if join_resp.status_code not in (200, 201, 204):  # pragma: no cover - network
        raise RuntimeError(f"Falha ao adicionar membro: {join_resp.text}")
    role_resp = requests.put(
        f"{base}/guilds/{GUILD_ID}/members/{user_id}/roles/{VIP_ROLE_ID}",
        headers=headers,
        timeout=10,
    )
    if role_resp.status_code not in (204, 201):  # pragma: no cover - network
        raise RuntimeError(f"Falha ao aplicar cargo: {role_resp.text}")

