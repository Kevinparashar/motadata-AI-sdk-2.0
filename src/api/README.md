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

