"""
Unit tests for API communication
"""
import unittest
from src.api.api_communicator import APICommunicator
from src.api.authentication import OAuth2Authenticator, JWTAuthenticator, APIKeyAuthenticator


class TestAPICommunicator(unittest.TestCase):
    """Test cases for APICommunicator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.communicator = APICommunicator(base_url="https://api.example.com")
    
    def test_communicator_creation(self):
        """Test communicator creation"""
        self.assertEqual(self.communicator.base_url, "https://api.example.com")
    
    def test_set_auth(self):
        """Test setting authentication"""
        self.communicator.set_auth("test-token")
        self.assertIsNotNone(self.communicator._auth_token)


class TestOAuth2Authenticator(unittest.TestCase):
    """Test cases for OAuth2Authenticator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.auth = OAuth2Authenticator(
            client_id="test-id",
            client_secret="test-secret",
            token_url="https://oauth.example.com/token"
        )
    
    def test_authenticator_creation(self):
        """Test authenticator creation"""
        self.assertEqual(self.auth.client_id, "test-id")


class TestJWTAuthenticator(unittest.TestCase):
    """Test cases for JWTAuthenticator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.auth = JWTAuthenticator(secret_key="test-secret")
    
    def test_authenticator_creation(self):
        """Test authenticator creation"""
        self.assertEqual(self.auth.secret_key, "test-secret")


class TestAPIKeyAuthenticator(unittest.TestCase):
    """Test cases for APIKeyAuthenticator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.auth = APIKeyAuthenticator(api_key="test-api-key")
    
    def test_authenticator_creation(self):
        """Test authenticator creation"""
        self.assertEqual(self.auth.api_key, "test-api-key")
    
    def test_get_access_token(self):
        """Test getting access token"""
        token = self.auth.get_access_token()
        self.assertEqual(token, "test-api-key")


if __name__ == '__main__':
    unittest.main()
