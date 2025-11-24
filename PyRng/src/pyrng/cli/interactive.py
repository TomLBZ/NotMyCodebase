"""Interactive mode for PyRng."""

import logging
from typing import Optional, Dict, Any
from pathlib import Path

from pyrng.config import PyRngConfig, ConfigLoader
from pyrng.core.generator import RandomGenerator
from pyrng.output.writers import write_output
from pyrng.core.exceptions import PyRngError

logger = logging.getLogger(__name__)


class InteractiveSession:
    """Manages an interactive PyRng session.
    
    Provides an interactive command-line interface for configuring and
    generating random numbers without restarting the application.
    
    Attributes:
        config: Current PyRngConfig instance.
        config_loader: ConfigLoader for saving/loading configs.
    
    Examples:
        >>> session = InteractiveSession()
        >>> session.run()
    """
    
    def __init__(
        self,
        initial_config: Optional[PyRngConfig] = None,
        config_loader: Optional[ConfigLoader] = None
    ) -> None:
        """Initialize interactive session.
        
        Args:
            initial_config: Starting configuration. If None, loads from file or uses defaults.
            config_loader: Config loader instance. If None, creates default.
        """
        self.config_loader = config_loader or ConfigLoader()
        
        if initial_config is None:
            self.config = self.config_loader.load()
        else:
            self.config = initial_config
        
        self.generator: Optional[RandomGenerator] = None
        self._update_generator()
    
    def _update_generator(self) -> None:
        """Update the random generator with current seed."""
        self.generator = RandomGenerator(seed=self.config.generation.seed)
    
    def run(self) -> None:
        """Run the interactive session loop.
        
        Displays prompts and processes user commands until 'exit' is entered.
        """
        self._print_welcome()
        
        while True:
            try:
                command = input("\npyrng> ").strip().lower()
                
                if not command:
                    continue
                
                if command in ["exit", "quit", "q"]:
                    print("Goodbye!")
                    break
                elif command in ["help", "h", "?"]:
                    self._show_help()
                elif command in ["show", "status", "config"]:
                    self._show_config()
                elif command.startswith("set "):
                    self._handle_set_command(command)
                elif command in ["generate", "gen", "g"]:
                    self._generate_numbers()
                elif command in ["save", "save-config"]:
                    self._save_config()
                elif command in ["load", "load-config"]:
                    self._load_config()
                elif command in ["reset"]:
                    self._reset_config()
                else:
                    print(f"Unknown command: '{command}'. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.")
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                print(f"Error: {e}")
    
    def _print_welcome(self) -> None:
        """Print welcome message."""
        print("=" * 60)
        print("PyRng Interactive Mode")
        print("=" * 60)
        print("Type 'help' for available commands or 'exit' to quit.")
        self._show_config()
    
    def _show_help(self) -> None:
        """Display help information."""
        help_text = """
Available Commands:
  help, h, ?          - Show this help message
  show, status        - Display current configuration
  set <param> <value> - Set a configuration parameter
  generate, gen, g    - Generate random numbers with current settings
  save                - Save current configuration to file
  load                - Reload configuration from file
  reset               - Reset configuration to defaults
  exit, quit, q       - Exit interactive mode

Configuration Parameters (use with 'set'):
  count <n>           - Number of samples (e.g., set count 1000)
  seed <n>            - Random seed (e.g., set seed 42)
  distribution <name> - Distribution type (uniform, normal, exponential, binomial, poisson)
  format <fmt>        - Output format (text, csv, json, binary)
  output <path>       - Output file path (or 'stdout' for console)
  verbose <on|off>    - Enable/disable verbose logging
  
Distribution Parameters:
  param.<name> <val>  - Set distribution parameter (e.g., param.mu 0, param.sigma 1)

Examples:
  set count 500
  set distribution normal
  set param.mu 10
  set param.sigma 2
  set seed 42
  generate
  set output results.csv
  set format csv
  generate
  save
"""
        print(help_text)
    
    def _show_config(self) -> None:
        """Display current configuration."""
        print("\nCurrent Configuration:")
        print(f"  Distribution:  {self.config.distribution.name}")
        print(f"  Parameters:    {self.config.distribution.parameters}")
        print(f"  Sample Count:  {self.config.generation.count}")
        print(f"  Random Seed:   {self.config.generation.seed}")
        print(f"  Output Format: {self.config.output.format}")
        print(f"  Output File:   {self.config.output.file_path or 'stdout'}")
        print(f"  Verbose:       {self.config.verbose}")
    
    def _handle_set_command(self, command: str) -> None:
        """Handle 'set' commands.
        
        Args:
            command: Full command string starting with 'set'.
        """
        parts = command.split(maxsplit=2)
        
        if len(parts) < 3:
            print("Usage: set <parameter> <value>")
            return
        
        param_name = parts[1].lower()
        value_str = parts[2]
        
        try:
            if param_name == "count":
                self.config.generation.count = int(value_str)
                print(f"Sample count set to {self.config.generation.count}")
            
            elif param_name == "seed":
                if value_str.lower() in ["none", "null", "random"]:
                    self.config.generation.seed = None
                else:
                    self.config.generation.seed = int(value_str)
                self._update_generator()
                print(f"Random seed set to {self.config.generation.seed}")
            
            elif param_name == "distribution":
                self.config.distribution.name = value_str.lower()
                # Reset parameters when changing distribution
                self.config.distribution.parameters = {}
                print(f"Distribution set to {self.config.distribution.name}")
                print("Note: Distribution parameters have been reset.")
            
            elif param_name == "format":
                if value_str.lower() not in ["text", "csv", "json", "binary"]:
                    print(f"Invalid format: {value_str}")
                    print("Valid formats: text, csv, json, binary")
                    return
                self.config.output.format = value_str.lower()
                print(f"Output format set to {self.config.output.format}")
            
            elif param_name == "output":
                if value_str.lower() in ["stdout", "console", "none"]:
                    self.config.output.file_path = None
                    print("Output set to stdout")
                else:
                    self.config.output.file_path = value_str
                    print(f"Output file set to {self.config.output.file_path}")
            
            elif param_name == "verbose":
                if value_str.lower() in ["on", "true", "1", "yes"]:
                    self.config.verbose = True
                elif value_str.lower() in ["off", "false", "0", "no"]:
                    self.config.verbose = False
                else:
                    print(f"Invalid value for verbose: {value_str}")
                    print("Use: on, off, true, false, yes, no, 1, or 0")
                    return
                print(f"Verbose logging set to {self.config.verbose}")
            
            elif param_name.startswith("param."):
                # Distribution parameter
                param_key = param_name[6:]  # Remove 'param.' prefix
                
                # Try to parse as float
                try:
                    param_value = float(value_str)
                except ValueError:
                    param_value = value_str
                
                self.config.distribution.parameters[param_key] = param_value
                print(f"Distribution parameter '{param_key}' set to {param_value}")
            
            else:
                print(f"Unknown parameter: {param_name}")
                print("Type 'help' to see available parameters.")
        
        except ValueError as e:
            print(f"Invalid value for {param_name}: {value_str}")
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error setting parameter: {e}")
    
    def _generate_numbers(self) -> None:
        """Generate random numbers with current configuration."""
        try:
            print(f"\nGenerating {self.config.generation.count} samples from "
                  f"{self.config.distribution.name} distribution...")
            
            # Generate samples
            samples = self.generator.generate(
                distribution=self.config.distribution.name,
                count=self.config.generation.count,
                parameters=self.config.distribution.parameters
            )
            
            print(f"Successfully generated {len(samples)} samples")
            
            # Determine output path
            output_path = None
            if self.config.output.file_path:
                output_path = Path(self.config.output.file_path)
            
            # Write output
            write_output(
                data=samples,
                output_path=output_path,
                format_type=self.config.output.format
            )
            
            if output_path:
                print(f"Output written to {output_path}")
            else:
                print("Output written to stdout")
        
        except PyRngError as e:
            print(f"Generation error: {e}")
            logger.error(f"Generation error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            logger.error(f"Unexpected error: {e}")
    
    def _save_config(self) -> None:
        """Save current configuration to file."""
        try:
            path = self.config_loader.save(self.config)
            print(f"Configuration saved to {path}")
        except Exception as e:
            print(f"Error saving configuration: {e}")
            logger.error(f"Error saving configuration: {e}")
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        try:
            self.config = self.config_loader.load()
            self._update_generator()
            print("Configuration loaded from file")
            self._show_config()
        except Exception as e:
            print(f"Error loading configuration: {e}")
            logger.error(f"Error loading configuration: {e}")
    
    def _reset_config(self) -> None:
        """Reset configuration to defaults."""
        self.config = PyRngConfig()
        self._update_generator()
        print("Configuration reset to defaults")
        self._show_config()


def start_interactive_mode(initial_config: Optional[PyRngConfig] = None) -> None:
    """Start an interactive PyRng session.
    
    Args:
        initial_config: Optional initial configuration. If None, loads from file or uses defaults.
    
    Examples:
        >>> start_interactive_mode()
    """
    session = InteractiveSession(initial_config=initial_config)
    session.run()
