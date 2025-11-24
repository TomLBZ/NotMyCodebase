# System Architecture - PyRng Project

## Executive Summary

PyRng is a highly configurable Python-based command-line application for generating random numbers from various probability distributions. The system is designed with modularity, extensibility, and maintainability as core principles, targeting Ubuntu Linux environments while maintaining cross-platform compatibility.

### Key Design Principles
1. **Modularity**: Clear separation of concerns with focused components
2. **Extensibility**: Easy to add new distributions and output formats
3. **Type Safety**: Comprehensive type hints throughout
4. **Performance**: Leverages NumPy for efficient array operations
5. **Usability**: Intuitive CLI with sensible defaults
6. **Testability**: Designed for easy unit and integration testing

## High-Level Architecture

### Architectural Style
**Layered Architecture** with clear separation between presentation (CLI), business logic (generation), and data (distributions).

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI Layer (Presentation)                  │
│  ┌─────────────────┐  ┌──────────────┐  ┌─────────────────┐│
│  │ Argument Parser │  │ Help System  │  │ Error Handler   ││
│  └─────────────────┘  └──────────────┘  └─────────────────┘│
└───────────────────────────────┬─────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────┐
│                  Application Layer (Orchestration)            │
│  ┌─────────────────┐  ┌──────────────┐  ┌─────────────────┐│
│  │ Config Manager  │  │  Validator   │  │ Logger Setup    ││
│  └─────────────────┘  └──────────────┘  └─────────────────┘│
└───────────────────────────────┬─────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────┐
│                  Core Layer (Business Logic)                  │
│  ┌─────────────────┐  ┌──────────────┐  ┌─────────────────┐│
│  │ Random Generator│  │   Factory    │  │  Distribution   ││
│  │                 │  │   Registry   │  │   Strategies    ││
│  └─────────────────┘  └──────────────┘  └─────────────────┘│
└───────────────────────────────┬─────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────┐
│                     Output Layer (Data)                       │
│  ┌─────────────────┐  ┌──────────────┐  ┌─────────────────┐│
│  │ Output Formatter│  │  File Writer │  │  Serializer     ││
│  └─────────────────┘  └──────────────┘  └─────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
pyrng/                          # Root project directory
├── .github/                    # GitHub specific files
│   └── workflows/              # CI/CD workflows
│       ├── test.yml            # Automated testing
│       └── lint.yml            # Code quality checks
├── docs/                       # Documentation
│   ├── user_guide.md           # User documentation
│   ├── developer_guide.md      # Developer documentation
│   └── api_reference.md        # API documentation
├── pyrng/                      # Main package directory
│   ├── __init__.py             # Package initialization, version
│   ├── __main__.py             # Entry point for python -m pyrng
│   ├── cli/                    # Command-line interface
│   │   ├── __init__.py
│   │   ├── parser.py           # Argument parsing
│   │   ├── commands.py         # CLI command implementations
│   │   └── validators.py       # CLI input validation
│   ├── core/                   # Core business logic
│   │   ├── __init__.py
│   │   ├── generator.py        # Main RandomGenerator class
│   │   ├── factory.py          # Distribution factory
│   │   └── exceptions.py       # Custom exception hierarchy
│   ├── distributions/          # Distribution implementations
│   │   ├── __init__.py
│   │   ├── base.py             # Abstract base class
│   │   ├── continuous.py       # Continuous distributions
│   │   │                       # (normal, uniform, exponential, etc.)
│   │   ├── discrete.py         # Discrete distributions
│   │   │                       # (binomial, poisson, etc.)
│   │   └── custom.py           # Custom distribution support
│   ├── config/                 # Configuration management
│   │   ├── __init__.py
│   │   ├── models.py           # Configuration data models
│   │   ├── loader.py           # Config file loading
│   │   └── defaults.py         # Default configurations
│   ├── output/                 # Output formatting and writing
│   │   ├── __init__.py
│   │   ├── formatters.py       # Output format implementations
│   │   ├── writers.py          # File writing logic
│   │   └── serializers.py      # Data serialization
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── logging_utils.py    # Logging configuration
│       ├── validation.py       # Common validators
│       └── helpers.py          # Helper functions
├── tests/                      # Test directory
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration and fixtures
│   ├── unit/                   # Unit tests
│   │   ├── test_cli.py
│   │   ├── test_generator.py
│   │   ├── test_distributions.py
│   │   ├── test_config.py
│   │   └── test_output.py
│   ├── integration/            # Integration tests
│   │   ├── test_workflows.py
│   │   └── test_cli_integration.py
│   └── data/                   # Test data files
│       ├── sample_config.json
│       └── expected_outputs/
├── examples/                   # Example scripts and configs
│   ├── basic_usage.py
│   ├── advanced_config.json
│   └── custom_distribution.py
├── .gitignore                  # Git ignore file
├── .python-version             # Python version specification
├── pyproject.toml              # Modern Python project config
├── setup.py                    # Package setup script (if needed)
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── README.md                   # Project README
├── CHANGELOG.md                # Version history
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # License file
└── pytest.ini                  # Pytest configuration
```

## Component Architecture

### 1. CLI Layer

#### Argument Parser (`cli/parser.py`)
**Responsibility**: Parse and validate command-line arguments.

```python
"""Command-line argument parsing module."""
import argparse
from typing import Optional
from pathlib import Path

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.
    
    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="pyrng",
        description="Flexible random number generator CLI",
        epilog="Examples: pyrng --help, pyrng uniform -n 1000"
    )
    
    # Global options
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "-c", "--config",
        type=Path,
        help="Path to configuration file"
    )
    parser.add_argument(
        "-s", "--seed",
        type=int,
        help="Random seed for reproducibility"
    )
    
    # Subcommands for different distributions
    subparsers = parser.add_subparsers(dest="distribution", help="Distribution type")
    
    # Uniform distribution
    uniform_parser = subparsers.add_parser("uniform", help="Uniform distribution")
    uniform_parser.add_argument("-n", "--count", type=int, required=True)
    uniform_parser.add_argument("--low", type=float, default=0.0)
    uniform_parser.add_argument("--high", type=float, default=1.0)
    
    # Normal distribution
    normal_parser = subparsers.add_parser("normal", help="Normal distribution")
    normal_parser.add_argument("-n", "--count", type=int, required=True)
    normal_parser.add_argument("--mu", type=float, default=0.0)
    normal_parser.add_argument("--sigma", type=float, default=1.0)
    
    # Output options (for all subcommands)
    for subparser in [uniform_parser, normal_parser]:
        subparser.add_argument(
            "-o", "--output",
            type=Path,
            help="Output file (default: stdout)"
        )
        subparser.add_argument(
            "-f", "--format",
            choices=["text", "csv", "json", "binary"],
            default="text",
            help="Output format"
        )
    
    return parser
