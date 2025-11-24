"""Unit tests for DistributionFactory."""

import pytest
from pyrng.core.factory import DistributionFactory
from pyrng.distributions.continuous import UniformDistribution, NormalDistribution
from pyrng.core.exceptions import DistributionError


class TestDistributionFactory:
    """Tests for DistributionFactory class."""
    
    def test_list_distributions(self):
        """Test that built-in distributions are registered."""
        dists = DistributionFactory.list_distributions()
        
        assert "uniform" in dists
        assert "normal" in dists
        assert "exponential" in dists
        assert "binomial" in dists
        assert "poisson" in dists
    
    def test_is_registered_for_known_distribution(self):
        """Test that is_registered returns True for known distributions."""
        assert DistributionFactory.is_registered("uniform")
        assert DistributionFactory.is_registered("normal")
        assert DistributionFactory.is_registered("UNIFORM")  # Case insensitive
    
    def test_is_registered_for_unknown_distribution(self):
        """Test that is_registered returns False for unknown distributions."""
        assert not DistributionFactory.is_registered("unknown")
        assert not DistributionFactory.is_registered("custom")
    
    def test_create_uniform_distribution(self):
        """Test creating uniform distribution."""
        dist = DistributionFactory.create("uniform", low=0, high=10)
        
        assert isinstance(dist, UniformDistribution)
        assert dist.low == 0
        assert dist.high == 10
    
    def test_create_normal_distribution(self):
        """Test creating normal distribution."""
        dist = DistributionFactory.create("normal", mu=100, sigma=15)
        
        assert isinstance(dist, NormalDistribution)
        assert dist.mu == 100
        assert dist.sigma == 15
    
    def test_create_with_case_insensitive_name(self):
        """Test that distribution names are case-insensitive."""
        dist1 = DistributionFactory.create("UNIFORM", low=0, high=1)
        dist2 = DistributionFactory.create("Uniform", low=0, high=1)
        dist3 = DistributionFactory.create("uniform", low=0, high=1)
        
        assert type(dist1) == type(dist2) == type(dist3)
    
    def test_create_unknown_distribution_raises_error(self):
        """Test that creating unknown distribution raises DistributionError."""
        with pytest.raises(DistributionError, match="Unknown distribution"):
            DistributionFactory.create("unknown")
    
    def test_create_with_invalid_parameters_raises_error(self):
        """Test that invalid parameters raise DistributionError."""
        with pytest.raises(DistributionError, match="Invalid parameters"):
            DistributionFactory.create("uniform", invalid_param=10)
    
    def test_create_with_default_parameters(self):
        """Test creating distribution with default parameters."""
        dist = DistributionFactory.create("uniform")
        
        assert isinstance(dist, UniformDistribution)
        assert dist.low == 0.0
        assert dist.high == 1.0
    
    def test_error_message_includes_available_distributions(self):
        """Test that error message lists available distributions."""
        try:
            DistributionFactory.create("unknown")
        except DistributionError as e:
            error_msg = str(e)
            assert "uniform" in error_msg
            assert "normal" in error_msg
            assert "Available distributions" in error_msg
