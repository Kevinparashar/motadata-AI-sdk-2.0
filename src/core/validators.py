"""
Input validation utilities
"""
from typing import Any, Optional, List, Dict
from .exceptions import ValidationError


def validate_string(value: Any, field_name: str, min_length: Optional[int] = None, 
                   max_length: Optional[int] = None, allow_empty: bool = False) -> str:
    """Validate and sanitize string input
    
    Args:
        value: Value to validate
        field_name: Name of the field being validated
        min_length: Minimum length requirement
        max_length: Maximum length requirement
        allow_empty: Whether empty strings are allowed
    
    Returns:
        Validated and sanitized string
    
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, str):
        raise ValidationError(
            f"{field_name} must be a string, got {type(value).__name__}",
            field=field_name,
            value=value
        )
    
    value = value.strip()
    
    if not allow_empty and not value:
        raise ValidationError(
            f"{field_name} cannot be empty",
            field=field_name,
            value=value
        )
    
    if min_length is not None and len(value) < min_length:
        raise ValidationError(
            f"{field_name} must be at least {min_length} characters",
            field=field_name,
            value=value
        )
    
    if max_length is not None and len(value) > max_length:
        raise ValidationError(
            f"{field_name} must be at most {max_length} characters",
            field=field_name,
            value=value
        )
    
    return value


def validate_dict(value: Any, field_name: str, required_keys: Optional[List[str]] = None) -> Dict:
    """Validate dictionary input
    
    Args:
        value: Value to validate
        field_name: Name of the field being validated
        required_keys: List of required keys
    
    Returns:
        Validated dictionary
    
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, dict):
        raise ValidationError(
            f"{field_name} must be a dictionary, got {type(value).__name__}",
            field=field_name,
            value=value
        )
    
    if required_keys:
        missing_keys = [key for key in required_keys if key not in value]
        if missing_keys:
            raise ValidationError(
                f"{field_name} missing required keys: {missing_keys}",
                field=field_name,
                value=value
            )
    
    return value


def validate_list(value: Any, field_name: str, min_items: Optional[int] = None,
                 max_items: Optional[int] = None, allow_empty: bool = True) -> List:
    """Validate list input
    
    Args:
        value: Value to validate
        field_name: Name of the field being validated
        min_items: Minimum number of items
        max_items: Maximum number of items
        allow_empty: Whether empty lists are allowed
    
    Returns:
        Validated list
    
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, list):
        raise ValidationError(
            f"{field_name} must be a list, got {type(value).__name__}",
            field=field_name,
            value=value
        )
    
    if not allow_empty and len(value) == 0:
        raise ValidationError(
            f"{field_name} cannot be empty",
            field=field_name,
            value=value
        )
    
    if min_items is not None and len(value) < min_items:
        raise ValidationError(
            f"{field_name} must have at least {min_items} items",
            field=field_name,
            value=value
        )
    
    if max_items is not None and len(value) > max_items:
        raise ValidationError(
            f"{field_name} must have at most {max_items} items",
            field=field_name,
            value=value
        )
    
    return value

