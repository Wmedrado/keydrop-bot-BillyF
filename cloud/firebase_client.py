"""Firebase integration module for Keydrop Bot."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional, Any, List, Dict
from datetime import datetime

try:
    import firebase_admin
    from firebase_admin import credentials, initialize_app, storage, db

    sys.modules[__name__ + ".storage"] = storage
    sys.modules[__name__ + ".db"] = db
except ImportError:  # pragma: no cover - optional dependency
    from types import SimpleNamespace

    firebase_admin = None
    credentials = SimpleNamespace(Certificate=lambda *a, **k: None)
    initialize_app = lambda *a, **k: None
    storage = SimpleNamespace(bucket=lambda *a, **k: None)
    db = SimpleNamespace(reference=lambda *a, **k: None)

sys.modules[__name__ + ".storage"] = storage
sys.modules[__name__ + ".db"] = db


logger = logging.getLogger(__name__)

# Global variable to hold the initialized Firebase app
from typing import Any

_firebase_app: Optional[Any] = None

# Constants for project configuration
_DATABASE_URL = "https://keydrop-bot-ab111-default-rtdb.firebaseio.com/"
_STORAGE_BUCKET = "keydrop-bot-ab111.appspot.com"


def initialize_firebase() -> Any:
    """Initialize Firebase if not already done."""
    global _firebase_app

    if firebase_admin is None:
        raise ImportError("firebase_admin is required for Firebase integration")

    if _firebase_app:
        return _firebase_app

    cred_path = Path(__file__).resolve().parents[1] / "firebase_credentials.json"
    if not cred_path.exists():
        raise FileNotFoundError(f"Firebase credentials not found at {cred_path}.")

    cred = credentials.Certificate(str(cred_path))
    _firebase_app = initialize_app(
        cred,
        {
            "databaseURL": _DATABASE_URL,
            "storageBucket": _STORAGE_BUCKET,
        },
    )
    logger.info("Firebase app initialized")
    return _firebase_app


def salvar_perfil(
    user_id: str,
    nome: str,
    lucro_total: float,
    tempo_total_min: int,
    bots_ativos_max: int,
) -> None:
    """Save or update a user's profile and ranking."""
    initialize_firebase()

    ref = db.reference(f"users/{user_id}")
    existing = ref.get() or {}
    data = {
        "nome": nome,
        "lucro_total": float(lucro_total),
        "tempo_total_min": int(tempo_total_min),
        "bots_ativos_max": int(bots_ativos_max),
    }
    if "foto_url" in existing:
        data["foto_url"] = existing["foto_url"]

    ref.update(data)
    atualizar_ranking(user_id, lucro_total)
    logger.debug("Perfil salvo para %s", user_id)


def atualizar_ranking(user_id: str, lucro_total: float) -> None:
    """Update the global ranking with the user's total profit."""
    initialize_firebase()
    ranking_ref = db.reference("rankings/top_lucro")
    ranking_ref.child(str(user_id)).set(float(lucro_total))
    logger.debug("Ranking atualizado para %s: %s", user_id, lucro_total)


def upload_foto_perfil(user_id: str, caminho_imagem: str) -> str:
    """Upload a profile photo and store its URL."""
    initialize_firebase()
    caminho = Path(caminho_imagem)
    if not caminho.exists():
        logger.error("Imagem de perfil nao encontrada: %s", caminho)
        raise FileNotFoundError(f"Profile image not found: {caminho}")
    try:
        bucket = storage.bucket()
        blob = bucket.blob(f"avatars/{user_id}.jpg")
        blob.upload_from_filename(str(caminho))
        blob.make_public()
        foto_url = blob.public_url

        user_ref = db.reference(f"users/{user_id}")
        user_ref.update({"foto_url": foto_url})
        logger.debug("Foto de perfil enviada para %s", foto_url)
        return foto_url
    except FileNotFoundError:
        raise
    except Exception as exc:  # pragma: no cover - network errors
        logger.exception("Falha ao enviar foto de perfil: %s", exc)
        raise RuntimeError("Falha ao enviar foto de perfil") from exc


def registrar_compra(user_id: str, itens: List[Dict[str, Any]]) -> None:
    """Persist a purchase attempt in the realtime database."""
    initialize_firebase()
    compra_ref = db.reference(f"compras/{user_id}")
    dados = {
        "itens": itens,
        "timestamp": int(datetime.utcnow().timestamp()),
    }
    compra_ref.push(dados)
    logger.debug("Compra registrada para %s: %s", user_id, dados)


def salvar_discord_info(user_id: str, info: Dict[str, Any]) -> None:
    """Persist Discord-related information for a user."""
    initialize_firebase()
    ref = db.reference(f"users/{user_id}/discord")
    ref.update(info)
    logger.debug("Discord info salvo para %s: %s", user_id, info)


def registrar_log_suspeito(
    user_id: str, hwid: str, recurso: str, mensagem: str
) -> None:
    """Save a suspicious activity log entry."""
    initialize_firebase()
    log_ref = db.reference("logs_suspeitos")
    dados = {
        "user_id": user_id,
        "hwid": hwid,
        "recurso": recurso,
        "mensagem": mensagem,
        "timestamp": int(datetime.utcnow().timestamp()),
    }
    log_ref.push(dados)
    logger.warning("Registro suspeito: %s", dados)
