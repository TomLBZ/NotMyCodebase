"""Abstract base class for output formatters."""

from abc import ABC, abstractmethod
import numpy as np
from typing import Any


class OutputFormatter(ABC):
    """Abstract base class for output format implementations.
    
    All output formatters must inherit from this class and implement
    the required abstract methods.
    """
    
    @abstractmethod
    def format(self, data: np.ndarray) -> Any:
        """Format the data for output.
        
        Args:
            data: NumPy array of generated samples.
        
        Returns:
            Formatted data (type depends on formatter implementation).
        """
        pass
    
    @abstractmethod
    def get_extension(self) -> str:
        """Get the file extension for this format.
        
        Returns:
            File extension (e.g., ".txt", ".csv", ".json").
        """
        pass
