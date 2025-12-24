"""
Unit tests for AI Gateway integration
"""
import unittest
from src.ai_gateway.gateway import AIGateway
from src.ai_gateway.prompt_manager import PromptManager, PromptTemplate


class TestAIGateway(unittest.TestCase):
    """Test cases for AIGateway"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.gateway = AIGateway(provider="openai", api_key="test-key")
    
    def test_gateway_creation(self):
        """Test gateway creation"""
        self.assertEqual(self.gateway.provider, "openai")
        self.assertEqual(self.gateway.api_key, "test-key")


class TestPromptManager(unittest.TestCase):
    """Test cases for PromptManager"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.manager = PromptManager()
    
    def test_prompt_manager_creation(self):
        """Test prompt manager creation"""
        self.assertIsNotNone(self.manager)
    
    def test_get_template(self):
        """Test getting a template"""
        template = self.manager.get_template("classification")
        self.assertIsNotNone(template)
    
    def test_list_templates(self):
        """Test listing templates"""
        templates = self.manager.list_templates()
        self.assertIsInstance(templates, list)
        self.assertGreater(len(templates), 0)


if __name__ == '__main__':
    unittest.main()
