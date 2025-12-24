"""
Interface to interact with AI models
"""
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from ..core.data_structures import RequestModel, ResponseModel


class AIGateway:
    """Main gateway interface for AI model interactions"""
    
    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        self.provider = provider
        self.api_key = api_key
        self.config = config or {}
        self._model_integration = None
    
    def set_model_integration(self, integration):
        """Set the model integration handler"""
        self._model_integration = integration
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a response from the AI model"""
        if not self._model_integration:
            raise ValueError("Model integration not set")
        
        return self._model_integration.generate(
            prompt=prompt,
            model=model,
            **kwargs
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Chat with the AI model"""
        if not self._model_integration:
            raise ValueError("Model integration not set")
        
        return self._model_integration.chat(
            messages=messages,
            model=model,
            **kwargs
        )
    
    def embed(self, text: str, model: Optional[str] = None) -> List[float]:
        """Generate embeddings for text"""
        if not self._model_integration:
            raise ValueError("Model integration not set")
        
        return self._model_integration.embed(text=text, model=model)
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        if not self._model_integration:
            return []
        return self._model_integration.get_available_models()


class ModelProvider(ABC):
    """Abstract base class for model providers"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response"""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Chat with the model"""
        pass
    
    @abstractmethod
    def embed(self, text: str, **kwargs) -> List[float]:
        """Generate embeddings"""
        pass
