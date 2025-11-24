"""Tests for configuration file loading and saving."""

import json
import pytest
from pathlib import Path

from pyrng.config.loader import ConfigLoader, merge_config_with_args
from pyrng.config.models import PyRngConfig, GenerationConfig, DistributionConfig
from pyrng.core.exceptions import ConfigurationError


class TestConfigLoader:
    """Tests for ConfigLoader."""
    
    def test_load_nonexistent_returns_defaults(self, tmp_path):
        """Test that loading from nonexistent file returns defaults."""
        config_path = tmp_path / "nonexistent.json"
        loader = ConfigLoader(config_path=config_path)
        
        config = loader.load()
        
        assert isinstance(config, PyRngConfig)
        assert config.generation.count == 100  # Default value
        assert config.distribution.name == "uniform"  # Default value
    
    def test_save_and_load(self, tmp_path):
        """Test saving and loading configuration."""
        config_path = tmp_path / "test_config.json"
        loader = ConfigLoader(config_path=config_path)
        
        # Create custom config
        config = PyRngConfig(
            generation=GenerationConfig(count=500, seed=42),
            distribution=DistributionConfig(
                name="normal",
                parameters={"mu": 10, "sigma": 2}
            )
        )
        
        # Save
        saved_path = loader.save(config)
        assert saved_path == config_path
        assert config_path.exists()
        
        # Load
        loaded_config = loader.load()
        assert loaded_config.generation.count == 500
        assert loaded_config.generation.seed == 42
        assert loaded_config.distribution.name == "normal"
        assert loaded_config.distribution.parameters == {"mu": 10, "sigma": 2}
    
    def test_save_creates_directory(self, tmp_path):
        """Test that save creates parent directories."""
        config_path = tmp_path / "nested" / "dir" / "config.json"
        loader = ConfigLoader(config_path=config_path)
        
        config = PyRngConfig()
        saved_path = loader.save(config)
        
        assert saved_path == config_path
        assert config_path.exists()
        assert config_path.parent.exists()
    
    def test_load_invalid_json(self, tmp_path):
        """Test loading invalid JSON raises error."""
        config_path = tmp_path / "invalid.json"
        config_path.write_text("{ invalid json }", encoding="utf-8")
        
        loader = ConfigLoader(config_path=config_path)
        
        with pytest.raises(ConfigurationError):
            loader.load()
    
    def test_create_default_config(self, tmp_path):
        """Test creating default config file."""
        config_path = tmp_path / "default.json"
        loader = ConfigLoader(config_path=config_path)
        
        created_path = loader.create_default_config()
        
        assert created_path == config_path
        assert config_path.exists()
        
        # Verify content
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        assert "generation" in data
        assert "distribution" in data
        assert "output" in data
    
    def test_create_default_config_already_exists(self, tmp_path):
        """Test that create_default_config doesn't overwrite existing file."""
        config_path = tmp_path / "existing.json"
        loader = ConfigLoader(config_path=config_path)
        
        # Create initial config with custom values
        custom_config = PyRngConfig(
            generation=GenerationConfig(count=999)
        )
        loader.save(custom_config)
        
        # Try to create default config
        returned_path = loader.create_default_config()
        
        # Should return existing path
        assert returned_path == config_path
        
        # Verify original content is preserved
        loaded = loader.load()
        assert loaded.generation.count == 999