```

#### Commands (`cli/commands.py`)
**Responsibility**: Implement CLI command logic.

```python
"""CLI command implementations."""
import sys
from pathlib import Path
from typing import Optional
import logging

from pyrng.core.generator import RandomGenerator
from pyrng.config.loader import load_config, merge_configs
from pyrng.output.writers import get_writer
from pyrng.utils.logging_utils import setup_logging

logger = logging.getLogger(__name__)

def execute_generate_command(args: argparse.Namespace) -> int:
    """Execute the generate command.
    
    Args:
        args: Parsed command-line arguments.
    
    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    try:
        # Setup logging
        setup_logging(verbose=args.verbose)
        
        # Load and merge configuration
        config = load_config(args.config) if args.config else Config()
        config = merge_configs(config, Config.from_cli_args(args))
        
        # Create generator
        generator = RandomGenerator(seed=config.seed)
        
        # Generate samples
        logger.info(f"Generating {args.count} samples from {args.distribution}")
        samples = generator.generate(
            distribution=args.distribution,
            count=args.count,
            parameters=config.parameters
        )
        
        # Write output
        writer = get_writer(
            output_path=args.output,
            format_type=args.format
        )
        writer.write(samples)
        
        logger.info("Generation completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=args.verbose)
        return 1
```

### 2. Core Layer

#### RandomGenerator (`core/generator.py`)
**Responsibility**: Main interface for generating random numbers.

```python
"""Core random number generator."""
import numpy as np
from typing import Optional, Dict, Any
import logging

from pyrng.distributions.base import Distribution
from pyrng.core.factory import DistributionFactory
from pyrng.core.exceptions import GenerationError

logger = logging.getLogger(__name__)

class RandomGenerator:
    """Main random number generator class.
    
    This class provides a unified interface for generating random numbers
    from various probability distributions.
    
    Attributes:
        seed: Random seed for reproducibility (if set).
        rng: NumPy random generator instance.
    
    Examples:
        >>> gen = RandomGenerator(seed=42)
        >>> samples = gen.generate("normal", 1000, {"mu": 0, "sigma": 1})
        >>> len(samples)
        1000
    """
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize the random generator.
        
        Args:
            seed: Random seed for reproducibility. If None, uses system entropy.
        """
        self.seed = seed
        self.rng = np.random.default_rng(seed=seed)
        logger.debug(f"Initialized RandomGenerator with seed={seed}")
    
    def generate(
        self,
        distribution: str,
        count: int,
        parameters: Optional[Dict[str, Any]] = None
    ) -> np.ndarray:
        """Generate random samples from a distribution.
        
        Args:
            distribution: Name of the distribution (e.g., "normal", "uniform").
            count: Number of samples to generate.
            parameters: Distribution-specific parameters.
        
        Returns:
            NumPy array of generated samples.
        
        Raises:
            GenerationError: If generation fails.
            ValidationError: If parameters are invalid.
        """
        try:
            # Create distribution instance
            params = parameters or {}
            dist = DistributionFactory.create(distribution, **params)
            
            # Generate samples
            logger.debug(f"Generating {count} samples from {distribution}")
            samples = dist.sample(size=count, rng=self.rng)
            
            return samples
            
        except Exception as e:
            raise GenerationError(f"Failed to generate samples: {e}") from e
    
    def reset_seed(self, seed: Optional[int] = None) -> None:
        """Reset the random generator with a new seed.
        
        Args:
            seed: New random seed.
        """
        self.seed = seed
        self.rng = np.random.default_rng(seed=seed)
        logger.debug(f"Reset RandomGenerator with seed={seed}")
