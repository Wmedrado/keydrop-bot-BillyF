# -*- coding: utf-8 -*-
"""Password reset utilities."""
from __future__ import annotations

import hashlib
import json
import os
import smtplib
from email.message import EmailMessage
from typing import Optional
from uuid import uuid4
from datetime import datetime, timedelta

try:
    from firebase_admin import db, auth
except Exception:  # pragma: no cover - optional dependency
    db = auth = None  # type: ignore

from dotenv import load_dotenv
from cloud.firebase_client import initialize_firebase



load_dotenv()

_SMTP_USER = os.getenv("SMTP_USER")
_SMTP_PASS = os.getenv("SMTP_PASS")
_SMTP_HOST = os.getenv("SMTP_HOST")
_SMTP_PORT_ENV = os.getenv("SMTP_PORT")
_SMTP_PORT = int(_SMTP_PORT_ENV) if _SMTP_PORT_ENV else 0

if not all([_SMTP_USER, _SMTP_PASS, _SMTP_HOST, _SMTP_PORT]):
    try:
        with open("config.json", "r", encoding="utf-8") as cfg_file:
            cfg = json.load(cfg_file)
        _SMTP_USER = _SMTP_USER or cfg.get("SMTP_USER")
        _SMTP_PASS = _SMTP_PASS or cfg.get("SMTP_PASS")
        _SMTP_HOST = _SMTP_HOST or cfg.get("SMTP_HOST")
        _SMTP_PORT = _SMTP_PORT or int(cfg.get("SMTP_PORT", 0))
    except FileNotFoundError:
        pass


def _save_token(user_id: str, token: str, expires_at: datetime) -> None:
    """Persist the reset token in Firebase."""
    initialize_firebase()
    if db is None:
        raise ImportError("firebase_admin is required for database operations")
    ref = db.reference(f"reset_tokens/{user_id}")
    ref.set({
        "token": token,
        "timestamp": int(datetime.utcnow().timestamp()),
        "expires_at": int(expires_at.timestamp()),
    })


def _send_email(email: str, token: str) -> None:
    """Send password reset email using configured SMTP credentials."""
    if not all([_SMTP_USER, _SMTP_PASS, _SMTP_HOST, _SMTP_PORT]):
        raise RuntimeError(
            "❗ Arquivo de configuração SMTP não encontrado. Configure \"config.json\" com suas credenciais."
        )
    link = f"https://meubot.com/reset?token={token}"
    body = (
        "Olá, você solicitou a redefinição de sua senha.\n\n"
        f"Clique no link abaixo para criar uma nova senha:\n{link}\n\n"
        "Este link expira em 15 minutos.\nSe não foi você quem solicitou, ignore este e-mail."
    )
    msg = EmailMessage()
    msg["Subject"] = "🔐 Redefinição de Senha - Bot Oficial"
    msg["From"] = _SMTP_USER
    msg["To"] = email
    msg.set_content(body)
    with smtplib.SMTP_SSL(_SMTP_HOST, _SMTP_PORT) as smtp:
        smtp.login(_SMTP_USER, _SMTP_PASS)
        smtp.send_message(msg)


def request_reset(email: str) -> str:
    """Generate reset token for the given email and send instructions."""
    if auth is None:
        raise ImportError("firebase_admin is required for auth operations")
    initialize_firebase()
    try:
        user = auth.get_user_by_email(email)
    except Exception as exc:  # fallback to generic not-found error
        raise ValueError("E-mail não encontrado") from exc
    token_raw = f"{uuid4()}-{datetime.utcnow().timestamp()}".encode()
    token = hashlib.sha256(token_raw).hexdigest()
    expires_at = datetime.utcnow() + timedelta(minutes=15)
    _save_token(user.uid, token, expires_at)
    _send_email(email, token)
    return token


def verify_token(token: str) -> Optional[str]:
    """Return user_id if token is valid and not expired."""
    initialize_firebase()
    if db is None:
        raise ImportError("firebase_admin is required for database operations")
    ref = db.reference("reset_tokens")
    data = ref.get() or {}
    now = int(datetime.utcnow().timestamp())
    for uid, info in data.items():
        if info.get("token") == token and now < int(info.get("expires_at", 0)):
            return uid
    return None


def reset_password(token: str, new_password: str) -> None:
    """Validate token and update user's password."""
    if auth is None:
        raise ImportError("firebase_admin is required for auth operations")
    uid = verify_token(token)
    if not uid:
        raise ValueError("Token inválido ou expirado")
    auth.update_user(uid, password=new_password)
    initialize_firebase()
    if db is None:
        raise ImportError("firebase_admin is required for database operations")
    db.reference(f"reset_tokens/{uid}").delete()
