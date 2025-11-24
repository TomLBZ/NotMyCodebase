"""Integration tests for interactive mode."""

import pytest
from io import StringIO
from unittest.mock import patch, MagicMock

from pyrng.cli.interactive import InteractiveSession
from pyrng.config.models import PyRngConfig, GenerationConfig, DistributionConfig


class TestInteractiveSession:
    """Tests for InteractiveSession."""
    
    def test_initialization_with_defaults(self):
        """Test session initializes with default config."""
        session = InteractiveSession()
        
        assert session.config is not None
        assert session.generator is not None
        assert session.config_loader is not None
    
    def test_initialization_with_custom_config(self):
        """Test session initializes with custom config."""
        custom_config = PyRngConfig(
            generation=GenerationConfig(count=500, seed=42)
        )
        
        session = InteractiveSession(initial_config=custom_config)
        
        assert session.config.generation.count == 500
        assert session.config.generation.seed == 42
    
    def test_set_count_command(self):
        """Test setting count parameter."""
        session = InteractiveSession()
        
        session._handle_set_command("set count 1000")
        
        assert session.config.generation.count == 1000
    
    def test_set_seed_command(self):
        """Test setting seed parameter."""
        session = InteractiveSession()
        
        session._handle_set_command("set seed 42")
        
        assert session.config.generation.seed == 42
    
    def test_set_seed_none_command(self):
        """Test setting seed to None."""
        session = InteractiveSession()
        session.config.generation.seed = 42
        
        session._handle_set_command("set seed none")
        
        assert session.config.generation.seed is None
    
    def test_set_distribution_command(self):
        """Test setting distribution."""
        session = InteractiveSession()
        
        session._handle_set_command("set distribution normal")
        
        assert session.config.distribution.name == "normal"
        # Parameters should be reset
        assert session.config.distribution.parameters == {}
    
    def test_set_format_command(self):
        """Test setting output format."""
        session = InteractiveSession()
        
        session._handle_set_command("set format csv")
        
        assert session.config.output.format == "csv"
    
    def test_set_output_command(self):
        """Test setting output file."""
        session = InteractiveSession()
        
        session._handle_set_command("set output test.csv")
        
        assert session.config.output.file_path == "test.csv"
    
    def test_set_output_stdout_command(self):
        """Test setting output to stdout."""
        session = InteractiveSession()
        session.config.output.file_path = "test.csv"
        
        session._handle_set_command("set output stdout")
        
        assert session.config.output.file_path is None
    
    def test_set_verbose_command(self):
        """Test setting verbose mode."""
        session = InteractiveSession()
        
        session._handle_set_command("set verbose on")
        assert session.config.verbose is True
        
        session._handle_set_command("set verbose off")
        assert session.config.verbose is False
    
    def test_set_distribution_parameter(self):
        """Test setting distribution parameter."""
        session = InteractiveSession()
        session.config.distribution.name = "normal"
        
        session._handle_set_command("set param.mu 10")
        session._handle_set_command("set param.sigma 2.5")
        
        assert session.config.distribution.parameters["mu"] == 10.0
        assert session.config.distribution.parameters["sigma"] == 2.5
    
    def test_reset_config(self):
        """Test resetting configuration to defaults."""
        session = InteractiveSession()
        
        # Change some values
        session.config.generation.count = 9999
        session.config.distribution.name = "exponential"
        
        # Reset
        session._reset_config()
        
        # Should be back to defaults
        assert session.config.generation.count == 100
        assert session.config.distribution.name == "uniform"
    
    @patch('pyrng.cli.interactive.write_output')
    def test_generate_numbers(self, mock_write_output):
        """Test generating numbers in interactive mode."""
        session = InteractiveSession()
        session.config.generation.count = 10
        session.config.generation.seed = 42
        session.config.distribution.name = "uniform"
        session._update_generator()
        
        session._generate_numbers()
        
        # Verify write_output was called
        assert mock_write_output.called
        call_args = mock_write_output.call_args
        
        # Check that samples were generated
        samples = call_args[1]['data']
        assert len(samples) == 10
    
    @patch('pyrng.config.loader.ConfigLoader.save')
    def test_save_config(self, mock_save):
        """Test saving configuration."""
        from pathlib import Path
        mock_save.return_value = Path("/tmp/config.json")
        
        session = InteractiveSession()
        session._save_config()
        
        assert mock_save.called
    
    @patch('pyrng.config.loader.ConfigLoader.load')
    def test_load_config(self, mock_load):
        """Test loading configuration."""
        mock_config = PyRngConfig(
            generation=GenerationConfig(count=999)
        )
        mock_load.return_value = mock_config
        
        session = InteractiveSession()
        session._load_config()
        
        assert mock_load.called
        assert session.config.generation.count == 999


class TestInteractiveCommands:
    """Test interactive command parsing."""
    
    def test_invalid_set_command(self):
        """Test handling of invalid set commands."""
        session = InteractiveSession()
        
        # Missing value
        with patch('builtins.print') as mock_print:
            session._handle_set_command("set count")
            assert mock_print.called
    
    def test_invalid_format_value(self):
        """Test handling of invalid format value."""
        session = InteractiveSession()
        
        with patch('builtins.print') as mock_print:
            session._handle_set_command("set format invalid_format")
            assert mock_print.called
    
    def test_invalid_count_value(self):
        """Test handling of invalid count value."""
        session = InteractiveSession()
        original_count = session.config.generation.count
        
        with patch('builtins.print') as mock_print:
            session._handle_set_command("set count not_a_number")
            assert mock_print.called
        
        # Count should be unchanged
        assert session.config.generation.count == original_count
