import httpx
import logging
from typing import Dict, Any
from .token_service import TokenService

class ManagerService:
    BASE_URL = "http://localhost:8000"
    logger = logging.getLogger(__name__)

    @classmethod
    async def get_config(cls) -> Dict[str, Any]:
        token = TokenService.get_token()
        if not token:
            return {"error": "Token de autenticação não encontrado"}
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{cls.BASE_URL}/config", headers=headers, timeout=10.0)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    TokenService.clear_token()
                    return {"error": "Sessão expirada. Faça login novamente."}
                else:
                    return {"error": f"Erro ao buscar configurações: {response.status_code}"}
            except httpx.RequestError as e:
                cls.logger.error(f"Config request error: {e}")
                return {"error": "Erro de conexão. Verifique sua internet."}
            except Exception as e:
                cls.logger.exception("Unexpected config error")
                return {"error": "Erro inesperado ao buscar configurações"}

    @classmethod
    async def update_config(cls, config: dict) -> Dict[str, Any]:
        token = TokenService.get_token()
        if not token:
            return {"error": "Token de autenticação não encontrado"}
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{cls.BASE_URL}/config/update", json=config, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    TokenService.clear_token()
                    return {"error": "Sessão expirada. Faça login novamente."}
                else:
                    return {"error": f"Erro ao salvar configurações: {response.status_code}"}
            except httpx.RequestError as e:
                cls.logger.error(f"Update config request error: {e}")
                return {"error": "Erro de conexão. Verifique sua internet."}
            except Exception as e:
                cls.logger.exception("Unexpected update config error")
                return {"error": "Erro inesperado ao salvar configurações"}
