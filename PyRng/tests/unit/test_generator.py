"""Unit tests for RandomGenerator class."""

import pytest
import numpy as np
from pyrng.core.generator import RandomGenerator
from pyrng.core.exceptions import GenerationError, DistributionError, ValidationError


class TestRandomGenerator:
    """Tests for RandomGenerator class."""
    
    def test_initialization_without_seed(self):
        """Test that generator initializes without seed."""
        gen = RandomGenerator()
        assert gen.seed is None
        assert gen.rng is not None
    
    def test_initialization_with_seed(self):
        """Test that generator initializes with seed."""
        gen = RandomGenerator(seed=42)
        assert gen.seed == 42
        assert gen.rng is not None
    
    def test_generate_with_valid_distribution(self):
        """Test generating samples from a valid distribution."""
        gen = RandomGenerator(seed=42)
        samples = gen.generate("uniform", 100, {"low": 0, "high": 10})
        
        assert len(samples) == 100
        assert all(0 <= x < 10 for x in samples)
    
    def test_generate_with_default_parameters(self):
        """Test generating samples with default parameters."""
        gen = RandomGenerator(seed=42)
        samples = gen.generate("uniform", 50)
        
        assert len(samples) == 50
        assert all(0 <= x < 1 for x in samples)
    
    def test_generate_with_unknown_distribution_raises_error(self):
        """Test that unknown distribution raises DistributionError."""
        gen = RandomGenerator()
        
        with pytest.raises(DistributionError, match="Unknown distribution"):
            gen.generate("unknown", 10)
    
    def test_generate_with_invalid_parameters_raises_error(self):
        """Test that invalid parameters raise ValidationError."""
        gen = RandomGenerator()
        
        with pytest.raises(ValidationError):
            gen.generate("uniform", 10, {"low": 10, "high": 5})
    
    def test_reproducibility_with_seed(self):
        """Test that same seed produces same results."""
        gen1 = RandomGenerator(seed=42)
        samples1 = gen1.generate("normal", 10, {"mu": 0, "sigma": 1})
        
        gen2 = RandomGenerator(seed=42)
        samples2 = gen2.generate("normal", 10, {"mu": 0, "sigma": 1})
        
        assert np.array_equal(samples1, samples2)
    
    def test_reset_seed(self):
        """Test resetting the seed."""
        gen = RandomGenerator(seed=42)
        samples1 = gen.generate("uniform", 10)
        
        gen.reset_seed(42)
        samples2 = gen.generate("uniform", 10)
        
        assert np.array_equal(samples1, samples2)
    
    def test_reset_seed_changes_output(self):
        """Test that resetting to different seed changes output."""
        gen = RandomGenerator(seed=42)
        samples1 = gen.generate("uniform", 10)
        
        gen.reset_seed(123)
        samples2 = gen.generate("uniform", 10)
        
        assert not np.array_equal(samples1, samples2)
    
    def test_get_state(self):
        """Test getting generator state."""
        gen = RandomGenerator(seed=42)
        state = gen.get_state()
        
        assert "seed" in state
        assert state["seed"] == 42
        assert "bit_generator" in state
    
    def test_repr(self):
        """Test string representation."""
        gen = RandomGenerator(seed=42)
        assert "RandomGenerator" in repr(gen)
        assert "seed=42" in repr(gen)
    
    def test_generate_multiple_distributions(self):
        """Test generating from multiple distributions sequentially."""
        gen = RandomGenerator(seed=42)
        
        uniform_samples = gen.generate("uniform", 10, {"low": 0, "high": 1})
        normal_samples = gen.generate("normal", 10, {"mu": 0, "sigma": 1})
        exponential_samples = gen.generate("exponential", 10, {"lam": 1.0})
        
        assert len(uniform_samples) == 10
        assert len(normal_samples) == 10
        assert len(exponential_samples) == 10
    
    def test_generate_large_sample_size(self):
        """Test generating large number of samples."""
        gen = RandomGenerator(seed=42)
        samples = gen.generate("normal", 100000, {"mu": 0, "sigma": 1})
        
        assert len(samples) == 100000
        # Statistical properties should hold for large samples
        assert abs(np.mean(samples)) < 0.05
        assert abs(np.std(samples) - 1.0) < 0.05
