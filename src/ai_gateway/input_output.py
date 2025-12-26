"""
Data preprocessing and post-processing
"""
from typing import Dict, Any, List, Union, Optional
import json
from ..core.validators import validate_string, validate_list, validate_dict
from ..core.exceptions import ValidationError, ModelError


def preprocess_input(
    data: Union[str, Dict[str, Any], List[Any]],
    format: str = "json"
) -> str:
    """Preprocess input data for AI model
    
    Args:
        data: Input data (string, dict, or list)
        format: Output format (json or text)
    
    Returns:
        Preprocessed string
    
    Raises:
        ValidationError: If format is invalid
        ModelError: If preprocessing fails
    """
    format = validate_string(format, "format", min_length=1, max_length=20)
    if format not in ["json", "text"]:
        raise ValidationError(f"Unsupported format: {format}", field="format", value=format)
    
    try:
        if isinstance(data, str):
            return data
        elif isinstance(data, (dict, list)):
            if format == "json":
                return json.dumps(data)
            else:
                return str(data)
        else:
            return str(data)
    except Exception as e:
        raise ModelError(f"Failed to preprocess input: {str(e)}", details={"format": format, "data_type": type(data).__name__})


def postprocess_output(
    response: Union[str, Dict[str, Any]],
    format: str = "json"
) -> Any:
    """Postprocess AI model output"""
    if isinstance(response, dict):
        return response
    elif isinstance(response, str):
        if format == "json":
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {"text": response}
        else:
            return {"text": response}
    else:
        return response


def normalize_text(text: str) -> str:
    """Normalize text input
    
    Args:
        text: Text to normalize
    
    Returns:
        Normalized text string
    
    Raises:
        ValidationError: If text is invalid
    """
    text = validate_string(text, "text", min_length=1, allow_empty=True)
    return text.strip().replace("\n", " ").replace("\t", " ")


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into chunks with overlap
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk
        overlap: Overlap between chunks
    
    Returns:
        List of text chunks
    
    Raises:
        ValidationError: If inputs are invalid
    """
    text = validate_string(text, "text", min_length=1)
    if chunk_size <= 0:
        raise ValidationError("chunk_size must be positive", field="chunk_size", value=chunk_size)
    if overlap < 0:
        raise ValidationError("overlap must be non-negative", field="overlap", value=overlap)
    if overlap >= chunk_size:
        raise ValidationError("overlap must be less than chunk_size", field="overlap", value=overlap)
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
    return chunks


def format_messages(
    messages: List[Dict[str, str]],
    system_prompt: Optional[str] = None
) -> List[Dict[str, str]]:
    """Format messages for chat API
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        system_prompt: Optional system prompt string
    
    Returns:
        Formatted list of messages
    
    Raises:
        ValidationError: If messages or system_prompt is invalid
    """
    messages = validate_list(messages, "messages", min_items=1, allow_empty=False)
    for i, msg in enumerate(messages):
        msg = validate_dict(msg, f"messages[{i}]", required_keys=["role", "content"])
        validate_string(msg["role"], f"messages[{i}].role", min_length=1)
        validate_string(msg["content"], f"messages[{i}].content", min_length=1)
    
    formatted = []
    if system_prompt:
        system_prompt = validate_string(system_prompt, "system_prompt", min_length=1)
        formatted.append({"role": "system", "content": system_prompt})
    formatted.extend(messages)
    return formatted
