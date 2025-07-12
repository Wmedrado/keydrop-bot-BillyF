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
import secrets

import types

try:
    from firebase_admin import db, auth
except Exception:  # pragma: no cover - optional dependency
    db = types.SimpleNamespace(reference=lambda *a, **k: None)
    auth = types.SimpleNamespace(
        get_user_by_email=lambda *a, **k: None,
        update_user=lambda *a, **k: None,
    )

from dotenv import load_dotenv
import importlib


def _fb():
    return importlib.import_module("cloud.firebase_client")


def _admin() -> types.ModuleType:
    try:
        return importlib.import_module("firebase_admin")
    except Exception:  # pragma: no cover - optional dependency
        return types.SimpleNamespace(auth=None, db=None)


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
    _fb().initialize_firebase()
    admin = _admin()
    db_obj = admin.db or db
    if db_obj is None:
        raise ImportError("firebase_admin is required for database operations")
    ref = db_obj.reference(f"reset_tokens/{user_id}")
    ref.set(
        {
            "token": token,
            "timestamp": int(datetime.utcnow().timestamp()),
            "expires_at": int(expires_at.timestamp()),
        }
    )


def _send_email(email: str, token: str) -> None:
    """Send password reset email using configured SMTP credentials."""
    if not all([_SMTP_USER, _SMTP_PASS, _SMTP_HOST, _SMTP_PORT]):
        raise RuntimeError(
            '❗ Arquivo de configuração SMTP não encontrado. Configure "config.json" com suas credenciais.'
        )
    link = f"https://appdomain.com/reset-password?token={token}"
    text_body = (
        "Olá, você solicitou a redefinição de sua senha.\n\n"
        f"Acesse o link a seguir para criar uma nova senha: {link}\n\n"
        "Este link expira em 1 hora.\nSe você não solicitou, apenas ignore este e-mail."
    )
    html_body = f"""
    <html>
        <body style='font-family: Arial, sans-serif;'>
            <p>Olá,</p>
            <p>Você solicitou a redefinição de sua senha.</p>
            <p><a href='{link}'>Clique aqui para criar uma nova senha</a></p>
            <p>O link é válido por 1 hora.</p>
            <p>Se não foi você quem solicitou, ignore este e-mail.</p>
        </body>
    </html>
    """
    msg = EmailMessage()
    msg["Subject"] = "🔐 Recuperação de senha"
    msg["From"] = _SMTP_USER
    msg["To"] = email
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")
    with smtplib.SMTP(_SMTP_HOST, _SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(_SMTP_USER, _SMTP_PASS)
        smtp.send_message(msg)


def request_reset(email: str) -> str:
    """Generate reset token for the given email and send instructions."""
    admin = _admin()
    if admin.auth is None:
        raise ImportError("firebase_admin is required for auth operations")
    _fb().initialize_firebase()
    try:
        user = admin.auth.get_user_by_email(email)
    except Exception as exc:  # fallback to generic not-found error
        raise ValueError("E-mail não encontrado") from exc
    token = secrets.token_urlsafe(32)
    hashed = hashlib.sha256(token.encode()).hexdigest()
    expires_at = datetime.utcnow() + timedelta(hours=1)
    _save_token(user.uid, hashed, expires_at)
    _send_email(email, token)
    return token


def verify_token(token: str) -> Optional[str]:
    """Return user_id if token is valid and not expired."""
    _fb().initialize_firebase()
    admin = _admin()
    db_obj = admin.db or db
    if db_obj is None:
        raise ImportError("firebase_admin is required for database operations")
    ref = db_obj.reference("reset_tokens")
    data = ref.get() or {}
    now = int(datetime.utcnow().timestamp())
    hashed = hashlib.sha256(token.encode()).hexdigest()
    for uid, info in data.items():
        if info.get("token") == hashed and now < int(info.get("expires_at", 0)):
            return uid
    return None


def reset_password(token: str, new_password: str) -> None:
    """Validate token and update user's password."""
    admin = _admin()
    if admin.auth is None:
        raise ImportError("firebase_admin is required for auth operations")
    uid = verify_token(token)
    if not uid:
        raise ValueError("Token inválido ou expirado")
    admin.auth.update_user(uid, password=new_password)
    _fb().initialize_firebase()
    db_obj = admin.db or db
    if db_obj is None:
        raise ImportError("firebase_admin is required for database operations")
    db_obj.reference(f"reset_tokens/{uid}").delete()
