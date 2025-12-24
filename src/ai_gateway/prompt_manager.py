"""
Manage prompts, templates, and fine-tuning
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import json


class PromptTemplate:
    """Prompt template class"""
    
    def __init__(self, name: str, template: str, variables: Optional[List[str]] = None):
        self.name = name
        self.template = template
        self.variables = variables or []
    
    def render(self, **kwargs) -> str:
        """Render the template with provided variables"""
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
        """Register a new prompt template"""
        self._templates[template.name] = template
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get a template by name"""
        return self._templates.get(name)
    
    def list_templates(self) -> List[str]:
        """List all available template names"""
        return list(self._templates.keys())
    
    def load_templates_from_file(self, file_path: str) -> None:
        """Load templates from a JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
            for template_data in data:
                template = PromptTemplate(
                    name=template_data["name"],
                    template=template_data["template"],
                    variables=template_data.get("variables", [])
                )
                self.register_template(template)
    
    def save_templates_to_file(self, file_path: str) -> None:
        """Save templates to a JSON file"""
        templates_data = [t.to_dict() for t in self._templates.values()]
        with open(file_path, 'w') as f:
            json.dump(templates_data, f, indent=2)
