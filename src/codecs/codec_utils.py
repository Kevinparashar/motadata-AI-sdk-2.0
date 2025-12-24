"""
Helper functions for codec operations
"""
from typing import Dict, Optional, Type
from .custom_codec import Codec, JSONCodec, Base64Codec, BinaryCodec, CustomCodec


# Codec registry
_codec_registry: Dict[str, Type[Codec]] = {
    "json": JSONCodec,
    "base64": Base64Codec,
    "binary": BinaryCodec,
    "custom": CustomCodec,
}


def register_codec(name: str, codec_class: Type[Codec]) -> None:
    """Register a custom codec"""
    _codec_registry[name] = codec_class


def get_codec(name: str, **kwargs) -> Codec:
    """Get a codec instance by name"""
    if name not in _codec_registry:
        raise ValueError(f"Unknown codec: {name}")
    
    codec_class = _codec_registry[name]
    if name == "custom":
        return codec_class(format=kwargs.get("format", "json"), **kwargs)
    return codec_class(**kwargs)


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
    """Quick encode function with format specification"""
    codec = get_codec(format)
    return codec.encode(data)


def decode_with_format(data: bytes, format: str = "json") -> Any:
    """Quick decode function with format specification"""
    codec = get_codec(format)
    return codec.decode(data)
