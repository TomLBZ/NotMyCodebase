"""Configuration file loading and saving."""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from pyrng.config.models import PyRngConfig
from pyrng.core.exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Handles loading and saving configuration files.
    
    Supports reading from and writing to JSON configuration files.
    
    Examples:
        >>> loader = ConfigLoader()
        >>> config = loader.load()
        >>> isinstance(config, PyRngConfig)
        True
    """
    
    DEFAULT_CONFIG_PATHS = [
        Path.home() / ".pyrng" / "config.json",
        Path.cwd() / "pyrng_config.json",
    ]
    
    def __init__(self, config_path: Optional[Path] = None) -> None:
        """Initialize config loader.
        
        Args:
            config_path: Custom config file path. If None, uses default locations.
        
        Examples:
            >>> loader = ConfigLoader()
            >>> loader = ConfigLoader(Path("/custom/path/config.json"))
        """
        self.config_path = config_path
    
    def _find_config_file(self) -> Optional[Path]:
        """Find an existing config file in default locations.
        
        Returns:
            Path to config file if found, None otherwise.
        """
        if self.config_path and self.config_path.exists():
            return self.config_path
        
        for path in self.DEFAULT_CONFIG_PATHS:
            if path.exists():
                logger.debug(f"Found config file at {path}")
                return path
        
        return None
    
    def _get_default_config_path(self) -> Path:
        """Get the default config file path for saving.
        
        Returns:
            Path for saving new config file.
        """
        if self.config_path:
            return self.config_path
        
        # Use first default path
        return self.DEFAULT_CONFIG_PATHS[0]
    
    def load(self) -> PyRngConfig:
        """Load configuration from file or return defaults.
        
        Searches for config files in default locations. If not found,
        returns default configuration.
        
        Returns:
            Loaded or default PyRngConfig instance.
        
        Raises:
            ConfigurationError: If config file exists but is invalid.
        
        Examples:
            >>> loader = ConfigLoader()
            >>> config = loader.load()
            >>> isinstance(config, PyRngConfig)
            True
        """
        config_file = self._find_config_file()
        
        if config_file is None:
            logger.info("No config file found, using defaults")
            return PyRngConfig()
        
        try:
            logger.info(f"Loading config from {config_file}")
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            config = PyRngConfig.from_dict(data)
            logger.debug(f"Successfully loaded config: {config}")
            return config
            
        except json.JSONDecodeError as e:
            raise ConfigurationError(
                f"Invalid JSON in config file {config_file}: {e}"
            ) from e
        except Exception as e:
            raise ConfigurationError(
                f"Failed to load config from {config_file}: {e}"
            ) from e
    
    def save(self, config: PyRngConfig) -> Path:
        """Save configuration to file.
        
        Creates parent directories if they don't exist.
        
        Args:
            config: Configuration to save.
        
        Returns:
            Path where config was saved.
        
        Raises:
            ConfigurationError: If saving fails.
        
        Examples:
            >>> loader = ConfigLoader()
            >>> config = PyRngConfig()
            >>> path = loader.save(config)
            >>> path.exists()
            True
        """
        config_path = self._get_default_config_path()
        
        try:
            # Create parent directory if needed
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert to dict and save as JSON
            data = config.to_dict()
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Config saved to {config_path}")
            return config_path
            
        except Exception as e:
            raise ConfigurationError(
                f"Failed to save config to {config_path}: {e}"
            ) from e
    
    def create_default_config(self) -> Path:
        """Create a default config file if none exists.
        
        Returns:
            Path to created config file.
        
        Examples:
            >>> loader = ConfigLoader()
            >>> path = loader.create_default_config()
            >>> path.exists()
            True
        """
        # If a specific config path was provided, use it regardless of whether
        # other configs exist in default locations
        if self.config_path:
            if self.config_path.exists():
                logger.info(f"Config file already exists at {self.config_path}")
                return self.config_path
            else:
                logger.info(f"Creating default config file at {self.config_path}")
                default_config = PyRngConfig()
                return self.save(default_config)
        
        # No specific path provided - check default locations
        config_file = self._find_config_file()
        if config_file is not None:
            logger.info(f"Config file already exists at {config_file}")
            return config_file
        
        logger.info("Creating default config file in default location")
        default_config = PyRngConfig()
        return self.save(default_config)


def merge_config_with_args(
    config: PyRngConfig,
    args: Dict[str, Any]
) -> PyRngConfig:
    """Merge CLI arguments with config file settings.
    
    CLI arguments take precedence over config file values.
    
    Args:
        config: Base configuration from file.
        args: Command-line arguments as dictionary.
    
    Returns:
        Merged configuration.
    
    Examples:
        >>> config = PyRngConfig()
        >>> args = {"count": 200, "seed": 42}
        >>> merged = merge_config_with_args(config, args)
        >>> merged.generation.count
        200
        >>> merged.generation.seed
        42
    """
    # Create a copy to avoid modifying original
    merged_data = config.to_dict()
    
    # Map CLI args to config structure
    if "count" in args and args["count"] is not None:
        merged_data["generation"]["count"] = args["count"]
    
    if "seed" in args and args["seed"] is not None:
        merged_data["generation"]["seed"] = args["seed"]
    
    if "distribution" in args and args["distribution"] is not None:
        # If distribution changes, clear old parameters to prevent leakage
        if merged_data["distribution"]["name"] != args["distribution"]:
            merged_data["distribution"]["parameters"] = {}
        merged_data["distribution"]["name"] = args["distribution"]
    
    # Handle distribution parameters
    if "parameters" in args and args["parameters"]:
        merged_data["distribution"]["parameters"].update(args["parameters"])
    
    if "output" in args and args["output"] is not None:
        merged_data["output"]["file_path"] = str(args["output"])
    
    if "format" in args and args["format"] is not None:
        merged_data["output"]["format"] = args["format"]
    
    if "verbose" in args and args["verbose"] is not None:
        merged_data["verbose"] = args["verbose"]
    
    return PyRngConfig.from_dict(merged_data)
