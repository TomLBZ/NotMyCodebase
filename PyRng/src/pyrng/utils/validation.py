"""Validation utilities for PyRng."""

from typing import Union
from pyrng.core.exceptions import ValidationError


def validate_sample_size(size: int) -> None:
    """Validate that sample size is positive.
    
    Args:
        size: Sample size to validate.
    
    Raises:
        ValidationError: If size is not a positive integer.
    
    Examples:
        >>> validate_sample_size(100)  # OK
        >>> validate_sample_size(0)  # Raises ValidationError
        >>> validate_sample_size(-5)  # Raises ValidationError
    """
    if not isinstance(size, int):
        raise ValidationError(
            f"Sample size must be an integer, got {type(size).__name__}"
        )
    if size <= 0:
        raise ValidationError(
            f"Sample size must be positive, got {size}"
        )


def validate_positive(value: Union[int, float], name: str = "value") -> None:
    """Validate that a numeric value is positive.
    
    Args:
        value: Numeric value to validate.
        name: Parameter name for error messages.
    
    Raises:
        ValidationError: If value is not positive.
    
    Examples:
        >>> validate_positive(1.5, "sigma")  # OK
        >>> validate_positive(0, "lambda")  # Raises ValidationError
        >>> validate_positive(-2.0, "rate")  # Raises ValidationError
    """
    if not isinstance(value, (int, float)):
        raise ValidationError(
            f"{name} must be numeric, got {type(value).__name__}"
        )
    if value <= 0:
        raise ValidationError(
            f"{name} must be positive, got {value}"
        )


def validate_probability(p: float, name: str = "probability") -> None:
    """Validate that a value is a valid probability (0 <= p <= 1).
    
    Args:
        p: Probability value to validate.
        name: Parameter name for error messages.
    
    Raises:
        ValidationError: If p is not in [0, 1].
    
    Examples:
        >>> validate_probability(0.5)  # OK
        >>> validate_probability(0.0)  # OK
        >>> validate_probability(1.0)  # OK
        >>> validate_probability(1.5)  # Raises ValidationError
        >>> validate_probability(-0.1)  # Raises ValidationError
    """
    if not isinstance(p, (int, float)):
        raise ValidationError(
            f"{name} must be numeric, got {type(p).__name__}"
        )
    if not 0 <= p <= 1:
        raise ValidationError(
            f"{name} must be between 0 and 1, got {p}"
        )


def validate_range(
    low: Union[int, float],
    high: Union[int, float],
    name: str = "range"
) -> None:
    """Validate that low < high for a numeric range.
    
    Args:
        low: Lower bound of the range.
        high: Upper bound of the range.
        name: Parameter name for error messages.
    
    Raises:
        ValidationError: If low >= high.
    
    Examples:
        >>> validate_range(0, 10)  # OK
        >>> validate_range(0.0, 1.0)  # OK
        >>> validate_range(5, 5)  # Raises ValidationError
        >>> validate_range(10, 5)  # Raises ValidationError
    """
    if not isinstance(low, (int, float)):
        raise ValidationError(
            f"{name} lower bound must be numeric, got {type(low).__name__}"
        )
    if not isinstance(high, (int, float)):
        raise ValidationError(
            f"{name} upper bound must be numeric, got {type(high).__name__}"
        )
    if low >= high:
        raise ValidationError(
            f"{name} lower bound must be less than upper bound, got [{low}, {high}]"
        )
