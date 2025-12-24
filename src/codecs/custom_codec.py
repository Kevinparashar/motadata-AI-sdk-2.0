"""
Custom encoding/decoding logic
"""
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod
import json
import base64


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
        """Encode data to JSON bytes"""
        return json.dumps(data).encode('utf-8')
    
    def decode(self, data: bytes) -> Any:
        """Decode JSON bytes to data"""
        return json.loads(data.decode('utf-8'))


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
        self.format = format
        self.config = kwargs
        self._codec = self._get_codec(format)
    
    def _get_codec(self, format: str) -> Codec:
        """Get the appropriate codec based on format"""
        codecs = {
            "json": JSONCodec(),
            "base64": Base64Codec(),
            "binary": BinaryCodec(),
        }
        if format not in codecs:
            raise ValueError(f"Unknown codec format: {format}")
        return codecs[format]
    
    def encode(self, data: Any) -> bytes:
        """Encode data using the configured codec"""
        return self._codec.encode(data)
    
    def decode(self, data: bytes) -> Any:
        """Decode data using the configured codec"""
        return self._codec.decode(data)
