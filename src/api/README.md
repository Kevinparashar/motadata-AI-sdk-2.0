# API Communication Module

## WHY
The API module handles all external API communication, authentication, and request/response management. It provides a robust foundation for making HTTP requests, WebSocket connections, and managing API credentials securely.

## WHAT
This module contains:

- **api_communicator.py**: Core API communication methods for HTTP requests (GET, POST, PUT, DELETE) and WebSocket connections. Handles connection pooling, retries, and error handling
- **api_methods.py**: High-level methods for data encoding/decoding, sending requests, handling responses, and managing request/response transformations
- **authentication.py**: Token-based authentication mechanisms including OAuth2, JWT token management, API key handling, and session management

## HOW
Use the API module to communicate with external services:

```python
from src.api.api_communicator import APICommunicator
from src.api.api_methods import send_request, encode_data
from src.api.authentication import OAuth2Authenticator, JWTAuthenticator

# Set up authentication
auth = OAuth2Authenticator(client_id="...", client_secret="...")
token = auth.get_access_token()

# Create API communicator
api = APICommunicator(base_url="https://api.example.com")
api.set_auth(token)

# Make requests
response = api.get("/endpoint")
response = api.post("/endpoint", data=encode_data(payload))

# Or use high-level methods
from src.api.api_methods import send_request
response = send_request("POST", "/endpoint", data=payload, auth=auth)
```

The module handles authentication refresh, rate limiting, error retries, and response parsing automatically.

## Input Validation and Error Handling

**All public methods in the API module include comprehensive input validation:**

- **APICommunicator.__init__()**: Validates `base_url` (string, non-empty), `timeout` (positive integer), and `headers` (dict)
- **APICommunicator.set_auth()**: Validates `token` (string, non-empty)
- **APICommunicator.get/post/put/delete()**: Validates `endpoint` (string) and optional `params`/`data`/`headers` (dict)
- **WebSocketCommunicator.__init__()**: Validates `url` (string, non-empty)
- **WebSocketCommunicator.send()**: Validates `message` (dict)
- **OAuth2Authenticator.__init__()**: Validates `client_id`, `client_secret`, `token_url` (all strings, non-empty), and optional `scope`
- **JWTAuthenticator.__init__()**: Validates `secret_key` (string, non-empty) and `algorithm` (string, 1-20 chars)
- **JWTAuthenticator.decode_token()**: Validates `token` (string, non-empty)
- **APIKeyAuthenticator.__init__()**: Validates `api_key` (string, non-empty)
- **send_request()**: Validates `method` (must be GET/POST/PUT/DELETE/PATCH), `url` (string), and `timeout` (positive)

**Custom Exceptions Used:**
- `ValidationError`: Invalid input parameters (replaces `ValueError`, `TypeError`)
- `APIError`: API request failures with status codes and response data (replaces generic exceptions)
- `AuthenticationError`: Authentication failures (replaces generic exceptions)
- `ConnectionError`: Connection failures (replaces built-in `ConnectionError`)

All methods raise appropriate custom exceptions with detailed error messages, status codes (for API errors), and context information.

## Libraries
This module uses the following Python standard libraries and packages:

- **typing**: Type hints (Dict, Any, Optional, List)
- **threading**: Thread synchronization primitives (Lock) for thread-safe operations
- **datetime**: Date and time handling (datetime, timedelta) for token expiration
- **json**: JSON encoding and decoding for request/response data
- **src.core.data_structures**: RequestModel and ResponseModel from core module
- **src.codecs**: encode_with_format and decode_with_format from codecs module

## Functions and Classes

### api_communicator.py
- **APICommunicator** (class): Base API communicator for HTTP and WebSocket
  - `__init__()`: Initialize communicator with base_url, timeout, and headers
  - `set_auth()`: Set authentication token
  - `get()`: Make a GET request
  - `post()`: Make a POST request
  - `put()`: Make a PUT request
  - `delete()`: Make a DELETE request
  - `_make_request()`: Internal method to make HTTP requests
- **WebSocketCommunicator** (class): WebSocket communicator for real-time communication
  - `__init__()`: Initialize WebSocket communicator with URL
  - `connect()`: Connect to WebSocket server
  - `disconnect()`: Disconnect from WebSocket server
  - `send()`: Send a message through WebSocket
  - `receive()`: Receive a message from WebSocket
  - `is_connected` (property): Check if connected to WebSocket

### api_methods.py
- **encode_data()**: Encode data for API transmission
- **decode_data()**: Decode data from API response
- **send_request()**: Send an HTTP request with authentication
- **prepare_request_data()**: Prepare data for API request
- **parse_response()**: Parse API response into structured format

### authentication.py
- **Authenticator** (abstract class): Base authenticator class
  - `get_access_token()`: Abstract method to get access token
  - `is_token_valid()`: Check if current token is valid
- **OAuth2Authenticator** (class): OAuth2 authentication
  - `__init__()`: Initialize OAuth2 authenticator with client_id, client_secret, token_url, and scope
  - `get_access_token()`: Get OAuth2 access token
  - `refresh_token()`: Refresh the access token
- **JWTAuthenticator** (class): JWT token authentication
  - `__init__()`: Initialize JWT authenticator with secret_key and algorithm
  - `get_access_token()`: Get JWT access token
  - `decode_token()`: Decode JWT token
- **APIKeyAuthenticator** (class): API key authentication
  - `__init__()`: Initialize API key authenticator with api_key
  - `get_access_token()`: Get API key
  - `is_token_valid()`: API keys don't expire

