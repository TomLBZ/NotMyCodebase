"""Continuous probability distributions."""

import numpy as np
from dataclasses import dataclass

from pyrng.distributions.base import Distribution
from pyrng.core.exceptions import ValidationError
from pyrng.utils.validation import validate_sample_size, validate_positive, validate_range


@dataclass
class UniformDistribution(Distribution):
    """Uniform distribution U(low, high).
    
    Generates random numbers uniformly distributed between low (inclusive)
    and high (exclusive).
    
    Attributes:
        low: Lower bound (inclusive). Default: 0.0.
        high: Upper bound (exclusive). Default: 1.0.
    
    Examples:
        >>> rng = np.random.default_rng(seed=42)
        >>> dist = UniformDistribution(low=0.0, high=10.0)
        >>> samples = dist.sample(size=5, rng=rng)
        >>> len(samples)
        5
        >>> all(0.0 <= x < 10.0 for x in samples)
        True
    """
    
    low: float = 0.0
    high: float = 1.0
    
    def __post_init__(self) -> None:
        """Validate parameters after initialization."""
        self.validate_parameters()
    
    def validate_parameters(self) -> None:
        """Validate that low < high.
        
        Raises:
            ValidationError: If low >= high.
        """
        validate_range(self.low, self.high, "uniform distribution range")
    
    def sample(self, size: int, rng: np.random.Generator) -> np.ndarray:
        """Generate samples from uniform distribution.
        
        Args:
            size: Number of samples to generate.
            rng: NumPy random generator instance.
        
        Returns:
            Array of uniformly distributed samples.
        
        Raises:
            ValidationError: If size is invalid.
        """
        validate_sample_size(size)
        return rng.uniform(self.low, self.high, size)


@dataclass
class NormalDistribution(Distribution):
    """Normal (Gaussian) distribution N(mu, sigma²).
    
    Generates random numbers from a normal distribution with specified
    mean and standard deviation.
    
    Attributes:
        mu: Mean (location parameter). Default: 0.0.
        sigma: Standard deviation (scale parameter). Must be positive. Default: 1.0.
    
    Examples:
        >>> rng = np.random.default_rng(seed=42)
        >>> dist = NormalDistribution(mu=100, sigma=15)
        >>> samples = dist.sample(size=10000, rng=rng)
        >>> abs(np.mean(samples) - 100) < 1.0  # Close to mean
        True
        >>> abs(np.std(samples) - 15) < 1.0  # Close to std dev
        True
    """
    
    mu: float = 0.0
    sigma: float = 1.0
    
    def __post_init__(self) -> None:
        """Validate parameters after initialization."""
        self.validate_parameters()
    
    def validate_parameters(self) -> None:
        """Validate that sigma > 0.
        
        Raises:
            ValidationError: If sigma is not positive.
        """
        validate_positive(self.sigma, "sigma (standard deviation)")
    
    def sample(self, size: int, rng: np.random.Generator) -> np.ndarray:
        """Generate samples from normal distribution.
        
        Args:
            size: Number of samples to generate.
            rng: NumPy random generator instance.
        
        Returns:
            Array of normally distributed samples.
        
        Raises:
            ValidationError: If size is invalid.
        """
        validate_sample_size(size)
        return rng.normal(self.mu, self.sigma, size)


@dataclass
class ExponentialDistribution(Distribution):
    """Exponential distribution Exp(lambda).
    
    Generates random numbers from an exponential distribution with
    specified rate parameter (lambda).
    
    Attributes:
        lam: Rate parameter (lambda). Must be positive. Default: 1.0.
    
    Note:
        The parameter is named 'lam' instead of 'lambda' because 'lambda'
        is a Python keyword.
    
    Examples:
        >>> rng = np.random.default_rng(seed=42)
        >>> dist = ExponentialDistribution(lam=2.0)
        >>> samples = dist.sample(size=10000, rng=rng)
        >>> abs(np.mean(samples) - 0.5) < 0.1  # Mean = 1/lambda
        True
    """
    
    lam: float = 1.0
    
    def __post_init__(self) -> None:
        """Validate parameters after initialization."""
        self.validate_parameters()
    
    def validate_parameters(self) -> None:
        """Validate that lambda > 0.
        
        Raises:
            ValidationError: If lambda is not positive.
        """
        validate_positive(self.lam, "lambda (rate parameter)")
    
    def sample(self, size: int, rng: np.random.Generator) -> np.ndarray:
        """Generate samples from exponential distribution.
        
        Args:
            size: Number of samples to generate.
            rng: NumPy random generator instance.
        
        Returns:
            Array of exponentially distributed samples.
        
        Raises:
            ValidationError: If size is invalid.
        
        Note:
            NumPy's exponential uses scale parameter (1/lambda), not rate.
        """
        validate_sample_size(size)
        # NumPy uses scale = 1/lambda
        scale = 1.0 / self.lam
        return rng.exponential(scale, size)
