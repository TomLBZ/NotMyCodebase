"""Distribution factory for creating distribution instances."""

from typing import Dict, Type, Any, List
import logging

from pyrng.distributions.base import Distribution
from pyrng.distributions.continuous import (
    UniformDistribution,
    NormalDistribution,
    ExponentialDistribution,
)
from pyrng.distributions.discrete import (
    BinomialDistribution,
    PoissonDistribution,
)
from pyrng.core.exceptions import DistributionError

logger = logging.getLogger(__name__)


class DistributionFactory:
    """Factory for creating distribution instances.
    
    This class maintains a registry of available distributions and
    provides a unified interface for creating them by name. It uses
    the factory pattern to decouple distribution creation from usage.
    
    Examples:
        >>> DistributionFactory.register("uniform", UniformDistribution)
        >>> dist = DistributionFactory.create("uniform", low=0, high=10)
        >>> type(dist).__name__
        'UniformDistribution'
    """
    
    _registry: Dict[str, Type[Distribution]] = {}
    
    @classmethod
    def register(
        cls,
        name: str,
        distribution_class: Type[Distribution]
    ) -> None:
        """Register a distribution type.
        
        Args:
            name: Name to register the distribution under (case-insensitive).
            distribution_class: Distribution class to register.
        
        Examples:
            >>> DistributionFactory.register("custom", CustomDistribution)
        """
        name_lower = name.lower()
        cls._registry[name_lower] = distribution_class
        logger.debug(f"Registered distribution: {name_lower}")
    
    @classmethod
    def create(cls, name: str, **kwargs: Any) -> Distribution:
        """Create a distribution instance by name.
        
        Args:
            name: Name of the distribution to create (case-insensitive).
            **kwargs: Distribution-specific parameters.
        
        Returns:
            Distribution instance configured with the provided parameters.
        
        Raises:
            DistributionError: If distribution name is not registered.
        
        Examples:
            >>> dist = DistributionFactory.create("normal", mu=0, sigma=1)
            >>> dist = DistributionFactory.create("uniform", low=0, high=100)
        """
        name_lower = name.lower()
        
        if name_lower not in cls._registry:
            available = ", ".join(sorted(cls._registry.keys()))
            raise DistributionError(
                f"Unknown distribution: '{name}'. "
                f"Available distributions: {available}"
            )
        
        distribution_class = cls._registry[name_lower]
        logger.debug(f"Creating distribution: {name_lower} with parameters {kwargs}")
        
        try:
            return distribution_class(**kwargs)
        except TypeError as e:
            raise DistributionError(
                f"Invalid parameters for distribution '{name}': {e}"
            ) from e
    
    @classmethod
    def list_distributions(cls) -> List[str]:
        """Get list of registered distribution names.
        
        Returns:
            Sorted list of distribution names.
        
        Examples:
            >>> dists = DistributionFactory.list_distributions()
            >>> "normal" in dists
            True
        """
        return sorted(cls._registry.keys())
    
    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Check if a distribution name is registered.
        
        Args:
            name: Distribution name to check (case-insensitive).
        
        Returns:
            True if the distribution is registered, False otherwise.
        
        Examples:
            >>> DistributionFactory.is_registered("normal")
            True
            >>> DistributionFactory.is_registered("unknown")
            False
        """
        return name.lower() in cls._registry


# Register built-in distributions
DistributionFactory.register("uniform", UniformDistribution)
DistributionFactory.register("normal", NormalDistribution)
DistributionFactory.register("exponential", ExponentialDistribution)
DistributionFactory.register("binomial", BinomialDistribution)
DistributionFactory.register("poisson", PoissonDistribution)

logger.debug(f"Registered {len(DistributionFactory._registry)} built-in distributions")
