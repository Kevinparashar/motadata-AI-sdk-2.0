"""
Interface to interact with AI models
"""
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from ..core.data_structures import RequestModel, ResponseModel
from ..core.validators import validate_string, validate_list, validate_dict
from ..core.exceptions import ModelError, ValidationError, ConfigurationError
import logging


class AIGateway:
    """Main gateway interface for AI model interactions"""
    
    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        self.provider = validate_string(provider, "provider", min_length=1, max_length=50)
        if api_key is not None:
            self.api_key = validate_string(api_key, "api_key", min_length=1)
        else:
            self.api_key = None
        if config is not None:
            self.config = validate_dict(config, "config", required_keys=None)
        else:
            self.config = {}
        self._model_integration = None
        self._logger = logging.getLogger(__name__)
    
    def set_model_integration(self, integration):
        """Set the model integration handler
        
        Args:
            integration: Model integration instance
        
        Raises:
            ValidationError: If integration is invalid
        """
        if integration is None:
            raise ValidationError("integration cannot be None", field="integration")
        self._model_integration = integration
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a response from the AI model
        
        Args:
            prompt: Input prompt text
            model: Model name (optional)
            **kwargs: Additional generation parameters
        
        Returns:
            Generated response dictionary
        
        Raises:
            ValidationError: If prompt is invalid
            ModelError: If model integration not set or generation fails
        """
        prompt = validate_string(prompt, "prompt", min_length=1, max_length=100000)
        if model is not None:
            model = validate_string(model, "model", min_length=1, max_length=100)
        
        if not self._model_integration:
            raise ModelError("Model integration not set. Call set_model_integration() first.")
        
        try:
            return self._model_integration.generate(
                prompt=prompt,
                model=model,
                **kwargs
            )
        except Exception as e:
            error_msg = f"Failed to generate response: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelError(error_msg, details={"prompt_length": len(prompt), "model": model, "error": str(e)})
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Chat with the AI model
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Model name (optional)
            **kwargs: Additional chat parameters
        
        Returns:
            Chat response dictionary
        
        Raises:
            ValidationError: If messages are invalid
            ModelError: If model integration not set or chat fails
        """
        messages = validate_list(messages, "messages", min_items=1, allow_empty=False)
        for i, msg in enumerate(messages):
            msg = validate_dict(msg, f"messages[{i}]", required_keys=["role", "content"])
            validate_string(msg["role"], f"messages[{i}].role", min_length=1)
            validate_string(msg["content"], f"messages[{i}].content", min_length=1)
        
        if model is not None:
            model = validate_string(model, "model", min_length=1, max_length=100)
        
        if not self._model_integration:
            raise ModelError("Model integration not set. Call set_model_integration() first.")
        
        try:
            return self._model_integration.chat(
                messages=messages,
                model=model,
                **kwargs
            )
        except Exception as e:
            error_msg = f"Failed to chat with model: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelError(error_msg, details={"message_count": len(messages), "model": model, "error": str(e)})
    
    def embed(self, text: str, model: Optional[str] = None) -> List[float]:
        """Generate embeddings for text
        
        Args:
            text: Input text to embed
            model: Embedding model name (optional)
        
        Returns:
            List of embedding values
        
        Raises:
            ValidationError: If text is invalid
            ModelError: If model integration not set or embedding fails
        """
        text = validate_string(text, "text", min_length=1, max_length=100000)
        if model is not None:
            model = validate_string(model, "model", min_length=1, max_length=100)
        
        if not self._model_integration:
            raise ModelError("Model integration not set. Call set_model_integration() first.")
        
        try:
            return self._model_integration.embed(text=text, model=model)
        except Exception as e:
            error_msg = f"Failed to generate embeddings: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelError(error_msg, details={"text_length": len(text), "model": model, "error": str(e)})
    
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
