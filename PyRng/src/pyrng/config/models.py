"""Configuration data models using Pydantic."""

from typing import Optional, Dict, Any, Literal
from pathlib import Path
from pydantic import BaseModel, Field, field_validator


class DistributionConfig(BaseModel):
    """Configuration for a specific distribution.
    
    Attributes:
        name: Distribution name (e.g., 'normal', 'uniform').
        parameters: Distribution-specific parameters.
    
    Examples:
        >>> config = DistributionConfig(name="normal", parameters={"mu": 0, "sigma": 1})
        >>> config.name
        'normal'
        >>> config.parameters
        {'mu': 0, 'sigma': 1}
    """
    
    name: str = Field(
        default="uniform",
        description="Distribution name"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Distribution parameters"
    )
    
    @field_validator("name")
    @classmethod
    def validate_distribution_name(cls, v: str) -> str:
        """Validate distribution name."""
        valid_distributions = [
            "uniform", "normal", "exponential", "binomial", "poisson"
        ]
        if v not in valid_distributions:
            raise ValueError(
                f"Invalid distribution '{v}'. "
                f"Must be one of: {', '.join(valid_distributions)}"
            )
        return v


class OutputConfig(BaseModel):
    """Configuration for output settings.
    
    Attributes:
        format: Output format (text, csv, json, binary).
        file_path: Optional output file path.
    
    Examples:
        >>> config = OutputConfig(format="csv", file_path="output.csv")
        >>> config.format
        'csv'
    """
    
    format: Literal["text", "csv", "json", "binary"] = Field(
        default="text",
        description="Output format"
    )
    file_path: Optional[str] = Field(
        default=None,
        description="Output file path (None for stdout)"
    )


class GenerationConfig(BaseModel):
    """Configuration for number generation.
    
    Attributes:
        count: Number of samples to generate.
        seed: Random seed for reproducibility.
    
    Examples:
        >>> config = GenerationConfig(count=100, seed=42)
        >>> config.count
        100
        >>> config.seed
        42
    """
    
    count: int = Field(
        default=100,
        gt=0,
        description="Number of samples to generate"
    )
    seed: Optional[int] = Field(
        default=None,
        description="Random seed for reproducibility"
    )


class PyRngConfig(BaseModel):
    """Main configuration model for PyRng.
    
    Attributes:
        generation: Generation settings (count, seed).
        distribution: Distribution settings.
        output: Output settings.
        verbose: Enable verbose logging.
    
    Examples:
        >>> config = PyRngConfig()
        >>> config.generation.count
        100
        >>> config.distribution.name
        'uniform'
    """
    
    generation: GenerationConfig = Field(
        default_factory=GenerationConfig,
        description="Generation settings"
    )
    distribution: DistributionConfig = Field(
        default_factory=DistributionConfig,
        description="Distribution settings"
    )
    output: OutputConfig = Field(
        default_factory=OutputConfig,
        description="Output settings"
    )
    verbose: bool = Field(
        default=False,
        description="Enable verbose logging"
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of the configuration.
        
        Examples:
            >>> config = PyRngConfig()
            >>> isinstance(config.to_dict(), dict)
            True
        """
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PyRngConfig":
        """Create configuration from dictionary.
        
        Args:
            data: Dictionary with configuration data.
        
        Returns:
            PyRngConfig instance.
        
        Examples:
            >>> data = {"generation": {"count": 50}}
            >>> config = PyRngConfig.from_dict(data)
            >>> config.generation.count
            50
        """
        return cls(**data)
