"""
Data preprocessing and post-processing
"""
from typing import Dict, Any, List, Union, Optional
import json


def preprocess_input(
    data: Union[str, Dict[str, Any], List[Any]],
    format: str = "json"
) -> str:
    """Preprocess input data for AI model"""
    if isinstance(data, str):
        return data
    elif isinstance(data, (dict, list)):
        if format == "json":
            return json.dumps(data)
        else:
            return str(data)
    else:
        return str(data)


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
    """Normalize text input"""
    return text.strip().replace("\n", " ").replace("\t", " ")


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into chunks with overlap"""
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
    """Format messages for chat API"""
    formatted = []
    if system_prompt:
        formatted.append({"role": "system", "content": system_prompt})
    formatted.extend(messages)
    return formatted
