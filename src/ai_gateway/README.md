# AI Gateway Module

## WHY
The AI Gateway module provides a unified interface for interacting with various AI models and services. It abstracts away the complexities of different AI providers, allowing you to switch between models or use multiple models seamlessly without changing your application code.

## WHAT
This module contains:

- **gateway.py**: Main gateway interface that provides a unified API for interacting with AI models, handling requests, and managing connections
- **input_output.py**: Data preprocessing and post-processing utilities for transforming input data into model-compatible formats and processing model outputs
- **model_integration.py**: Integration logic for different AI models and providers (OpenAI, Anthropic, local models, etc.), handling provider-specific configurations and API calls
- **prompt_manager.py**: Prompt management system for handling prompt templates, fine-tuning configurations, and dynamic prompt generation

## HOW
Use the AI Gateway to interact with AI models:

```python
from src.ai_gateway.gateway import AIGateway
from src.ai_gateway.model_integration import ModelProvider
from src.ai_gateway.prompt_manager import PromptManager

# Initialize the gateway
gateway = AIGateway(provider=ModelProvider.OPENAI, api_key="your-key")

# Use prompt manager
prompt_mgr = PromptManager()
prompt = prompt_mgr.get_template("classification")

# Process input/output
from src.ai_gateway.input_output import preprocess_input, postprocess_output

processed_input = preprocess_input(raw_data)
response = gateway.generate(prompt, processed_input)
result = postprocess_output(response)
```

The gateway handles authentication, rate limiting, error handling, and response formatting automatically.

## Input Validation and Error Handling

**All public methods in the AI Gateway module include comprehensive input validation:**

- **AIGateway.__init__()**: Validates `provider` (string, 1-50 chars), `api_key` (string, non-empty if provided), and `config` (dict)
- **AIGateway.set_model_integration()**: Validates integration object is not None
- **AIGateway.generate()**: Validates `prompt` (string, 1-100000 chars) and `model` (string, 1-100 chars if provided)
- **AIGateway.chat()**: Validates `messages` (list, non-empty, each message must have "role" and "content" keys) and `model` (string if provided)
- **AIGateway.embed()**: Validates `text` (string, 1-100000 chars) and `model` (string if provided)
- **OpenAIProvider/AnthropicProvider.__init__()**: Validates `api_key` (string, non-empty) and `base_url` (string if provided)
- **ModelIntegrationFactory.create()**: Validates `provider` (string, must be "openai" or "anthropic") and `api_key` (string, non-empty)
- **PromptTemplate.__init__()**: Validates `name` (string, 1-100 chars), `template` (string, non-empty), and `variables` (list)
- **PromptManager.get_template()**: Validates `name` (string, non-empty)
- **PromptManager.register_template()**: Validates template is a PromptTemplate instance
- **PromptManager.load_templates_from_file()**: Validates `file_path` (string) and file format (must be JSON array)
- **preprocess_input()**: Validates `format` (must be "json" or "text")
- **normalize_text()**: Validates `text` (string, allows empty)
- **chunk_text()**: Validates `text` (string, non-empty), `chunk_size` (positive), `overlap` (non-negative, less than chunk_size)
- **format_messages()**: Validates `messages` (list, non-empty, each with "role" and "content"), and `system_prompt` (string if provided)

**Custom Exceptions Used:**
- `ValidationError`: Invalid input parameters (replaces `ValueError`, `TypeError`)
- `ModelError`: AI model operation failures (replaces generic exceptions)
- `ConfigurationError`: Configuration and file loading errors (replaces `FileNotFoundError`, `ValueError`)
- `ConnectionError`: Connection failures (replaces built-in `ConnectionError`)

All methods raise appropriate custom exceptions with detailed error messages and context information for debugging.

## Libraries
This module uses the following Python standard libraries and packages:

- **typing**: Type hints (Dict, Any, Optional, List, Union)
- **abc**: Abstract base classes (ABC, abstractmethod) for defining interfaces
- **json**: JSON encoding and decoding for data serialization
- **pathlib**: Object-oriented filesystem paths for template file management
- **src.core.data_structures**: RequestModel and ResponseModel from core module

## Functions and Classes

### gateway.py
- **AIGateway** (class): Main gateway interface for AI model interactions
  - `__init__()`: Initialize gateway with provider, api_key, and config
  - `set_model_integration()`: Set the model integration handler
  - `generate()`: Generate a response from the AI model
  - `chat()`: Chat with the AI model
  - `embed()`: Generate embeddings for text
  - `get_available_models()`: Get list of available models
- **ModelProvider** (abstract class): Abstract base class for model providers
  - `generate()`: Abstract method to generate a response
  - `chat()`: Abstract method to chat with the model
  - `embed()`: Abstract method to generate embeddings

### input_output.py
- **preprocess_input()**: Preprocess input data for AI model (supports str, dict, list)
- **postprocess_output()**: Postprocess AI model output (handles JSON parsing)
- **normalize_text()**: Normalize text input (strip, replace newlines/tabs)
- **chunk_text()**: Split text into chunks with overlap for large text processing
- **format_messages()**: Format messages for chat API with optional system prompt

### model_integration.py
- **OpenAIProvider** (class): OpenAI model provider integration
  - `__init__()`: Initialize OpenAI provider with api_key and base_url
  - `generate()`: Generate response using OpenAI
  - `chat()`: Chat with OpenAI model
  - `embed()`: Generate embeddings using OpenAI
  - `get_available_models()`: Get available OpenAI models
- **AnthropicProvider** (class): Anthropic (Claude) model provider integration
  - `__init__()`: Initialize Anthropic provider with api_key
  - `generate()`: Generate response using Anthropic
  - `chat()`: Chat with Anthropic model
  - `embed()`: Generate embeddings using Anthropic
  - `get_available_models()`: Get available Anthropic models
- **ModelIntegrationFactory** (class): Factory for creating model integrations
  - `create()`: Static method to create a model provider instance

### prompt_manager.py
- **PromptTemplate** (class): Prompt template class
  - `__init__()`: Initialize template with name, template string, and variables
  - `render()`: Render the template with provided variables
  - `to_dict()`: Convert template to dictionary
- **PromptManager** (class): Manager for prompts and templates
  - `__init__()`: Initialize prompt manager with optional templates directory
  - `register_template()`: Register a new prompt template
  - `get_template()`: Get a template by name
  - `list_templates()`: List all available template names
  - `load_templates_from_file()`: Load templates from a JSON file
  - `save_templates_to_file()`: Save templates to a JSON file

