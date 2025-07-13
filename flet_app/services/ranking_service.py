import httpx
import logging
from typing import Dict, Any, Optional
from .token_service import TokenService

class RankingService:
    BASE_URL = "http://localhost:8000"
    logger = logging.getLogger(__name__)

    @classmethod
    async def get_ranking(cls) -> Dict[str, Any]:
        token = TokenService.get_token()
        if not token:
            return {"error": "Token de autenticação não encontrado"}
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{cls.BASE_URL}/ranking", headers=headers, timeout=10.0)
                if response.status_code == 200:
                    return {"ranking": response.json()}
                elif response.status_code == 401:
                    TokenService.clear_token()
                    return {"error": "Sessão expirada. Faça login novamente."}
                else:
                    return {"error": f"Erro ao buscar ranking: {response.status_code}"}
            except httpx.RequestError as e:
                cls.logger.error(f"Ranking request error: {e}")
                return {"error": "Erro de conexão. Verifique sua internet."}
            except Exception as e:
                cls.logger.exception("Unexpected ranking fetch error")
                return {"error": "Erro inesperado ao buscar ranking"}
