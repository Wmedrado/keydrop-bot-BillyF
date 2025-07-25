# -*- coding: utf-8 -*-
"""Password reset utilities."""
from __future__ import annotations

import hashlib
import json
import os
import smtplib
from email.message import EmailMessage
from typing import Optional
from datetime import datetime, timedelta
import secrets
from dotenv import load_dotenv
from cloud.firebase_client import initialize_firebase

try:
    from firebase_admin import db, auth
except Exception:  # pragma: no cover - optional dependency
    db = auth = None  # type: ignore


def _ensure_firebase_admin() -> None:
    """Load firebase_admin modules lazily if available."""
    global auth, db
    if auth is None or db is None:
        try:
            from firebase_admin import db as fb_db, auth as fb_auth
        except Exception as exc:  # pragma: no cover - optional dependency
            raise ImportError(
                "firebase_admin is required for auth operations"
            ) from exc  # noqa: E501
        if auth is None:
            auth = fb_auth
        if db is None:
            db = fb_db


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
            "❗ Arquivo de configuração SMTP não encontrado. "
            'Configure "config.json" com suas credenciais.'
        )
    link = f"https://appdomain.com/reset-password?token={token}"
    text_body = (
        "Olá, você solicitou a redefinição de sua senha.\n\n"
        f"Acesse o link a seguir para criar uma nova senha: {link}\n\n"
        "Este link expira em 1 hora.\n"
        "Se você não solicitou, apenas ignore este e-mail."
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
    _ensure_firebase_admin()  # ensure auth module
    try:
        initialize_firebase()
    except FileNotFoundError:
        pass
    try:
        user = auth.get_user_by_email(email)
    except Exception as exc:  # fallback to generic not-found error
        raise ValueError("E-mail não encontrado") from exc
    token = secrets.token_urlsafe(32)
    hashed = hashlib.sha256(token.encode()).hexdigest()  # noqa: E501
    expires_at = datetime.utcnow() + timedelta(hours=1)
    _save_token(user.uid, hashed, expires_at)
    _send_email(email, token)
    return token


def verify_token(token: str) -> Optional[str]:
    """Return user_id if token is valid and not expired."""
    try:
        initialize_firebase()
    except FileNotFoundError:
        pass
    _ensure_firebase_admin()  # load db module
    ref = db.reference("reset_tokens")
    data = ref.get() or {}
    now = int(datetime.utcnow().timestamp())
    hashed = hashlib.sha256(token.encode()).hexdigest()
    for uid, info in data.items():
        if info.get("token") == hashed and now < int(
            info.get("expires_at", 0)
        ):  # noqa: E501
            return uid
    return None


def reset_password(token: str, new_password: str) -> None:
    """Validate token and update user's password."""
    _ensure_firebase_admin()  # reload admin modules
    uid = verify_token(token)
    if not uid:
        raise ValueError("Token inválido ou expirado")
    auth.update_user(uid, password=new_password)
    try:
        initialize_firebase()
    except FileNotFoundError:
        pass
    if db is None:
        raise ImportError("firebase_admin is required for database operations")
    db.reference(f"reset_tokens/{uid}").delete()
