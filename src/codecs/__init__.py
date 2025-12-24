"""
Codec handling for custom data encoding/decoding
"""
from .custom_codec import (
    Codec,
    JSONCodec,
    Base64Codec,
    BinaryCodec,
    CustomCodec
)
from .codec_utils import (
    register_codec,
    get_codec,
    list_codecs,
    validate_encoded_data,
    encode_with_format,
    decode_with_format
)

__all__ = [
    "Codec",
    "JSONCodec",
    "Base64Codec",
    "BinaryCodec",
    "CustomCodec",
    "register_codec",
    "get_codec",
    "list_codecs",
    "validate_encoded_data",
    "encode_with_format",
    "decode_with_format",
]
