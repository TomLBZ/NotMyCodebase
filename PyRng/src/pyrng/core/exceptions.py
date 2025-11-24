"""Custom exception hierarchy for PyRng."""


class PyRngError(Exception):
    """Base exception for all PyRng errors.
    
    All custom exceptions in PyRng inherit from this class.
    """
    
    pass


class ValidationError(PyRngError):
    """Raised when input validation fails.
    
    This exception is raised when parameters, arguments, or configuration
    values fail validation checks.
    
    Examples:
        >>> if size <= 0:
        ...     raise ValidationError(f"Sample size must be positive, got {size}")
    """
    
    pass


class DistributionError(PyRngError):
    """Raised when a distribution operation fails.
    
    This exception is raised for distribution-specific errors such as
    unknown distribution names or invalid distribution parameters.
    
    Examples:
        >>> if name not in registry:
        ...     raise DistributionError(f"Unknown distribution: {name}")
    """
    
    pass


class OutputError(PyRngError):
    """Raised when output formatting or writing fails.
    
    This exception is raised when operations related to output formatting,
    file writing, or serialization fail.
    
    Examples:
        >>> if not output_path.parent.exists():
        ...     raise OutputError(f"Output directory does not exist: {output_path.parent}")
    """
    
    pass


class ConfigurationError(PyRngError):
    """Raised when configuration loading or validation fails.
    
    This exception is raised when configuration files are invalid, missing
    required fields, or contain incompatible values.
    
    Examples:
        >>> if "distribution" not in config:
        ...     raise ConfigurationError("Missing required field: distribution")
    """
    
    pass


class GenerationError(PyRngError):
    """Raised when random number generation fails.
    
    This exception is raised when the random number generation process
    encounters an error that prevents sample creation.
    
    Examples:
        >>> try:
        ...     samples = dist.sample(size, rng)
        ... except Exception as e:
        ...     raise GenerationError(f"Generation failed: {e}") from e
    """
    
    pass