```

#### Distribution Factory (`core/factory.py`)
**Responsibility**: Create distribution instances by name.

```python
"""Distribution factory for creating distribution instances."""
from typing import Dict, Type, Any
import logging

from pyrng.distributions.base import Distribution
from pyrng.core.exceptions import DistributionNotFoundError

logger = logging.getLogger(__name__)

class DistributionFactory:
    """Factory for creating distribution instances.
    
    This class maintains a registry of available distributions and
    provides a unified interface for creating them by name.
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
            name: Name to register the distribution under.
            distribution_class: Distribution class to register.
        """
        cls._registry[name] = distribution_class
        logger.debug(f"Registered distribution: {name}")
    
    @classmethod
    def create(cls, name: str, **kwargs: Any) -> Distribution:
        """Create a distribution instance by name.
        
        Args:
            name: Name of the distribution to create.
            **kwargs: Distribution-specific parameters.
        
        Returns:
            Distribution instance.
        
        Raises:
            DistributionNotFoundError: If distribution name is not registered.
        """
        if name not in cls._registry:
            available = ", ".join(cls._registry.keys())
            raise DistributionNotFoundError(
                f"Unknown distribution: {name}. "
                f"Available distributions: {available}"
            )
        
        distribution_class = cls._registry[name]
        return distribution_class(**kwargs)
    
    @classmethod
    def list_distributions(cls) -> list[str]:
        """Get list of registered distribution names.
        
        Returns:
            List of distribution names.
        """
        return list(cls._registry.keys())
```

### 3. Distribution Layer

#### Base Distribution (`distributions/base.py`)
**Responsibility**: Abstract interface for all distributions.

```python
"""Abstract base class for probability distributions."""
from abc import ABC, abstractmethod
import numpy as np
from typing import Any

class Distribution(ABC):
    """Abstract base class for probability distributions.
    
    All distribution implementations must inherit from this class
    and implement the sample() method.
    """
    
    @abstractmethod
    def sample(self, size: int, rng: np.random.Generator) -> np.ndarray:
        """Generate samples from this distribution.
        
        Args:
            size: Number of samples to generate.
            rng: NumPy random generator instance.
        
        Returns:
            NumPy array of samples.
        """
        pass
    
    @abstractmethod
    def validate_parameters(self) -> None:
        """Validate distribution parameters.
        
        Raises:
            ValidationError: If parameters are invalid.
        """
        pass
    
    def __repr__(self) -> str:
        """String representation of the distribution."""
        params = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({params})"
