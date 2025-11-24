"""Core random number generator."""

import numpy as np
from typing import Optional, Dict, Any
import logging

from pyrng.distributions.base import Distribution
from pyrng.core.factory import DistributionFactory
from pyrng.core.exceptions import GenerationError, ValidationError, DistributionError

logger = logging.getLogger(__name__)


class RandomGenerator:
    """Main random number generator class.
    
    This class provides a unified interface for generating random numbers
    from various probability distributions. It manages the random number
    generator state and provides reproducibility through seeding.
    
    Attributes:
        seed: Random seed for reproducibility (if set).
        rng: NumPy random generator instance.
    
    Examples:
        >>> gen = RandomGenerator(seed=42)
        >>> samples = gen.generate("normal", 1000, {"mu": 0, "sigma": 1})
        >>> len(samples)
        1000
        
        >>> # Generate uniform distribution
        >>> samples = gen.generate("uniform", 100, {"low": 0, "high": 10})
        >>> all(0 <= x < 10 for x in samples)
        True
    """
    
    def __init__(self, seed: Optional[int] = None) -> None:
        """Initialize the random generator.
        
        Args:
            seed: Random seed for reproducibility. If None, uses system entropy.
        
        Examples:
            >>> gen = RandomGenerator()  # Random seed
            >>> gen = RandomGenerator(seed=42)  # Fixed seed
        """
        self.seed = seed
        self.rng = np.random.default_rng(seed=seed)
        logger.debug(f"Initialized RandomGenerator with seed={seed}")
    
    def generate(
        self,
        distribution: str,
        count: int,
        parameters: Optional[Dict[str, Any]] = None
    ) -> np.ndarray:
        """Generate random samples from a distribution.
        
        Args:
            distribution: Name of the distribution (e.g., "normal", "uniform").
            count: Number of samples to generate. Must be positive.
            parameters: Distribution-specific parameters. If None, uses defaults.
        
        Returns:
            NumPy array of generated samples with length equal to count.
        
        Raises:
            GenerationError: If generation fails.
            ValidationError: If parameters are invalid.
            DistributionError: If distribution name is unknown.
        
        Examples:
            >>> gen = RandomGenerator(seed=42)
            >>> samples = gen.generate("normal", 5, {"mu": 0, "sigma": 1})
            >>> len(samples)
            5
            
            >>> # With default parameters
            >>> samples = gen.generate("uniform", 10)
            >>> len(samples)
            10
        """
        try:
            # Create distribution instance
            params = parameters or {}
            dist = DistributionFactory.create(distribution, **params)
            
            # Generate samples
            logger.debug(
                f"Generating {count} samples from {distribution} "
                f"with parameters {params}"
            )
            samples = dist.sample(size=count, rng=self.rng)
            
            logger.info(
                f"Successfully generated {len(samples)} samples "
                f"from {distribution} distribution"
            )
            
            return samples
            
        except (ValidationError, DistributionError, GenerationError):
            # Re-raise PyRng exceptions as-is
            raise
        except Exception as e:
            # Wrap unexpected exceptions
            raise GenerationError(
                f"Failed to generate samples from {distribution}: {e}"
            ) from e
    
    def reset_seed(self, seed: Optional[int] = None) -> None:
        """Reset the random generator with a new seed.
        
        This method creates a new random generator with the specified seed,
        allowing you to reset the random state or switch to a different seed.
        
        Args:
            seed: New random seed. If None, uses system entropy.
        
        Examples:
            >>> gen = RandomGenerator(seed=42)
            >>> samples1 = gen.generate("uniform", 5)
            >>> gen.reset_seed(42)  # Reset to same seed
            >>> samples2 = gen.generate("uniform", 5)
            >>> np.array_equal(samples1, samples2)
            True
        """
        self.seed = seed
        self.rng = np.random.default_rng(seed=seed)
        logger.debug(f"Reset RandomGenerator with seed={seed}")
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the random generator.
        
        Returns:
            Dictionary containing the generator state including seed.
        
        Examples:
            >>> gen = RandomGenerator(seed=42)
            >>> state = gen.get_state()
            >>> state["seed"]
            42
        """
        return {
            "seed": self.seed,
            "bit_generator": self.rng.bit_generator.state,
        }
    
    def __repr__(self) -> str:
        """String representation of the generator.
        
        Returns:
            String showing the generator configuration.
        
        Examples:
            >>> gen = RandomGenerator(seed=42)
            >>> repr(gen)
            'RandomGenerator(seed=42)'
        """
        return f"RandomGenerator(seed={self.seed})"
