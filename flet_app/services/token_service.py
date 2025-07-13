import os
import json
from typing import Optional

class TokenService:
    """
    Manages authentication token storage and retrieval
    Provides secure token management with local storage
    """
    TOKEN_FILE = os.path.join(os.path.expanduser("~"), ".keydrop_token.json")

    @classmethod
    def save_token(cls, token: str) -> None:
        """
        Save authentication token securely
        
        Args:
            token (str): Authentication token to save
        """
        try:
            with open(cls.TOKEN_FILE, 'w') as f:
                json.dump({"token": token}, f)
            os.chmod(cls.TOKEN_FILE, 0o600)  # Restrict file permissions
        except Exception as e:
            print(f"Error saving token: {e}")

    @classmethod
    def get_token(cls) -> Optional[str]:
        """
        Retrieve stored authentication token
        
        Returns:
            Optional[str]: Stored token or None if not found
        """
        try:
            if not os.path.exists(cls.TOKEN_FILE):
                return None
            
            with open(cls.TOKEN_FILE, 'r') as f:
                data = json.load(f)
                return data.get('token')
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    @classmethod
    def clear_token(cls) -> None:
        """
        Remove stored authentication token
        """
        try:
            if os.path.exists(cls.TOKEN_FILE):
                os.unlink(cls.TOKEN_FILE)
        except Exception as e:
            print(f"Error clearing token: {e}")
