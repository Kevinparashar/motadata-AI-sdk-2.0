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

