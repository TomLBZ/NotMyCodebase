"""CLI command implementations."""

import sys
import argparse
from typing import Dict, Any, Optional
import logging

from pyrng.core.generator import RandomGenerator
from pyrng.output.writers import write_output
from pyrng.utils.logging_utils import setup_logging
from pyrng.core.exceptions import PyRngError
from pyrng.config import ConfigLoader, merge_config_with_args, PyRngConfig
from pyrng.cli.interactive import start_interactive_mode

logger = logging.getLogger(__name__)


def get_distribution_parameters(args: argparse.Namespace) -> Dict[str, Any]:
    """Extract distribution parameters from parsed arguments.
    
    Args:
        args: Parsed command-line arguments.
    
    Returns:
        Dictionary of distribution-specific parameters.
    
    Examples:
        >>> args = argparse.Namespace(
        ...     distribution="uniform",
        ...     low=0.0,
        ...     high=10.0
        ... )
        >>> params = get_distribution_parameters(args)
        >>> params
        {'low': 0.0, 'high': 10.0}
    """
    params: Dict[str, Any] = {}
    
    # Map distribution to their parameters
    param_mapping = {
        "uniform": ["low", "high"],
        "normal": ["mu", "sigma"],
        "exponential": ["lam"],
        "binomial": ["n", "p"],
        "poisson": ["lam"],
    }
    
    # Get parameters for the selected distribution
    if args.distribution in param_mapping:
        for param_name in param_mapping[args.distribution]:
            # Handle special case: binomial's 'n' is 'trials' in CLI
            if param_name == "n" and args.distribution == "binomial":
                if hasattr(args, "trials"):
                    params["n"] = args.trials
            elif hasattr(args, param_name):
                params[param_name] = getattr(args, param_name)
    
    return params


def execute_command(args: argparse.Namespace) -> int:
    """Execute the random number generation command.
    
    Handles config loading, interactive mode, and standard CLI generation.
    
    Args:
        args: Parsed command-line arguments.
    
    Returns:
        Exit code (0 for success, non-zero for failure).
    
    Examples:
        >>> args = argparse.Namespace(
        ...     distribution="uniform",
        ...     count=10,
        ...     low=0.0,
        ...     high=1.0,
        ...     seed=42,
        ...     output=None,
        ...     format="text",
        ...     verbose=False,
        ...     interactive=False,
        ...     config=None,
        ...     create_config=False
        ... )
        >>> execute_command(args)
        0
    """
    try:
        # Setup logging
        setup_logging(verbose=args.verbose)
        
        # Handle --create-config flag
        if args.create_config:
            config_loader = ConfigLoader(config_path=args.config)
            config_path = config_loader.create_default_config()
            print(f"Default configuration file created at: {config_path}")
            return 0
        
        # Load configuration from file if available
        config_loader = ConfigLoader(config_path=args.config)
        base_config = config_loader.load()
        
        # Handle interactive mode
        if args.interactive:
            # Merge CLI args into config for interactive session
            if args.distribution:
                cli_args = {
                    "distribution": args.distribution,
                    "count": getattr(args, "count", None),
                    "seed": args.seed,
                    "output": args.output,
                    "format": args.format,
                    "verbose": args.verbose,
                    "parameters": get_distribution_parameters(args),
                }
                config = merge_config_with_args(base_config, cli_args)
            else:
                config = base_config
            
            start_interactive_mode(initial_config=config)
            return 0
        
        # Standard CLI mode - require distribution
        if not args.distribution:
            logger.error("Distribution is required in non-interactive mode")
            print("Error: Distribution argument is required.")
            print("Use 'pyrng --help' for usage information.")
            print("Or use 'pyrng --interactive' for interactive mode.")
            return 1
        
        # Merge config file with CLI arguments (CLI takes precedence)
        cli_args = {
            "distribution": args.distribution,
            "count": args.count,
            "seed": args.seed,
            "output": args.output,
            "format": args.format,
            "verbose": args.verbose,
            "parameters": get_distribution_parameters(args),
        }
        config = merge_config_with_args(base_config, cli_args)
        
        logger.info(
            f"Generating {config.generation.count} samples from "
            f"{config.distribution.name} distribution"
        )
        logger.debug(f"Distribution parameters: {config.distribution.parameters}")
        
        # Create generator
        generator = RandomGenerator(seed=config.generation.seed)
        
        # Generate samples
        samples = generator.generate(
            distribution=config.distribution.name,
            count=config.generation.count,
            parameters=config.distribution.parameters
        )
        
        logger.info(f"Successfully generated {len(samples)} samples")
        
        # Prepare format options
        format_options = {}
        if config.output.format == "csv":
            format_options["header"] = "value"
        elif config.output.format == "json":
            format_options["pretty"] = True
        
        # Write output
        output_path = None
        if config.output.file_path:
            from pathlib import Path
            output_path = Path(config.output.file_path)
        
        write_output(
            data=samples,
            output_path=output_path,
            format_type=config.output.format,
            **format_options
        )
        
        if output_path:
            logger.info(f"Output written to {output_path}")
        
        return 0
        
    except PyRngError as e:
        logger.error(f"Error: {e}")
        if args.verbose:
            logger.exception("Detailed error information:")
        return 1
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            logger.exception("Detailed error information:")
        return 2
