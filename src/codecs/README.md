# Codecs Module

## WHY

The codecs module provides custom encoding and decoding functionality for transforming data between different formats. This is essential for handling custom data serialization, protocol-specific encoding, and data transformation requirements that standard libraries don't cover.

## WHAT

This module contains:

- **custom_codec.py**: Custom encoding and decoding logic for specialized data formats, protocol-specific serialization, and proprietary data structures
- **codec_utils.py**: Helper functions and utilities for codec operations, including format validation, encoding/decoding error handling, and codec registry management

## HOW

Use codecs to transform data:

```python
from src.codecs.custom_codec import CustomCodec
from src.codecs.codec_utils import register_codec, get_codec

# Create a custom codec
codec = CustomCodec(format="binary_protocol")

# Encode data
encoded_data = codec.encode(data_object)

# Decode data
decoded_object = codec.decode(encoded_data)

# Register and retrieve codecs
register_codec("my_format", CustomCodec(format="my_format"))
codec = get_codec("my_format")
```

Codecs are particularly useful when working with custom protocols, binary formats, or when you need to transform data for specific communication channels.

## Input Validation and Error Handling

**All public methods in the codecs module include comprehensive input validation:**

- **CustomCodec.__init__()**: Validates `format` (string, 1-50 chars, must be "json", "base64", or "binary")
- **register_codec()**: Validates `name` (string, 1-50 chars) and `codec_class` (must be a Codec subclass)
- **get_codec()**: Validates `name` (string, non-empty, must exist in registry)
- **encode_with_format()**: Validates `format` (string, must exist in registry)
- **decode_with_format()**: Validates `format` (string, must exist in registry)
- **JSONCodec.encode()**: Validates data can be JSON serialized
- **JSONCodec.decode()**: Validates data can be JSON deserialized

**Custom Exceptions Used:**

- `ValidationError`: Invalid input parameters (replaces `ValueError`, `TypeError`)
- `CodecError`: Encoding/decoding failures (replaces `json.JSONDecodeError`, `UnicodeDecodeError`, and generic exceptions)

All methods raise appropriate custom exceptions with detailed error messages and context information for debugging.

## Libraries

This module uses the following Python standard libraries and packages:

- **typing**: Type hints (Any, Dict, Optional, Type)
- **abc**: Abstract base classes (ABC, abstractmethod) for defining codec interfaces
- **json**: JSON encoding and decoding for JSON codec implementation
- **base64**: Base64 encoding and decoding for Base64 codec implementation

## Functions and Classes

### custom_codec.py

- **Codec** (abstract class): Abstract base class for codecs
  - `encode()`: Abstract method to encode data to bytes
  - `decode()`: Abstract method to decode bytes to data
- **JSONCodec** (class): JSON encoding/decoding codec
  - `encode()`: Encode data to JSON bytes
  - `decode()`: Decode JSON bytes to data
- **Base64Codec** (class): Base64 encoding/decoding codec
  - `encode()`: Encode data to base64 bytes
  - `decode()`: Decode base64 bytes to data
- **BinaryCodec** (class): Binary encoding/decoding codec
  - `encode()`: Encode data to binary
  - `decode()`: Decode binary to data
- **CustomCodec** (class): Custom codec with configurable encoding/decoding
  - `__init__()`: Initialize codec with format and config
  - `encode()`: Encode data using the configured codec
  - `decode()`: Decode data using the configured codec

### codec_utils.py

- **register_codec()**: Register a custom codec in the codec registry
- **get_codec()**: Get a codec instance by name
- **list_codecs()**: List all registered codecs
- **validate_encoded_data()**: Validate that data can be decoded with the given codec
- **encode_with_format()**: Quick encode function with format specification
- **decode_with_format()**: Quick decode function with format specification
