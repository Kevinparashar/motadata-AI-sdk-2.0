"""
Manage prompts, templates, and fine-tuning
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
from ..core.validators import validate_string, validate_list, validate_dict
from ..core.exceptions import ValidationError, ConfigurationError
import logging


class PromptTemplate:
    """Prompt template class"""
    
    def __init__(self, name: str, template: str, variables: Optional[List[str]] = None):
        self.name = validate_string(name, "name", min_length=1, max_length=100)
        self.template = validate_string(template, "template", min_length=1)
        if variables is not None:
            self.variables = validate_list(variables, "variables", allow_empty=True)
        else:
            self.variables = []
    
    def render(self, **kwargs) -> str:
        """Render the template with provided variables
        
        Args:
            **kwargs: Variables to substitute in template
        
        Returns:
            Rendered template string
        
        Raises:
            ValidationError: If required variables are missing
        """
        rendered = self.template
        for key, value in kwargs.items():
            rendered = rendered.replace(f"{{{key}}}", str(value))
        return rendered
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary"""
        return {
            "name": self.name,
            "template": self.template,
            "variables": self.variables
        }


class PromptManager:
    """Manager for prompts and templates"""
    
    def __init__(self, templates_dir: Optional[str] = None):
        self.templates_dir = Path(templates_dir) if templates_dir else None
        self._templates: Dict[str, PromptTemplate] = {}
        self._load_default_templates()
    
    def _load_default_templates(self) -> None:
        """Load default prompt templates"""
        default_templates = {
            "classification": PromptTemplate(
                name="classification",
                template="Classify the following text: {text}\n\nCategory:",
                variables=["text"]
            ),
            "summarization": PromptTemplate(
                name="summarization",
                template="Summarize the following text:\n\n{text}\n\nSummary:",
                variables=["text"]
            ),
            "qa": PromptTemplate(
                name="qa",
                template="Question: {question}\n\nContext: {context}\n\nAnswer:",
                variables=["question", "context"]
            )
        }
        self._templates.update(default_templates)
    
    def register_template(self, template: PromptTemplate) -> None:
        """Register a new prompt template
        
        Args:
            template: PromptTemplate instance to register
        
        Raises:
            ValidationError: If template is invalid
        """
        if not isinstance(template, PromptTemplate):
            raise ValidationError("template must be a PromptTemplate instance", field="template")
        self._templates[template.name] = template
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get a template by name
        
        Args:
            name: Template name
        
        Returns:
            PromptTemplate instance or None if not found
        
        Raises:
            ValidationError: If name is invalid
        """
        name = validate_string(name, "name", min_length=1)
        return self._templates.get(name)
    
    def list_templates(self) -> List[str]:
        """List all available template names
        
        Returns:
            List of template names
        """
        return list(self._templates.keys())
    
    def load_templates_from_file(self, file_path: str) -> None:
        """Load templates from a JSON file
        
        Args:
            file_path: Path to JSON file containing templates
        
        Raises:
            ValidationError: If file_path is invalid
            ConfigurationError: If file not found or invalid format
        """
        file_path = validate_string(file_path, "file_path", min_length=1)
        path = Path(file_path)
        if not path.exists():
            raise ConfigurationError(f"Template file not found: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ConfigurationError("Template file must contain a JSON array")
                
                for template_data in data:
                    template_data = validate_dict(template_data, "template_data", required_keys=["name", "template"])
                    template = PromptTemplate(
                        name=template_data["name"],
                        template=template_data["template"],
                        variables=template_data.get("variables", [])
                    )
                    self.register_template(template)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in template file: {str(e)}", details={"file": file_path})
        except Exception as e:
            raise ConfigurationError(f"Failed to load templates: {str(e)}", details={"file": file_path})
    
    def save_templates_to_file(self, file_path: str) -> None:
        """Save templates to a JSON file
        
        Args:
            file_path: Path to save JSON file
        
        Raises:
            ValidationError: If file_path is invalid
            ConfigurationError: If save fails
        """
        file_path = validate_string(file_path, "file_path", min_length=1)
        try:
            templates_data = [t.to_dict() for t in self._templates.values()]
            with open(file_path, 'w') as f:
                json.dump(templates_data, f, indent=2)
        except Exception as e:
            raise ConfigurationError(f"Failed to save templates: {str(e)}", details={"file": file_path})