```

#### Continuous Distributions (`distributions/continuous.py`)
**Responsibility**: Implement continuous distributions.

```python
"""Continuous probability distributions."""
import numpy as np
from dataclasses import dataclass

from pyrng.distributions.base import Distribution
from pyrng.core.exceptions import ValidationError

@dataclass
class UniformDistribution(Distribution):
    """Uniform distribution U(low, high).
    
    Attributes:
        low: Lower bound (inclusive).
        high: Upper bound (exclusive).
    """
    low: float = 0.0
    high: float = 1.0
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        self.validate_parameters()
    
    def validate_parameters(self) -> None:
        """Validate distribution parameters."""
        if self.low >= self.high:
            raise ValidationError(
                f"low must be less than high, got low={self.low}, high={self.high}"
            )
    
    def sample(self, size: int, rng: np.random.Generator) -> np.ndarray:
        """Generate uniform samples."""
        return rng.uniform(self.low, self.high, size)

@dataclass
class NormalDistribution(Distribution):
    """Normal distribution N(mu, sigma^2).
    
    Attributes:
        mu: Mean (location parameter).
        sigma: Standard deviation (scale parameter).
    """
    mu: float = 0.0
    sigma: float = 1.0
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        self.validate_parameters()
    
    def validate_parameters(self) -> None:
        """Validate distribution parameters."""
        if self.sigma <= 0:
            raise ValidationError(
                f"sigma must be positive, got sigma={self.sigma}"
            )
    
    def sample(self, size: int, rng: np.random.Generator) -> np.ndarray:
        """Generate normal samples."""
        return rng.normal(self.mu, self.sigma, size)

@dataclass
class ExponentialDistribution(Distribution):
    """Exponential distribution Exp(lambda).
    
    Attributes:
        rate: Rate parameter (lambda).
    """
    rate: float = 1.0
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        self.validate_parameters()
    
    def validate_parameters(self) -> None:
        """Validate distribution parameters."""
        if self.rate <= 0:
            raise ValidationError(
                f"rate must be positive, got rate={self.rate}"
            )
    
    def sample(self, size: int, rng: np.random.Generator) -> np.ndarray:
        """Generate exponential samples."""
        scale = 1.0 / self.rate
        return rng.exponential(scale, size)