class TestMergeConfigWithArgs:
    """Tests for merge_config_with_args function."""
    
    def test_merge_empty_args(self):
        """Test merging with empty args dict."""
        config = PyRngConfig()
        args = {}
        
        merged = merge_config_with_args(config, args)
        
        # Should be unchanged
        assert merged.generation.count == config.generation.count
        assert merged.distribution.name == config.distribution.name
    
    def test_merge_count(self):
        """Test merging count parameter."""
        config = PyRngConfig()
        args = {"count": 500}
        
        merged = merge_config_with_args(config, args)
        
        assert merged.generation.count == 500
    
    def test_merge_seed(self):
        """Test merging seed parameter."""
        config = PyRngConfig()
        args = {"seed": 42}
        
        merged = merge_config_with_args(config, args)
        
        assert merged.generation.seed == 42
    
    def test_merge_distribution(self):
        """Test merging distribution parameter."""
        config = PyRngConfig()
        args = {"distribution": "normal"}
        
        merged = merge_config_with_args(config, args)
        
        assert merged.distribution.name == "normal"
    
    def test_merge_parameters(self):
        """Test merging distribution parameters."""
        config = PyRngConfig()
        args = {"parameters": {"mu": 10, "sigma": 2}}
        
        merged = merge_config_with_args(config, args)
        
        assert merged.distribution.parameters["mu"] == 10
        assert merged.distribution.parameters["sigma"] == 2
    
    def test_merge_output_settings(self):
        """Test merging output settings."""
        config = PyRngConfig()
        args = {
            "output": "/tmp/output.csv",
            "format": "csv"
        }
        
        merged = merge_config_with_args(config, args)
        
        assert merged.output.file_path == "/tmp/output.csv"
        assert merged.output.format == "csv"
    
    def test_merge_verbose(self):
        """Test merging verbose setting."""
        config = PyRngConfig()
        args = {"verbose": True}
        
        merged = merge_config_with_args(config, args)
        
        assert merged.verbose is True
    
    def test_merge_multiple_parameters(self):
        """Test merging multiple parameters at once."""
        config = PyRngConfig()
        args = {
            "count": 1000,
            "seed": 123,
            "distribution": "exponential",
            "parameters": {"lam": 1.5},
            "format": "json",
            "verbose": True
        }
        
        merged = merge_config_with_args(config, args)
        
        assert merged.generation.count == 1000
        assert merged.generation.seed == 123
        assert merged.distribution.name == "exponential"
        assert merged.distribution.parameters["lam"] == 1.5
        assert merged.output.format == "json"
        assert merged.verbose is True
    
    def test_merge_none_values_ignored(self):
        """Test that None values in args don't override config."""
        config = PyRngConfig(
            generation=GenerationConfig(count=500, seed=42)
        )
        args = {
            "count": None,
            "seed": None
        }
        
        merged = merge_config_with_args(config, args)
        
        # Original values should be preserved
        assert merged.generation.count == 500
        assert merged.generation.seed == 42
    
    def test_original_config_not_modified(self):
        """Test that original config is not modified by merge."""
        config = PyRngConfig()
        original_count = config.generation.count
        
        args = {"count": 9999}
        merged = merge_config_with_args(config, args)
        
        # Original should be unchanged
        assert config.generation.count == original_count
        # Merged should have new value
        assert merged.generation.count == 9999
    
    def test_merge_clears_parameters_when_distribution_changes(self):
        """Test that old parameters are cleared when distribution changes."""
        config = PyRngConfig(
            distribution=DistributionConfig(
                name="poisson",
                parameters={"lam": 5.0}
            )
        )
        
        # Change distribution to normal without specifying new parameters
        args = {"distribution": "normal"}
        merged = merge_config_with_args(config, args)
        
        # Distribution should change
        assert merged.distribution.name == "normal"
        # Old parameters should be cleared
        assert "lam" not in merged.distribution.parameters
        assert merged.distribution.parameters == {}
    
    def test_merge_keeps_parameters_when_distribution_unchanged(self):
        """Test that parameters are kept when distribution doesn't change."""
        config = PyRngConfig(
            distribution=DistributionConfig(
                name="normal",
                parameters={"mu": 0.0, "sigma": 1.0}
            )
        )
        
        # Update other settings but keep distribution the same
        args = {"count": 500, "distribution": "normal"}
        merged = merge_config_with_args(config, args)
        
        # Distribution parameters should be preserved
        assert merged.distribution.name == "normal"
        assert merged.distribution.parameters["mu"] == 0.0
        assert merged.distribution.parameters["sigma"] == 1.0
