import httpx
import asyncio
import logging
from typing import Dict, Any, Optional
from .token_service import TokenService

class AuthService:
    """
    Comprehensive authentication service with robust error handling
    """
    BASE_URL = "http://localhost:8000"  # Configurable backend URL
    logger = logging.getLogger(__name__)
    
    @classmethod
    async def login(cls, email: str, password: str) -> Dict[str, Any]:
        """
        Perform login with comprehensive error handling
        
        Args:
            email (str): User's email
            password (str): User's password
        
        Returns:
            Dict containing login result or error details
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{cls.BASE_URL}/login", 
                    json={
                        "email": email, 
                        "senha": password
                    },
                    timeout=10.0  # Add request timeout
                )
                
                # Handle different HTTP status codes
                if response.status_code == 200:
                    result = response.json()
                    # Save token if login successful
                    if result.get('token'):
                        TokenService.save_token(result['token'])
                    return result
                elif response.status_code == 401:
                    return {"error": "Credenciais inválidas"}
                elif response.status_code == 404:
                    return {"error": "Usuário não encontrado"}
                else:
                    return {"error": f"Erro desconhecido: {response.status_code}"}
            
            except httpx.RequestError as e:
                cls.logger.error(f"Login request error: {e}")
                return {"error": "Erro de conexão. Verifique sua internet."}
            except Exception as e:
                cls.logger.exception("Unexpected login error")
                return {"error": "Erro inesperado durante login"}
    
    @classmethod
    async def register(cls, email: str, password: str, confirm_password: str) -> Dict[str, Any]:
        """
        Perform user registration with input validation
        
        Args:
            email (str): User's email
            password (str): User's password
            confirm_password (str): Password confirmation
        
        Returns:
            Dict containing registration result or error details
        """
        # Input validation
        if not email or not email.strip():
            return {"error": "Email inválido"}
        
        if not password or len(password) < 6:
            return {"error": "Senha deve ter no mínimo 6 caracteres"}
        
        if password != confirm_password:
            return {"error": "Senhas não coincidem"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{cls.BASE_URL}/register", 
                    json={
                        "email": email, 
                        "senha": password
                    },
                    timeout=10.0
                )
                
                result = response.json()
                return result
            
            except httpx.RequestError as e:
                cls.logger.error(f"Registration request error: {e}")
                return {"error": "Erro de conexão. Verifique sua internet."}
            except Exception as e:
                cls.logger.exception("Unexpected registration error")
                return {"error": "Erro inesperado durante registro"}
    
    @classmethod
    async def get_profile(cls, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch user profile with comprehensive token management
        
        Args:
            token (Optional[str]): Authentication token
        
        Returns:
            Dict containing profile data or error details
        """
        # Use stored token if not provided
        if not token:
            token = TokenService.get_token()
        
        if not token:
            return {"error": "Token de autenticação não encontrado"}
        
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{cls.BASE_URL}/profile",
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    # Token might be expired
                    TokenService.clear_token()
                    return {"error": "Sessão expirada. Faça login novamente."}
                else:
                    return {"error": f"Erro ao buscar perfil: {response.status_code}"}
            
            except httpx.RequestError as e:
                cls.logger.error(f"Profile request error: {e}")
                return {"error": "Erro de conexão. Verifique sua internet."}
            except Exception as e:
                cls.logger.exception("Unexpected profile fetch error")
                return {"error": "Erro inesperado ao buscar perfil"}
