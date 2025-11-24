"""Discrete probability distributions."""

import numpy as np
from dataclasses import dataclass

from pyrng.distributions.base import Distribution
from pyrng.core.exceptions import ValidationError
from pyrng.utils.validation import (
    validate_sample_size,
    validate_positive,
    validate_probability,
)


@dataclass
class BinomialDistribution(Distribution):
    """Binomial distribution B(n, p).
    
    Generates random numbers representing the number of successes in n
    independent Bernoulli trials with probability p.
    
    Attributes:
        n: Number of trials. Must be positive integer. Default: 10.
        p: Probability of success per trial. Must be in [0, 1]. Default: 0.5.
    
    Examples:
        >>> rng = np.random.default_rng(seed=42)
        >>> dist = BinomialDistribution(n=10, p=0.5)
        >>> samples = dist.sample(size=1000, rng=rng)
        >>> all(0 <= x <= 10 for x in samples)  # All values in [0, n]
        True
        >>> abs(np.mean(samples) - 5.0) < 0.5  # Mean = n*p
        True
    """
    
    n: int = 10
    p: float = 0.5
    
    def __post_init__(self) -> None:
        """Validate parameters after initialization."""
        self.validate_parameters()
    
    def validate_parameters(self) -> None:
        """Validate that n > 0 and 0 <= p <= 1.
        
        Raises:
            ValidationError: If parameters are invalid.
        """
        if not isinstance(self.n, int):
            raise ValidationError(
                f"n (trials) must be an integer, got {type(self.n).__name__}"
            )
        if self.n <= 0:
            raise ValidationError(
                f"n (trials) must be positive, got {self.n}"
            )
        validate_probability(self.p, "p (success probability)")
    
    def sample(self, size: int, rng: np.random.Generator) -> np.ndarray:
        """Generate samples from binomial distribution.
        
        Args:
            size: Number of samples to generate.
            rng: NumPy random generator instance.
        
        Returns:
            Array of binomially distributed samples (integers).
        
        Raises:
            ValidationError: If size is invalid.
        """
        validate_sample_size(size)
        return rng.binomial(self.n, self.p, size)


@dataclass
class PoissonDistribution(Distribution):
    """Poisson distribution Pois(lambda).
    
    Generates random numbers representing the number of events occurring
    in a fixed interval when events occur at a constant mean rate lambda.
    
    Attributes:
        lam: Rate parameter (lambda). Must be positive. Default: 1.0.
    
    Note:
        The parameter is named 'lam' instead of 'lambda' because 'lambda'
        is a Python keyword.
    
    Examples:
        >>> rng = np.random.default_rng(seed=42)
        >>> dist = PoissonDistribution(lam=5.0)
        >>> samples = dist.sample(size=10000, rng=rng)
        >>> abs(np.mean(samples) - 5.0) < 0.2  # Mean = lambda
        True
        >>> abs(np.var(samples) - 5.0) < 0.5  # Variance = lambda
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
        """Generate samples from Poisson distribution.
        
        Args:
            size: Number of samples to generate.
            rng: NumPy random generator instance.
        
        Returns:
            Array of Poisson distributed samples (integers).
        
        Raises:
            ValidationError: If size is invalid.
        """
        validate_sample_size(size)
        return rng.poisson(self.lam, size)