```

### 4. Configuration Layer

#### Configuration Models (`config/models.py`)
**Responsibility**: Define configuration data structures.

```python
"""Configuration data models."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class Config:
    """Application configuration.
    
    Attributes:
        seed: Random seed for reproducibility.
        distribution: Distribution type to use.
        parameters: Distribution-specific parameters.
        output_path: Output file path (None for stdout).
        output_format: Output format (text, csv, json, binary).
        verbose: Enable verbose logging.
    """
    seed: Optional[int] = None
    distribution: str = "uniform"
    parameters: Dict[str, Any] = field(default_factory=dict)
    output_path: Optional[str] = None
    output_format: str = "text"
    verbose: bool = False
    
    def merge(self, other: 'Config') -> 'Config':
        """Merge with another config (other takes precedence).
        
        Args:
            other: Configuration to merge with.
        
        Returns:
            New merged configuration.
        """
        return Config(
            seed=other.seed if other.seed is not None else self.seed,
            distribution=other.distribution or self.distribution,
            parameters={**self.parameters, **other.parameters},
            output_path=other.output_path or self.output_path,
            output_format=other.output_format or self.output_format,
            verbose=other.verbose or self.verbose
        )
```

### 5. Output Layer

#### Output Formatters (`output/formatters.py`)
**Responsibility**: Format data for different output types.

```python
"""Output formatting implementations."""
from abc import ABC, abstractmethod
import numpy as np
import json
from typing import Any

class OutputFormatter(ABC):
    """Abstract base class for output formatters."""
    
    @abstractmethod
    def format(self, data: np.ndarray) -> Any:
        """Format data for output.
        
        Args:
            data: NumPy array of data to format.
        
        Returns:
            Formatted data (type depends on formatter).
        """
        pass

class TextFormatter(OutputFormatter):
    """Plain text formatter (one number per line)."""
    
    def format(self, data: np.ndarray) -> str:
        """Format as plain text."""
        return "\n".join(str(x) for x in data)

class CSVFormatter(OutputFormatter):
    """CSV formatter."""
    
    def format(self, data: np.ndarray) -> str:
        """Format as CSV."""
        return "value\n" + "\n".join(str(x) for x in data)

class JSONFormatter(OutputFormatter):
    """JSON formatter."""
    
    def format(self, data: np.ndarray) -> str:
        """Format as JSON."""
        return json.dumps({
            "count": len(data),
            "values": data.tolist()
        }, indent=2)

class BinaryFormatter(OutputFormatter):
    """Binary formatter (NumPy binary format)."""
    
    def format(self, data: np.ndarray) -> bytes:
        """Format as binary."""
        return data.tobytes()
```

## Data Flow

### Generation Workflow

```
1. User Input (CLI)
   ↓
2. Argument Parsing
   ├─ Parse CLI arguments
   ├─ Load config file (if specified)
   └─ Merge configurations (CLI > File > Defaults)
   ↓
3. Validation
   ├─ Validate parameters
   ├─ Check constraints
   └─ Setup logging
   ↓
4. Generation
   ├─ Create RandomGenerator
   ├─ Get Distribution from Factory
   ├─ Generate samples (NumPy)
   └─ Return array
   ↓
5. Output
   ├─ Format data (text/csv/json/binary)
   ├─ Write to file or stdout
   └─ Log completion
   ↓
6. Exit (status code)
```

### Example: Generate 1000 Normal Random Numbers

```bash
$ pyrng normal -n 1000 --mu 0 --sigma 1 -o output.csv -f csv --seed 42
```

**Flow**:
1. CLI parser receives arguments
2. Creates Config: `{distribution: "normal", count: 1000, mu: 0, sigma: 1, output: "output.csv", format: "csv", seed: 42}`
3. Validator checks count > 0, sigma > 0
4. RandomGenerator created with seed=42
5. DistributionFactory creates NormalDistribution(mu=0, sigma=1)
6. Generator calls distribution.sample(1000, rng) → returns np.ndarray
7. CSVFormatter formats array as CSV string
8. FileWriter writes to output.csv
9. Success logged, exit 0

## Design Patterns

### 1. Strategy Pattern (Distributions)
Each distribution is a strategy that implements the `Distribution` interface. The generator delegates to the selected strategy.

### 2. Factory Pattern (Distribution Creation)
`DistributionFactory` encapsulates the logic for creating distribution instances based on string names.

### 3. Template Method (Base Distribution)
`Distribution` abstract class defines the template for all distributions with required methods.

### 4. Dependency Injection
`RandomGenerator.generate()` receives the RNG instance, making it testable and flexible.

### 5. Builder Pattern (Configuration)
Configuration is built incrementally from multiple sources (defaults → file → CLI).

## Error Handling Strategy

### Exception Hierarchy

```python
PyRngError                      # Base exception
├── ConfigurationError          # Configuration issues
│   ├── InvalidConfigError
│   └── MissingConfigError
├── ValidationError             # Invalid parameters
│   ├── ParameterRangeError
│   └── ParameterTypeError
├── GenerationError             # Generation failures
│   └── DistributionNotFoundError
└── OutputError                 # Output failures
    ├── FileWriteError
    └── FormatError
```

### Error Handling Principles
1. **Fail Fast**: Validate early, before expensive operations
2. **Clear Messages**: Provide actionable error messages
3. **Graceful Degradation**: Log errors and exit cleanly
4. **No Silent Failures**: Always log or report errors

## Performance Considerations

### Optimization Strategies
1. **Vectorization**: Use NumPy operations instead of Python loops
2. **Memory Efficiency**: Generate in chunks for very large datasets (future enhancement)
3. **Lazy Evaluation**: Only load/compute what's needed
4. **Caching**: Cache distribution instances if reused

### Performance Targets
- Generate 1M uniform numbers: < 0.5 seconds
- Generate 1M normal numbers: < 1 second
- Startup time: < 100ms
- Memory overhead: < 50MB base, O(n) for samples

## Security Considerations

### Input Validation
- All CLI inputs validated before use
- File paths sanitized using `pathlib.Path`
- No code execution from user input (no `eval`, `exec`)

### Safe File Operations
- Check file permissions before writing
- Use context managers for file handles
- Validate file paths to prevent directory traversal

### Dependency Security
- Pin dependency versions in requirements.txt
- Regular dependency audits with `pip-audit`
- Minimal dependency surface (prefer stdlib)

## Testing Strategy

### Test Coverage Goals
- **Unit Tests**: 95%+ coverage
- **Integration Tests**: Cover all major workflows
- **Edge Cases**: Boundary values, invalid inputs
- **Performance Tests**: Benchmarks for critical paths

### Test Structure
```python
# Unit test example
def test_normal_distribution_generates_correct_size():
    dist = NormalDistribution(mu=0, sigma=1)
    rng = np.random.default_rng(seed=42)
    samples = dist.sample(size=1000, rng=rng)
    assert len(samples) == 1000

# Integration test example
def test_cli_generates_to_file(tmp_path):
    output_file = tmp_path / "output.txt"
    result = subprocess.run([
        "pyrng", "uniform", "-n", "100",
        "-o", str(output_file)
    ], capture_output=True)
    assert result.returncode == 0
    assert output_file.exists()
    lines = output_file.read_text().strip().split("\n")
    assert len(lines) == 100
```

## Deployment and Distribution

### Package Distribution
- **PyPI**: Publish as `pyrng` package
- **Installation**: `pip install pyrng`
- **Entry Point**: Registered console script `pyrng`

### Versioning
- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Version Location**: `pyrng/__init__.py` `__version__` variable
- **Git Tags**: Tag releases in git

### Release Process
1. Update CHANGELOG.md
2. Bump version in `__init__.py`
3. Run full test suite
4. Create git tag
5. Build package: `python -m build`
6. Upload to PyPI: `twine upload dist/*`

## Extensibility Points

### Adding New Distributions
1. Create distribution class inheriting from `Distribution`
2. Implement `sample()` and `validate_parameters()` methods
3. Register with `DistributionFactory`
4. Add CLI subcommand in parser
5. Add tests

### Adding New Output Formats
1. Create formatter class inheriting from `OutputFormatter`
2. Implement `format()` method
3. Register in formatter factory
4. Add to CLI format choices
5. Add tests

### Adding New Configuration Sources
1. Implement loader function
2. Add to configuration merge chain
3. Document in user guide

## Future Enhancements

### Phase 2 (Potential)
- **Multivariate Distributions**: Support for correlated random vectors
- **Streaming Generation**: Generate infinite streams with iterators
- **Parallel Generation**: Multi-process generation for performance
- **Custom Distributions**: User-defined distribution from code/config
- **Statistical Tests**: Built-in tests for distribution quality

### Phase 3 (Potential)
- **Web API**: REST API for random number generation
- **Database Integration**: Direct database output
- **Cloud Storage**: S3/GCS output support
- **Visualization**: Built-in plotting capabilities
- **Interactive Mode**: REPL for exploratory use

## Architectural Decisions and Rationale

### Why Layered Architecture?
- **Clear Separation**: Each layer has distinct responsibility
- **Testability**: Easy to test layers in isolation
- **Maintainability**: Changes localized to specific layers
- **Understandability**: Intuitive flow from CLI to output

### Why NumPy for Core Generation?
- **Performance**: 10-100x faster than pure Python
- **Rich API**: Comprehensive set of distributions
- **Industry Standard**: Well-documented, widely used
- **Array Operations**: Efficient handling of large datasets

### Why argparse over click/typer?
- **Standard Library**: No external dependency
- **Sufficient Features**: Meets all requirements
- **Educational Value**: Students learn stdlib
- **Lightweight**: Minimal overhead
- **Note**: Can easily switch to click if preferred

### Why Dataclasses for Models?
- **Simplicity**: Clean, concise syntax
- **Type Hints**: Built-in support
- **Immutability**: Can make frozen dataclasses
- **Standard Library**: No external dependency (Python 3.7+)

### Why Strategy Pattern for Distributions?
- **Extensibility**: Easy to add new distributions
- **Testability**: Test each distribution independently
- **Maintainability**: Each distribution self-contained
- **Open/Closed Principle**: Open for extension, closed for modification

## Conclusion

This architecture provides a solid foundation for a flexible, maintainable, and extensible random number generator CLI application. The design emphasizes:

- **Simplicity**: Straightforward code structure
- **Modularity**: Clear component boundaries
- **Type Safety**: Comprehensive type hints
- **Testability**: Easy to test at all levels
- **Performance**: Leverages NumPy for efficiency
- **Extensibility**: Easy to add new features

The architecture follows Python best practices and is designed for educational purposes while being production-ready. All components are well-documented and follow consistent patterns, making the codebase easy to understand and maintain.
