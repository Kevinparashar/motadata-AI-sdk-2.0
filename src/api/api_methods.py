"""
Methods for data encoding/decoding, sending requests
"""
from typing import Dict, Any, Optional
import json
from .api_communicator import APICommunicator
from ..codecs import encode_with_format, decode_with_format
from ..core.data_structures import ResponseModel
from ..core.validators import validate_string
from ..core.exceptions import ValidationError, APIError


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
    """Send an HTTP request
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        url: Base URL for the request
        data: Request body data
        headers: Additional headers
        auth: Authentication object or token string
        timeout: Request timeout in seconds
    
    Returns:
        ResponseModel with response data
    
    Raises:
        ValidationError: If method or URL is invalid
        APIError: If request fails
    """
    method = validate_string(method, "method", min_length=1).upper()
    url = validate_string(url, "url", min_length=1)
    
    if method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        raise ValidationError(
            f"Unsupported HTTP method: {method}",
            field="method",
            value=method
        )
    
    if timeout <= 0:
        raise ValidationError("timeout must be positive", field="timeout", value=timeout)
    
    try:
        communicator = APICommunicator(base_url=url, timeout=timeout, headers=headers)
        
        if auth:
            if hasattr(auth, 'get_access_token'):
                token = auth.get_access_token()
                communicator.set_auth(token)
            elif isinstance(auth, str):
                communicator.set_auth(auth)
        
        if method == "GET":
            return communicator.get("")
        elif method == "POST":
            return communicator.post("", data=data)
        elif method == "PUT":
            return communicator.put("", data=data)
        elif method == "DELETE":
            return communicator.delete("")
        elif method == "PATCH":
            return communicator.put("", data=data)  # Using PUT as placeholder
    except APIError:
        raise
    except Exception as e:
        raise APIError(f"Failed to send {method} request to {url}", details={"error": str(e)})


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
