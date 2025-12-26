"""
Custom encoding/decoding logic
"""
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod
import json
import base64
from ..core.validators import validate_string
from ..core.exceptions import CodecError, ValidationError
import logging


class Codec(ABC):
    """Abstract base class for codecs"""
    
    @abstractmethod
    def encode(self, data: Any) -> bytes:
        """Encode data to bytes"""
        pass
    
    @abstractmethod
    def decode(self, data: bytes) -> Any:
        """Decode bytes to data"""
        pass


class JSONCodec(Codec):
    """JSON encoding/decoding codec"""
    
    def encode(self, data: Any) -> bytes:
        """Encode data to JSON bytes
        
        Raises:
            CodecError: If encoding fails
        """
        try:
            return json.dumps(data).encode('utf-8')
        except (TypeError, ValueError) as e:
            raise CodecError(f"Failed to encode data to JSON: {str(e)}", details={"data_type": type(data).__name__})
    
    def decode(self, data: bytes) -> Any:
        """Decode JSON bytes to data
        
        Raises:
            CodecError: If decoding fails
        """
        try:
            return json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise CodecError(f"Failed to decode JSON data: {str(e)}", details={"data_length": len(data)})


class Base64Codec(Codec):
    """Base64 encoding/decoding codec"""
    
    def encode(self, data: Any) -> bytes:
        """Encode data to base64 bytes"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif not isinstance(data, bytes):
            data = str(data).encode('utf-8')
        return base64.b64encode(data)
    
    def decode(self, data: bytes) -> Any:
        """Decode base64 bytes to data"""
        decoded = base64.b64decode(data)
        try:
            return decoded.decode('utf-8')
        except UnicodeDecodeError:
            return decoded


class BinaryCodec(Codec):
    """Binary encoding/decoding codec"""
    
    def encode(self, data: Any) -> bytes:
        """Encode data to binary"""
        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            return data.encode('utf-8')
        else:
            return str(data).encode('utf-8')
    
    def decode(self, data: bytes) -> Any:
        """Decode binary to data"""
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            return data


class CustomCodec(Codec):
    """Custom codec with configurable encoding/decoding"""
    
    def __init__(self, format: str = "json", **kwargs):
        self.format = validate_string(format, "format", min_length=1, max_length=50)
        self.config = kwargs
        self._codec = self._get_codec(format)
        self._logger = logging.getLogger(__name__)
    
    def _get_codec(self, format: str) -> Codec:
        """Get the appropriate codec based on format
        
        Raises:
            ValidationError: If format is not supported
        """
        codecs = {
            "json": JSONCodec(),
            "base64": Base64Codec(),
            "binary": BinaryCodec(),
        }
        if format not in codecs:
            raise ValidationError(
                f"Unknown codec format: {format}",
                field="format",
                value=format
            )
        return codecs[format]
    
    def encode(self, data: Any) -> bytes:
        """Encode data using the configured codec"""
        return self._codec.encode(data)
    
    def decode(self, data: bytes) -> Any:
        """Decode data using the configured codec"""
        return self._codec.decode(data)
