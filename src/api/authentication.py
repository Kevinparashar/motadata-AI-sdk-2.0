"""
Token-based authentication (OAuth2, JWT)
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import threading
from ..core.validators import validate_string
from ..core.exceptions import AuthenticationError, ValidationError
import logging


class Authenticator:
    """Base authenticator class"""
    
    def __init__(self):
        self._token = None
        self._token_expiry = None
        self._lock = threading.Lock()
    
    def get_access_token(self) -> str:
        """Get access token"""
        raise NotImplementedError("Subclasses must implement get_access_token")
    
    def is_token_valid(self) -> bool:
        """Check if current token is valid"""
        if not self._token:
            return False
        if self._token_expiry and datetime.now() >= self._token_expiry:
            return False
        return True


class OAuth2Authenticator(Authenticator):
    """OAuth2 authentication"""
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_url: str,
        scope: Optional[str] = None
    ):
        super().__init__()
        self.client_id = validate_string(client_id, "client_id", min_length=1)
        self.client_secret = validate_string(client_secret, "client_secret", min_length=1)
        self.token_url = validate_string(token_url, "token_url", min_length=1)
        if scope is not None:
            self.scope = validate_string(scope, "scope", min_length=1)
        else:
            self.scope = None
        self._logger = logging.getLogger(__name__)
    
    def get_access_token(self) -> str:
        """Get OAuth2 access token
        
        Returns:
            Access token string
        
        Raises:
            AuthenticationError: If token retrieval fails
        """
        with self._lock:
            if self.is_token_valid():
                return self._token
            
            try:
                # OAuth2 token request would go here
                # This is a placeholder implementation
                self._token = "oauth2_access_token"
                self._token_expiry = datetime.now() + timedelta(hours=1)
                return self._token
            except Exception as e:
                error_msg = f"Failed to get OAuth2 access token: {str(e)}"
                self._logger.error(error_msg, exc_info=True)
                raise AuthenticationError(error_msg, details={"token_url": self.token_url, "error": str(e)})
    
    def refresh_token(self) -> str:
        """Refresh the access token"""
        with self._lock:
            self._token = None
            self._token_expiry = None
            return self.get_access_token()


class JWTAuthenticator(Authenticator):
    """JWT token authentication"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        super().__init__()
        self.secret_key = validate_string(secret_key, "secret_key", min_length=1)
        self.algorithm = validate_string(algorithm, "algorithm", min_length=1, max_length=20)
        self._logger = logging.getLogger(__name__)
    
    def get_access_token(self) -> str:
        """Get JWT access token"""
        with self._lock:
            if self.is_token_valid():
                return self._token
            
            # JWT token generation would go here
            # This is a placeholder implementation
            self._token = "jwt_access_token"
            self._token_expiry = datetime.now() + timedelta(hours=1)
            return self._token
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode JWT token
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded token payload dictionary
        
        Raises:
            ValidationError: If token is invalid
            AuthenticationError: If token decoding fails
        """
        token = validate_string(token, "token", min_length=1)
        try:
            # JWT decoding logic would go here
            return {"sub": "user", "exp": datetime.now() + timedelta(hours=1)}
        except Exception as e:
            error_msg = f"Failed to decode JWT token: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise AuthenticationError(error_msg, details={"error": str(e)})


class APIKeyAuthenticator(Authenticator):
    """API key authentication"""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = validate_string(api_key, "api_key", min_length=1)
        self._token = api_key  # API key is the token itself
    
    def get_access_token(self) -> str:
        """Get API key"""
        return self.api_key
    
    def is_token_valid(self) -> bool:
        """API keys don't expire"""
        return bool(self.api_key)
