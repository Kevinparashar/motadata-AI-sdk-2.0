"""
Methods for data encoding/decoding, sending requests
"""
from typing import Dict, Any, Optional
import json
from .api_communicator import APICommunicator
from ..codecs import encode_with_format, decode_with_format
from ..core.data_structures import ResponseModel


def encode_data(data: Any, format: str = "json") -> bytes:
    """Encode data for API transmission"""
    return encode_with_format(data, format=format)


def decode_data(data: bytes, format: str = "json") -> Any:
    """Decode data from API response"""
    return decode_with_format(data, format=format)


def send_request(
    method: str,
    url: str,
    data: Optional[Any] = None,
    headers: Optional[Dict[str, str]] = None,
    auth: Optional[Any] = None,
    timeout: int = 30
) -> ResponseModel:
    """Send an HTTP request"""
    communicator = APICommunicator(base_url=url, timeout=timeout, headers=headers)
    
    if auth:
        if hasattr(auth, 'get_access_token'):
            token = auth.get_access_token()
            communicator.set_auth(token)
        elif isinstance(auth, str):
            communicator.set_auth(auth)
    
    if method.upper() == "GET":
        return communicator.get("")
    elif method.upper() == "POST":
        return communicator.post("", data=data)
    elif method.upper() == "PUT":
        return communicator.put("", data=data)
    elif method.upper() == "DELETE":
        return communicator.delete("")
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")


def prepare_request_data(data: Any) -> Dict[str, Any]:
    """Prepare data for API request"""
    if isinstance(data, dict):
        return data
    elif isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {"data": data}
    else:
        return {"data": str(data)}


def parse_response(response: ResponseModel) -> Dict[str, Any]:
    """Parse API response"""
    result = {
        "status_code": response.status_code,
        "headers": response.headers,
        "timestamp": response.timestamp.isoformat()
    }
    
    if response.error:
        result["error"] = response.error
    else:
        result["data"] = response.data
    
    return result
