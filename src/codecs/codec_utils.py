"""
Helper functions for codec operations
"""
from typing import Dict, Optional, Type, Any
from .custom_codec import Codec, JSONCodec, Base64Codec, BinaryCodec, CustomCodec
from ..core.validators import validate_string
from ..core.exceptions import CodecError, ValidationError


# Codec registry
_codec_registry: Dict[str, Type[Codec]] = {
    "json": JSONCodec,
    "base64": Base64Codec,
    "binary": BinaryCodec,
    "custom": CustomCodec,
}


def register_codec(name: str, codec_class: Type[Codec]) -> None:
    """Register a custom codec
    
    Args:
        name: Codec name identifier
        codec_class: Codec class to register
    
    Raises:
        ValidationError: If name or codec_class is invalid
    """
    name = validate_string(name, "name", min_length=1, max_length=50)
    if not isinstance(codec_class, type) or not issubclass(codec_class, Codec):
        raise ValidationError(
            "codec_class must be a subclass of Codec",
            field="codec_class",
            value=type(codec_class).__name__
        )
    _codec_registry[name] = codec_class


def get_codec(name: str, **kwargs) -> Codec:
    """Get a codec instance by name
    
    Args:
        name: Codec name
        **kwargs: Additional arguments for codec initialization
    
    Returns:
        Codec instance
    
    Raises:
        ValidationError: If codec name is not found
    """
    name = validate_string(name, "name", min_length=1)
    if name not in _codec_registry:
        raise ValidationError(
            f"Unknown codec: {name}",
            field="name",
            value=name
        )
    
    try:
        codec_class = _codec_registry[name]
        if name == "custom":
            return codec_class(format=kwargs.get("format", "json"), **kwargs)
        return codec_class(**kwargs)
    except Exception as e:
        raise CodecError(f"Failed to create codec instance: {str(e)}", details={"name": name, "error": str(e)})


def list_codecs() -> list:
    """List all registered codecs"""
    return list(_codec_registry.keys())


def validate_encoded_data(data: bytes, codec: Codec) -> bool:
    """Validate that data can be decoded with the given codec"""
    try:
        codec.decode(data)
        return True
    except Exception:
        return False


def encode_with_format(data: Any, format: str = "json") -> bytes:
    """Quick encode function with format specification
    
    Args:
        data: Data to encode
        format: Codec format name
    
    Returns:
        Encoded bytes
    
    Raises:
        CodecError: If encoding fails
    """
    codec = get_codec(format)
    try:
        return codec.encode(data)
    except CodecError:
        raise
    except Exception as e:
        raise CodecError(f"Failed to encode data with format {format}: {str(e)}", details={"format": format, "error": str(e)})


def decode_with_format(data: bytes, format: str = "json") -> Any:
    """Quick decode function with format specification
    
    Args:
        data: Encoded bytes to decode
        format: Codec format name
    
    Returns:
        Decoded data
    
    Raises:
        CodecError: If decoding fails
    """
    codec = get_codec(format)
    try:
        return codec.decode(data)
    except CodecError:
        raise
    except Exception as e:
        raise CodecError(f"Failed to decode data with format {format}: {str(e)}", details={"format": format, "error": str(e)})
