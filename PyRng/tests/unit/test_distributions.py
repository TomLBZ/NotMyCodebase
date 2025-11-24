"""Unit tests for distribution implementations."""

import pytest
import numpy as np
from pyrng.distributions.continuous import (
    UniformDistribution,
    NormalDistribution,
    ExponentialDistribution,
)
from pyrng.distributions.discrete import (
    BinomialDistribution,
    PoissonDistribution,
)
from pyrng.core.exceptions import ValidationError


class TestUniformDistribution:
    """Tests for UniformDistribution."""
    
    def test_initialization_with_defaults(self):
        """Test that distribution initializes with default parameters."""
        dist = UniformDistribution()
        assert dist.low == 0.0
        assert dist.high == 1.0
    
    def test_initialization_with_custom_parameters(self):
        """Test initialization with custom parameters."""
        dist = UniformDistribution(low=5.0, high=10.0)
        assert dist.low == 5.0
        assert dist.high == 10.0
    
    def test_invalid_range_raises_error(self):
        """Test that low >= high raises ValidationError."""
        with pytest.raises(ValidationError):
            UniformDistribution(low=10.0, high=5.0)
        
        with pytest.raises(ValidationError):
            UniformDistribution(low=5.0, high=5.0)
    
    def test_sample_generation(self, default_rng):
        """Test that samples are generated correctly."""
        dist = UniformDistribution(low=0.0, high=10.0)
        samples = dist.sample(100, default_rng)
        
        assert len(samples) == 100
        assert all(0.0 <= x < 10.0 for x in samples)
    
    def test_sample_statistics(self, default_rng):
        """Test that sample statistics are reasonable."""
        dist = UniformDistribution(low=0.0, high=10.0)
        samples = dist.sample(10000, default_rng)
        
        # Mean should be approximately (low + high) / 2
        assert abs(np.mean(samples) - 5.0) < 0.2
    
    def test_repr(self):
        """Test string representation."""
        dist = UniformDistribution(low=0, high=10)
        assert "UniformDistribution" in repr(dist)
        assert "low=0" in repr(dist)
        assert "high=10" in repr(dist)


class TestNormalDistribution:
    """Tests for NormalDistribution."""
    
    def test_initialization_with_defaults(self):
        """Test that distribution initializes with default parameters."""
        dist = NormalDistribution()
        assert dist.mu == 0.0
        assert dist.sigma == 1.0
    
    def test_initialization_with_custom_parameters(self):
        """Test initialization with custom parameters."""
        dist = NormalDistribution(mu=100.0, sigma=15.0)
        assert dist.mu == 100.0
        assert dist.sigma == 15.0
    
    def test_invalid_sigma_raises_error(self):
        """Test that sigma <= 0 raises ValidationError."""
        with pytest.raises(ValidationError):
            NormalDistribution(mu=0, sigma=0)
        
        with pytest.raises(ValidationError):
            NormalDistribution(mu=0, sigma=-1.0)
    
    def test_sample_generation(self, default_rng):
        """Test that samples are generated correctly."""
        dist = NormalDistribution(mu=0, sigma=1)
        samples = dist.sample(100, default_rng)
        
        assert len(samples) == 100
    
    def test_sample_statistics(self, default_rng):
        """Test that sample statistics match parameters."""
        dist = NormalDistribution(mu=100, sigma=15)
        samples = dist.sample(10000, default_rng)
        
        # Mean and std dev should be close to parameters
        assert abs(np.mean(samples) - 100) < 1.0
        assert abs(np.std(samples) - 15) < 1.0


