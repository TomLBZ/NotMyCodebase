"""Abstract base class for probability distributions."""

from abc import ABC, abstractmethod
import numpy as np
from typing import Any


class Distribution(ABC):
    """Abstract base class for probability distributions.
    
    All distribution implementations must inherit from this class
    and implement the required abstract methods.
    
    This class defines the interface that all distributions must follow,
    ensuring consistency and enabling polymorphic usage.
    """
    
    @abstractmethod
    def sample(self, size: int, rng: np.random.Generator) -> np.ndarray:
        """Generate samples from this distribution.
        
        Args:
            size: Number of samples to generate. Must be positive.
            rng: NumPy random generator instance for reproducible generation.
        
        Returns:
            NumPy array of samples with length equal to size.
        
        Raises:
            ValidationError: If size is invalid.
            GenerationError: If sample generation fails.
        """
        pass
    
    @abstractmethod
    def validate_parameters(self) -> None:
        """Validate distribution parameters.
        
        This method should check that all parameters are valid for the
        specific distribution. It is called during initialization.
        
        Raises:
            ValidationError: If any parameters are invalid.
        """
        pass
    
    def __repr__(self) -> str:
        """String representation of the distribution.
        
        Returns:
            String showing the distribution class name and parameters.
        
        Examples:
            >>> dist = UniformDistribution(0, 1)
            >>> repr(dist)
            'UniformDistribution(low=0, high=1)'
        """
        params = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({params})"
