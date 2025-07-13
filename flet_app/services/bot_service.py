import httpx
import asyncio
import logging
from typing import Dict, List, Any, Optional
from .token_service import TokenService

class BotService:
    """
    Service for managing and retrieving bot information
    """
    BASE_URL = "http://localhost:8000"  # Configurable backend URL
    logger = logging.getLogger(__name__)

    @classmethod
    async def get_bots(cls) -> Dict[str, Any]:
        """
        Fetch all bots associated with the user
        
        Returns:
            Dict containing bot data or error details
        """
        # Retrieve stored token
        token = TokenService.get_token()
        
        if not token:
            return {"error": "Token de autenticação não encontrado"}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{cls.BASE_URL}/bots",
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return {"bots": response.json()}
                elif response.status_code == 401:
                    # Token might be expired
                    TokenService.clear_token()
                    return {"error": "Sessão expirada. Faça login novamente."}
                else:
                    return {"error": f"Erro ao buscar bots: {response.status_code}"}
            
            except httpx.RequestError as e:
                cls.logger.error(f"Bots request error: {e}")
                return {"error": "Erro de conexão. Verifique sua internet."}
            except Exception as e:
                cls.logger.exception("Unexpected bots fetch error")
                return {"error": "Erro inesperado ao buscar bots"}

    @classmethod
    async def start_bot(cls, bot_id: str) -> Dict[str, Any]:
        """
        Start a specific bot
        
        Args:
            bot_id (str): Unique identifier for the bot
        
        Returns:
            Dict containing start result or error details
        """
        token = TokenService.get_token()
        
        if not token:
            return {"error": "Token de autenticação não encontrado"}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{cls.BASE_URL}/bots/{bot_id}/start",
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return {"success": True, "message": "Bot iniciado com sucesso"}
                elif response.status_code == 401:
                    TokenService.clear_token()
                    return {"error": "Sessão expirada. Faça login novamente."}
                else:
                    return {"error": f"Erro ao iniciar bot: {response.status_code}"}
            
            except httpx.RequestError as e:
                cls.logger.error(f"Start bot request error: {e}")
                return {"error": "Erro de conexão. Verifique sua internet."}
            except Exception as e:
                cls.logger.exception("Unexpected bot start error")
                return {"error": "Erro inesperado ao iniciar bot"}

    @classmethod
    async def stop_bot(cls, bot_id: str) -> Dict[str, Any]:
        """
        Stop a specific bot
        
        Args:
            bot_id (str): Unique identifier for the bot
        
        Returns:
            Dict containing stop result or error details
        """
        token = TokenService.get_token()
        
        if not token:
            return {"error": "Token de autenticação não encontrado"}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{cls.BASE_URL}/bots/{bot_id}/stop",
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return {"success": True, "message": "Bot parado com sucesso"}
                elif response.status_code == 401:
                    TokenService.clear_token()
                    return {"error": "Sessão expirada. Faça login novamente."}
                else:
                    return {"error": f"Erro ao parar bot: {response.status_code}"}
            
            except httpx.RequestError as e:
                cls.logger.error(f"Stop bot request error: {e}")
                return {"error": "Erro de conexão. Verifique sua internet."}
            except Exception as e:
                cls.logger.exception("Unexpected bot stop error")
                return {"error": "Erro inesperado ao parar bot"}
