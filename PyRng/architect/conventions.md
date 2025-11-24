# Development Conventions - PyRng Project

## Coding Conventions

### General Principles
1. **Simplicity**: Write clear, straightforward code over clever solutions
2. **Explicitness**: Favor explicit code over implicit behavior
3. **Consistency**: Follow established patterns throughout the codebase
4. **Type Safety**: Use type hints extensively
5. **Modularity**: Keep functions and classes focused and single-purpose

### Python Style Guide

#### PEP 8 Compliance
- Follow [PEP 8](https://pep8.org/) style guide
- Use Black for automatic formatting (line length: 88 characters)
- Use Ruff for linting

#### Naming Conventions

```python
# Modules and packages: lowercase with underscores
random_generators.py
distribution_module/

# Classes: PascalCase
class RandomGenerator:
class NormalDistribution:
class ConfigurationManager:

# Functions and methods: snake_case
def generate_numbers():
def validate_input():
def parse_arguments():

# Constants: UPPERCASE with underscores
MAX_SAMPLE_SIZE = 1_000_000
DEFAULT_SEED = 42
CONFIG_FILE_NAME = "pyrng.json"

# Private functions/methods: prefix with single underscore
def _internal_helper():
class MyClass:
    def _private_method(self):

# Variables: snake_case
sample_size = 1000
distribution_type = "normal"
output_file_path = Path("./output.csv")

# Type variables: PascalCase with suffix
T = TypeVar('T')
DistributionT = TypeVar('DistributionT', bound='Distribution')
```

#### Import Organization

```python
# Standard library imports (alphabetical)
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Third-party imports (alphabetical)
import numpy as np
from pydantic import BaseModel, Field

# Local application imports (alphabetical)
from pyrng.core.generator import RandomGenerator
from pyrng.distributions import NormalDistribution
from pyrng.utils.config import load_config
```

### Type Hints

#### Required Usage
- All function signatures must have type hints
- All class attributes should have type hints
- Use `Optional[]` for nullable values
- Use `Union[]` for multiple types (or `|` operator in Python 3.10+)

```python
from typing import Optional, List, Dict, Any

def generate_numbers(
    distribution: str,
    count: int,
    seed: Optional[int] = None,
    parameters: Optional[Dict[str, Any]] = None
) -> np.ndarray:
    """Generate random numbers with specified distribution."""
    pass

class Distribution:
    name: str
    parameters: Dict[str, float]
    _rng: Optional[np.random.Generator] = None
    
    def sample(self, size: int) -> np.ndarray:
        pass
```

### Code Structure

#### Function Length
- Keep functions under 50 lines when possible
- Extract complex logic into helper functions
- One function should do one thing well

#### Class Design
- Follow Single Responsibility Principle
- Use composition over inheritance when appropriate
- Keep class interfaces minimal and focused

```python
# Good: Focused, single responsibility
class UniformDistribution:
    def __init__(self, low: float, high: float):
        self.low = low
        self.high = high
    
    def sample(self, size: int, rng: np.random.Generator) -> np.ndarray:
        return rng.uniform(self.low, self.high, size)

# Bad: Too many responsibilities
class Distribution:
    def sample(self): pass
    def save_to_file(self): pass  # Should be separate
    def plot_histogram(self): pass  # Should be separate
    def validate_config(self): pass  # Should be separate
```

#### Error Handling

```python
# Define custom exception hierarchy
class PyRngError(Exception):
    """Base exception for PyRng."""
    pass

class ConfigurationError(PyRngError):
    """Raised when configuration is invalid."""
    pass

class ValidationError(PyRngError):
    """Raised when input validation fails."""
    pass

# Use specific exceptions
def validate_sample_size(size: int) -> None:
    if size <= 0:
        raise ValidationError(f"Sample size must be positive, got {size}")
    if size > MAX_SAMPLE_SIZE:
        raise ValidationError(
            f"Sample size {size} exceeds maximum {MAX_SAMPLE_SIZE}"
        )

# Handle exceptions at appropriate levels
try:
    config = load_config(config_path)
except FileNotFoundError:
    logger.error(f"Configuration file not found: {config_path}")
    sys.exit(1)
except ConfigurationError as e:
    logger.error(f"Invalid configuration: {e}")
    sys.exit(1)
```

## Documentation Standards

### Docstring Format
Use Google-style docstrings for consistency.

```python
def generate_samples(
    distribution: Distribution,
    size: int,
    seed: Optional[int] = None
) -> np.ndarray:
    """Generate random samples from a distribution.
    
    This function creates random samples using the specified distribution
    and ensures reproducibility when a seed is provided.
    
    Args:
        distribution: The probability distribution to sample from.
        size: Number of samples to generate. Must be positive.
        seed: Random seed for reproducibility. If None, uses system entropy.
    
    Returns:
        A NumPy array containing the generated samples.
    
    Raises:
        ValidationError: If size is not positive.
        GenerationError: If sample generation fails.
    
    Examples:
        >>> dist = NormalDistribution(mu=0, sigma=1)
        >>> samples = generate_samples(dist, 1000, seed=42)
        >>> len(samples)
        1000
    """
    pass
```

### Module Docstrings

```python
"""Random number generation core module.

This module provides the main RandomGenerator class and supporting
utilities for generating random numbers from various distributions.

Classes:
    RandomGenerator: Main generator class with multi-distribution support.
    GeneratorConfig: Configuration data class for generator setup.

Functions:
    create_generator: Factory function for creating generators.

Examples:
    >>> from pyrng.core import RandomGenerator
    >>> gen = RandomGenerator(seed=42)
    >>> samples = gen.uniform(0, 1, size=1000)
"""
```

### Class Docstrings

```python
class NormalDistribution:
    """Normal (Gaussian) distribution implementation.
    
    This class implements the normal distribution with configurable
    mean (mu) and standard deviation (sigma) parameters.
    
    Attributes:
        mu: Mean of the distribution (location parameter).
        sigma: Standard deviation of the distribution (scale parameter).
    
    Examples:
        >>> dist = NormalDistribution(mu=0, sigma=1)
        >>> samples = dist.sample(size=1000, rng=np.random.default_rng())
    """
```

### Comments

```python
# Use comments to explain WHY, not WHAT
# Good: Explains reasoning
# Use vectorized operations for 10x performance improvement
samples = rng.normal(mu, sigma, size)

# Bad: States the obvious
# Generate normal distribution samples
samples = rng.normal(mu, sigma, size)

# Use TODO comments with context
# TODO(username): Add support for truncated normal distribution
# TODO(username): Optimize memory usage for size > 10M samples
```

### README and Documentation
- **README.md**: User-facing documentation with installation, usage, examples
- **CONTRIBUTING.md**: Guidelines for contributors
- **docs/**: Detailed documentation for complex features
- **CHANGELOG.md**: Version history and changes

## Testing Guidelines

### Test Organization

```
tests/
├── unit/                 # Unit tests (fast, isolated)
│   ├── test_distributions.py
│   ├── test_generators.py
│   └── test_validators.py
├── integration/          # Integration tests
│   ├── test_cli.py
│   └── test_workflows.py
├── fixtures/             # Shared test fixtures
│   └── conftest.py
└── data/                 # Test data files
    └── sample_config.json
```

### Test Naming

```python
# Pattern: test_<function_name>_<scenario>_<expected_result>
def test_generate_uniform_with_valid_params_returns_array():
    pass

def test_generate_uniform_with_negative_size_raises_error():
    pass

def test_load_config_with_missing_file_raises_filenotfound():
    pass
```

### Test Structure (Arrange-Act-Assert)

```python
def test_normal_distribution_sampling():
    # Arrange: Set up test data and dependencies
    mu, sigma = 0.0, 1.0
    dist = NormalDistribution(mu=mu, sigma=sigma)
    rng = np.random.default_rng(seed=42)
    size = 10000
    
    # Act: Execute the code under test
    samples = dist.sample(size=size, rng=rng)
    
    # Assert: Verify the results
    assert len(samples) == size
    assert abs(np.mean(samples) - mu) < 0.1
    assert abs(np.std(samples) - sigma) < 0.1
```

### Test Coverage Requirements
- **Minimum Coverage**: 90% overall
- **Critical Paths**: 100% coverage for core generation logic
- **Edge Cases**: Test boundary conditions, invalid inputs
- **Error Paths**: Test exception handling

### Fixtures and Parametrization

```python
import pytest

# Shared fixtures in conftest.py
@pytest.fixture
def default_rng():
    """Provide a seeded RNG for reproducible tests."""
    return np.random.default_rng(seed=42)

@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file."""
    config_file = tmp_path / "config.json"
    config_file.write_text('{"seed": 42, "distribution": "normal"}')
    return config_file

# Parametrized tests for multiple scenarios
@pytest.mark.parametrize("size,expected_len", [
    (10, 10),
    (100, 100),
    (1000, 1000),
])
def test_sample_size(size, expected_len, default_rng):
    dist = UniformDistribution(0, 1)
    samples = dist.sample(size, default_rng)
    assert len(samples) == expected_len

@pytest.mark.parametrize("invalid_size", [-1, 0, -100])
def test_invalid_sample_size_raises_error(invalid_size):
    with pytest.raises(ValidationError):
        validate_sample_size(invalid_size)
```

### Test Execution

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyrng --cov-report=html --cov-report=term

# Run specific test file
pytest tests/unit/test_distributions.py

# Run tests matching pattern
pytest -k "test_normal"

# Run with verbose output
pytest -v

# Run in parallel (with pytest-xdist)
pytest -n auto
```

## Common Patterns

### Configuration Management

```python
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any
import json

@dataclass
class Config:
    """Application configuration."""
    seed: Optional[int] = None
    distribution: str = "uniform"
    parameters: Dict[str, Any] = field(default_factory=dict)
    output_format: str = "stdout"
    verbose: bool = False
    
    @classmethod
    def from_file(cls, path: Path) -> 'Config':
        """Load configuration from JSON file."""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)
    
    @classmethod
    def from_cli_args(cls, args: argparse.Namespace) -> 'Config':
        """Create configuration from CLI arguments."""
        return cls(
            seed=args.seed,
            distribution=args.distribution,
            parameters=parse_parameters(args.params),
            output_format=args.output,
            verbose=args.verbose
        )
    
    def merge(self, other: 'Config') -> 'Config':
        """Merge with another config (other takes precedence)."""
        # Implementation details...
        pass
```

### Factory Pattern for Distributions

```python
from typing import Dict, Type
from abc import ABC, abstractmethod

class Distribution(ABC):
    """Abstract base class for probability distributions."""
    
    @abstractmethod
    def sample(self, size: int, rng: np.random.Generator) -> np.ndarray:
        """Generate samples from this distribution."""
        pass

class DistributionFactory:
    """Factory for creating distribution instances."""
    
    _registry: Dict[str, Type[Distribution]] = {}
    
    @classmethod
    def register(cls, name: str, distribution_class: Type[Distribution]) -> None:
        """Register a distribution type."""
        cls._registry[name] = distribution_class
    
    @classmethod
    def create(cls, name: str, **kwargs) -> Distribution:
        """Create a distribution instance by name."""
        if name not in cls._registry:
            raise ValueError(f"Unknown distribution: {name}")
        return cls._registry[name](**kwargs)

# Registration
DistributionFactory.register("normal", NormalDistribution)
DistributionFactory.register("uniform", UniformDistribution)

# Usage
dist = DistributionFactory.create("normal", mu=0, sigma=1)
```

### Logging Pattern

```python
import logging
from pathlib import Path

def setup_logging(verbose: bool = False, log_file: Optional[Path] = None) -> None:
    """Configure application logging."""
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    logger = logging.getLogger('pyrng')
    logger.setLevel(level)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

# Usage in modules
logger = logging.getLogger(__name__)

def some_function():
    logger.debug("Detailed debug information")
    logger.info("General information")
    logger.warning("Warning message")
    logger.error("Error occurred")
```

### Resource Management

```python
from contextlib import contextmanager
from typing import TextIO

@contextmanager
def output_writer(output_path: Optional[Path] = None):
    """Context manager for output file handling."""
    if output_path is None:
        # Write to stdout
        yield sys.stdout
    else:
        # Write to file
        file_handle = open(output_path, 'w')
        try:
            yield file_handle
        finally:
            file_handle.close()

# Usage
with output_writer(output_file) as writer:
    writer.write(f"{sample}\n")
```

### Validation Pattern

```python
from typing import Any, Callable, TypeVar

T = TypeVar('T')

def validate(
    value: T,
    *validators: Callable[[T], None]
) -> T:
    """Apply multiple validators to a value."""
    for validator in validators:
        validator(value)
    return value

# Validator functions
def positive(value: int) -> None:
    if value <= 0:
        raise ValidationError(f"Value must be positive, got {value}")

def in_range(min_val: float, max_val: float) -> Callable[[float], None]:
    def validator(value: float) -> None:
        if not min_val <= value <= max_val:
            raise ValidationError(
                f"Value {value} not in range [{min_val}, {max_val}]"
            )
    return validator

# Usage
sample_size = validate(user_input, positive, in_range(1, 1_000_000))
```

## Version Control Conventions

### Commit Messages
Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(distributions): add exponential distribution support

Implement ExponentialDistribution class with rate parameter.
Add corresponding tests and documentation.

Closes #23
```

```
fix(cli): handle missing config file gracefully

Previously crashed with FileNotFoundError. Now logs error
and uses default configuration.
```

### Branch Naming
- `main`: Stable production code
- `develop`: Development integration branch
- `feature/<name>`: New features
- `fix/<name>`: Bug fixes
- `docs/<name>`: Documentation updates

### Pull Request Guidelines
- Clear description of changes
- Reference related issues
- All tests must pass
- Code coverage should not decrease
- Follow code review checklist

## Code Review Checklist

- [ ] Code follows PEP 8 and project conventions
- [ ] All functions have type hints
- [ ] All public APIs have docstrings
- [ ] Tests are included and pass
- [ ] Code coverage is maintained or improved
- [ ] No hardcoded values (use constants or config)
- [ ] Error handling is appropriate
- [ ] Logging is used effectively
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Documentation updated if needed

## Development Workflow

1. **Setup**: Create virtual environment, install dependencies
2. **Branch**: Create feature/fix branch from `develop`
3. **Develop**: Write code following conventions
4. **Test**: Write and run tests, ensure coverage
5. **Format**: Run black and ruff to format/lint code
6. **Type Check**: Run mypy to verify type correctness
7. **Commit**: Make atomic commits with clear messages
8. **Push**: Push branch and create pull request
9. **Review**: Address review comments
10. **Merge**: Merge to develop after approval

## Performance Guidelines

- **Vectorization**: Use NumPy operations instead of Python loops
- **Memory**: Consider memory usage for large datasets, use generators when appropriate
- **Profiling**: Profile code before optimizing (use cProfile, line_profiler)
- **Caching**: Cache expensive computations when appropriate (functools.lru_cache)

## Security Considerations

- **Input Validation**: Always validate user input
- **File Operations**: Use Path objects, validate file paths
- **Code Execution**: Never use eval() or exec() on user input
- **Dependencies**: Keep dependencies updated, monitor for vulnerabilities
- **Secrets**: Never commit sensitive data (use .gitignore)
