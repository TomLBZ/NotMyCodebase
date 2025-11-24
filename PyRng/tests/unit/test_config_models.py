"""Tests for configuration models."""

import pytest
from pydantic import ValidationError

from pyrng.config.models import (
    DistributionConfig,
    OutputConfig,
    GenerationConfig,
    PyRngConfig,
)


class TestDistributionConfig:
    """Tests for DistributionConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = DistributionConfig()
        assert config.name == "uniform"
        assert config.parameters == {}
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = DistributionConfig(
            name="normal",
            parameters={"mu": 0, "sigma": 1}
        )
        assert config.name == "normal"
        assert config.parameters == {"mu": 0, "sigma": 1}
    
    def test_invalid_distribution_name(self):
        """Test that invalid distribution names are rejected."""
        with pytest.raises(ValidationError):
            DistributionConfig(name="invalid_distribution")
    
    def test_valid_distribution_names(self):
        """Test all valid distribution names."""
        valid_names = ["uniform", "normal", "exponential", "binomial", "poisson"]
        for name in valid_names:
            config = DistributionConfig(name=name)
            assert config.name == name


class TestOutputConfig:
    """Tests for OutputConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = OutputConfig()
        assert config.format == "text"
        assert config.file_path is None
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = OutputConfig(format="csv", file_path="/tmp/output.csv")
        assert config.format == "csv"
        assert config.file_path == "/tmp/output.csv"
    
    def test_valid_formats(self):
        """Test all valid output formats."""
        valid_formats = ["text", "csv", "json", "binary"]
        for fmt in valid_formats:
            config = OutputConfig(format=fmt)
            assert config.format == fmt


class TestGenerationConfig:
    """Tests for GenerationConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = GenerationConfig()
        assert config.count == 100
        assert config.seed is None
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = GenerationConfig(count=1000, seed=42)
        assert config.count == 1000
        assert config.seed == 42
    
    def test_positive_count_validation(self):
        """Test that count must be positive."""
        with pytest.raises(ValidationError):
            GenerationConfig(count=0)
        
        with pytest.raises(ValidationError):
            GenerationConfig(count=-10)


class TestPyRngConfig:
    """Tests for PyRngConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = PyRngConfig()
        assert config.generation.count == 100
        assert config.distribution.name == "uniform"
        assert config.output.format == "text"
        assert config.verbose is False
    
    def test_nested_configuration(self):
        """Test nested configuration objects."""
        config = PyRngConfig(
            generation=GenerationConfig(count=500, seed=42),
            distribution=DistributionConfig(
                name="normal",
                parameters={"mu": 10, "sigma": 2}
            ),
            output=OutputConfig(format="json", file_path="output.json")
        )
        
        assert config.generation.count == 500
        assert config.generation.seed == 42
        assert config.distribution.name == "normal"
        assert config.distribution.parameters == {"mu": 10, "sigma": 2}
        assert config.output.format == "json"
        assert config.output.file_path == "output.json"
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = PyRngConfig()
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert "generation" in config_dict
        assert "distribution" in config_dict
        assert "output" in config_dict
        assert "verbose" in config_dict
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "generation": {"count": 200, "seed": 123},
            "distribution": {"name": "exponential", "parameters": {"lam": 1.5}},
            "output": {"format": "csv", "file_path": "test.csv"},
            "verbose": True
        }
        
        config = PyRngConfig.from_dict(data)
        
        assert config.generation.count == 200
        assert config.generation.seed == 123
        assert config.distribution.name == "exponential"
        assert config.distribution.parameters == {"lam": 1.5}
        assert config.output.format == "csv"
        assert config.output.file_path == "test.csv"
        assert config.verbose is True
    
    def test_round_trip(self):
        """Test that to_dict and from_dict are inverses."""
        original = PyRngConfig(
            generation=GenerationConfig(count=300, seed=99),
            distribution=DistributionConfig(name="poisson", parameters={"lam": 5})
        )
        
        # Convert to dict and back
        config_dict = original.to_dict()
        restored = PyRngConfig.from_dict(config_dict)
        
        assert restored.generation.count == original.generation.count
        assert restored.generation.seed == original.generation.seed
        assert restored.distribution.name == original.distribution.name
        assert restored.distribution.parameters == original.distribution.parameters