class TestExponentialDistribution:
    """Tests for ExponentialDistribution."""
    
    def test_initialization_with_defaults(self):
        """Test that distribution initializes with default parameters."""
        dist = ExponentialDistribution()
        assert dist.lam == 1.0
    
    def test_initialization_with_custom_parameter(self):
        """Test initialization with custom lambda."""
        dist = ExponentialDistribution(lam=2.0)
        assert dist.lam == 2.0
    
    def test_invalid_lambda_raises_error(self):
        """Test that lambda <= 0 raises ValidationError."""
        with pytest.raises(ValidationError):
            ExponentialDistribution(lam=0)
        
        with pytest.raises(ValidationError):
            ExponentialDistribution(lam=-1.0)
    
    def test_sample_generation(self, default_rng):
        """Test that samples are generated correctly."""
        dist = ExponentialDistribution(lam=1.0)
        samples = dist.sample(100, default_rng)
        
        assert len(samples) == 100
        assert all(x >= 0 for x in samples)
    
    def test_sample_statistics(self, default_rng):
        """Test that sample statistics match expected values."""
        dist = ExponentialDistribution(lam=2.0)
        samples = dist.sample(10000, default_rng)
        
        # Mean should be approximately 1/lambda
        expected_mean = 1.0 / 2.0
        assert abs(np.mean(samples) - expected_mean) < 0.1


class TestBinomialDistribution:
    """Tests for BinomialDistribution."""
    
    def test_initialization_with_defaults(self):
        """Test that distribution initializes with default parameters."""
        dist = BinomialDistribution()
        assert dist.n == 10
        assert dist.p == 0.5
    
    def test_initialization_with_custom_parameters(self):
        """Test initialization with custom parameters."""
        dist = BinomialDistribution(n=20, p=0.3)
        assert dist.n == 20
        assert dist.p == 0.3
    
    def test_invalid_n_raises_error(self):
        """Test that invalid n raises ValidationError."""
        with pytest.raises(ValidationError):
            BinomialDistribution(n=0, p=0.5)
        
        with pytest.raises(ValidationError):
            BinomialDistribution(n=-5, p=0.5)
    
    def test_invalid_p_raises_error(self):
        """Test that invalid p raises ValidationError."""
        with pytest.raises(ValidationError):
            BinomialDistribution(n=10, p=1.5)
        
        with pytest.raises(ValidationError):
            BinomialDistribution(n=10, p=-0.1)
    
    def test_sample_generation(self, default_rng):
        """Test that samples are generated correctly."""
        dist = BinomialDistribution(n=10, p=0.5)
        samples = dist.sample(100, default_rng)
        
        assert len(samples) == 100
        assert all(0 <= x <= 10 for x in samples)
        assert all(isinstance(x, (int, np.integer)) for x in samples)
    
    def test_sample_statistics(self, default_rng):
        """Test that sample statistics match expected values."""
        dist = BinomialDistribution(n=20, p=0.5)
        samples = dist.sample(10000, default_rng)
        
        # Mean should be approximately n * p
        expected_mean = 20 * 0.5
        assert abs(np.mean(samples) - expected_mean) < 0.5


class TestPoissonDistribution:
    """Tests for PoissonDistribution."""
    
    def test_initialization_with_defaults(self):
        """Test that distribution initializes with default parameters."""
        dist = PoissonDistribution()
        assert dist.lam == 1.0
    
    def test_initialization_with_custom_parameter(self):
        """Test initialization with custom lambda."""
        dist = PoissonDistribution(lam=5.0)
        assert dist.lam == 5.0
    
    def test_invalid_lambda_raises_error(self):
        """Test that lambda <= 0 raises ValidationError."""
        with pytest.raises(ValidationError):
            PoissonDistribution(lam=0)
        
        with pytest.raises(ValidationError):
            PoissonDistribution(lam=-1.0)
    
    def test_sample_generation(self, default_rng):
        """Test that samples are generated correctly."""
        dist = PoissonDistribution(lam=5.0)
        samples = dist.sample(100, default_rng)
        
        assert len(samples) == 100
        assert all(x >= 0 for x in samples)
        assert all(isinstance(x, (int, np.integer)) for x in samples)
    
    def test_sample_statistics(self, default_rng):
        """Test that sample statistics match expected values."""
        dist = PoissonDistribution(lam=10.0)
        samples = dist.sample(10000, default_rng)
        
        # Mean should be approximately lambda
        assert abs(np.mean(samples) - 10.0) < 0.5
        # Variance should be approximately lambda
        assert abs(np.var(samples) - 10.0) < 1.0
