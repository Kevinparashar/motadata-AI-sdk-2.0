"""
Integration with LiteLLM for AI model access
"""
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from .gateway import ModelProvider
from ..core.validators import validate_string, validate_list, validate_dict
from ..core.exceptions import ModelError, ValidationError, ConfigurationError
import logging

try:
    from litellm import completion, embedding, get_model_list
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    logging.warning("LiteLLM not installed. Install with: pip install litellm")


class LiteLLMProvider(ModelProvider):
    """LiteLLM provider integration - unified interface for multiple AI models"""
    
    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None, **kwargs):
        if not LITELLM_AVAILABLE:
            raise ConfigurationError(
                "LiteLLM is not installed. Install with: pip install litellm",
                details={"package": "litellm"}
            )
        if api_key is not None:
            self.api_key = validate_string(api_key, "api_key", min_length=1)
        else:
            self.api_key = None
        if api_base is not None:
            self.api_base = validate_string(api_base, "api_base", min_length=1)
        else:
            self.api_base = None
        self.config = kwargs
        self._logger = logging.getLogger(__name__)
    
    def generate(self, prompt: str, model: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Generate a response using LiteLLM
        
        Args:
            prompt: Input prompt text
            model: Model name (e.g., 'gpt-4', 'claude-3-opus', 'gemini-pro')
            **kwargs: Additional generation parameters
        
        Returns:
            Generated response dictionary
        
        Raises:
            ModelError: If generation fails
        """
        prompt = validate_string(prompt, "prompt", min_length=1)
        if model is not None:
            model = validate_string(model, "model", min_length=1)
        
        try:
            response = completion(
                model=model or "gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                api_key=self.api_key,
                api_base=self.api_base,
                **{**self.config, **kwargs}
            )
            
            return {
                "text": response.choices[0].message.content,
                "model": response.model,
                "provider": "litellm",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if hasattr(response.usage, 'prompt_tokens') else 0,
                    "completion_tokens": response.usage.completion_tokens if hasattr(response.usage, 'completion_tokens') else 0,
                    "total_tokens": response.usage.total_tokens if hasattr(response.usage, 'total_tokens') else 0
                }
            }
        except Exception as e:
            error_msg = f"LiteLLM generation failed: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelError(error_msg, details={"model": model, "error": str(e)})
    
    def chat(self, messages: List[Dict[str, str]], model: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Chat with AI model using LiteLLM
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model name
            **kwargs: Additional chat parameters
        
        Returns:
            Chat response dictionary
        
        Raises:
            ModelError: If chat fails
        """
        messages = validate_list(messages, "messages", min_items=1, allow_empty=False)
        for i, msg in enumerate(messages):
            msg = validate_dict(msg, f"messages[{i}]", required_keys=["role", "content"])
            validate_string(msg["role"], f"messages[{i}].role", min_length=1)
            validate_string(msg["content"], f"messages[{i}].content", min_length=1)
        
        if model is not None:
            model = validate_string(model, "model", min_length=1)
        
        try:
            response = completion(
                model=model or "gpt-3.5-turbo",
                messages=messages,
                api_key=self.api_key,
                api_base=self.api_base,
                **{**self.config, **kwargs}
            )
            
            return {
                "message": {
                    "role": response.choices[0].message.role,
                    "content": response.choices[0].message.content
                },
                "model": response.model,
                "provider": "litellm",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if hasattr(response.usage, 'prompt_tokens') else 0,
                    "completion_tokens": response.usage.completion_tokens if hasattr(response.usage, 'completion_tokens') else 0,
                    "total_tokens": response.usage.total_tokens if hasattr(response.usage, 'total_tokens') else 0
                }
            }
        except Exception as e:
            error_msg = f"LiteLLM chat failed: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelError(error_msg, details={"model": model, "error": str(e)})
    
    def embed(self, text: str, model: Optional[str] = None, **kwargs) -> List[float]:
        """Generate embeddings using LiteLLM
        
        Args:
            text: Input text to embed
            model: Embedding model name
        
        Returns:
            List of embedding values
        
        Raises:
            ModelError: If embedding fails
        """
        text = validate_string(text, "text", min_length=1)
        if model is not None:
            model = validate_string(model, "model", min_length=1)
        
        try:
            response = embedding(
                model=model or "text-embedding-ada-002",
                input=text,
                api_key=self.api_key,
                api_base=self.api_base,
                **{**self.config, **kwargs}
            )
            
            return response.data[0].embedding
        except Exception as e:
            error_msg = f"LiteLLM embedding failed: {str(e)}"
            self._logger.error(error_msg, exc_info=True)
            raise ModelError(error_msg, details={"model": model, "error": str(e)})
    
    def get_available_models(self) -> List[str]:
        """Get available models from LiteLLM"""
        try:
            if LITELLM_AVAILABLE:
                return get_model_list()
            return []
        except Exception as e:
            self._logger.warning(f"Failed to get model list: {str(e)}")
            return []


class ModelIntegrationFactory:
    """Factory for creating model integrations using LiteLLM"""
    
    @staticmethod
    def create(provider: str = "litellm", api_key: Optional[str] = None, **kwargs) -> ModelProvider:
        """Create a LiteLLM provider instance
        
        Args:
            provider: Provider name (default: "litellm")
            api_key: API key for the provider (optional, can be set via environment)
            **kwargs: Additional provider-specific arguments
        
        Returns:
            LiteLLMProvider instance
        
        Raises:
            ValidationError: If provider is invalid
            ConfigurationError: If LiteLLM is not available or creation fails
        """
        provider = validate_string(provider, "provider", min_length=1).lower()
        
        if provider != "litellm":
            raise ConfigurationError(
                f"Only 'litellm' provider is supported. Got: {provider}",
                details={"provider": provider, "supported": ["litellm"]}
            )
        
        if not LITELLM_AVAILABLE:
            raise ConfigurationError(
                "LiteLLM is not installed. Install with: pip install litellm",
                details={"package": "litellm"}
            )
        
        try:
            return LiteLLMProvider(api_key=api_key, **kwargs)
        except Exception as e:
            raise ConfigurationError(
                f"Failed to create LiteLLM provider: {str(e)}",
                details={"provider": provider, "error": str(e)}
            )
