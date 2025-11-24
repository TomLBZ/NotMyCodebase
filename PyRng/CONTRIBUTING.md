# Contributing to PyRng

Thank you for your interest in contributing to PyRng! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

### Setting Up Development Environment

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd PyRng
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

4. **Verify installation:**
   ```bash
   pytest tests/
   pyrng --help
   ```

## Development Workflow

### Making Changes

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding conventions below

3. **Write tests** for new functionality

4. **Run tests:**
   ```bash
   pytest tests/
   ```

5. **Check code coverage:**
   ```bash
   pytest tests/ --cov=pyrng --cov-report=html
   ```

6. **Format your code:**
   ```bash
   black src/pyrng tests/
   ```

7. **Run type checking:**
   ```bash
   mypy src/pyrng
   ```

8. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

### Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and PRs when relevant

Examples:
- `Fix config merge bug when switching distributions`
- `Add support for gamma distribution`
- `Improve error messages for invalid parameters`

## Coding Conventions

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use `black` for automatic formatting (line length: 88)
- Use type hints for all function signatures
- Write docstrings for all public functions and classes (Google style)

### Naming Conventions

- **Modules**: `lowercase_with_underscores.py`
- **Classes**: `PascalCase`
- **Functions/Methods**: `snake_case`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Private members**: `_leading_underscore`

### Type Hints

Always use type hints:

```python
from typing import Optional, Dict, Any
import numpy as np

def generate_numbers(
    distribution: str,
    count: int,
    seed: Optional[int] = None,
    parameters: Optional[Dict[str, Any]] = None
) -> np.ndarray:
    """Generate random numbers with specified distribution."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def my_function(param1: int, param2: str) -> bool:
    """Brief description of the function.
    
    More detailed description if needed.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
    
    Returns:
        Description of return value.
    
    Raises:
        ValueError: If param1 is negative.
    
    Examples:
        >>> my_function(5, "test")
        True
    """
    pass
```

## Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>`
- Organize tests into unit and integration tests
- Use pytest fixtures for shared test data
- Aim for >90% code coverage

### Test Structure

```python
import pytest
from pyrng.core.generator import RandomGenerator

class TestRandomGenerator:
    """Test suite for RandomGenerator class."""
    
    def test_initialization_with_seed(self):
        """Test that generator initializes correctly with seed."""
        gen = RandomGenerator(seed=42)
        assert gen.seed == 42
    
    def test_generate_with_invalid_distribution_raises_error(self):
        """Test that unknown distribution raises DistributionError."""
        gen = RandomGenerator()
        with pytest.raises(DistributionError):
            gen.generate("unknown_dist", 100)
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_generator.py

# Run specific test
pytest tests/unit/test_generator.py::TestRandomGenerator::test_initialization_with_seed

# Run with coverage
pytest tests/ --cov=pyrng --cov-report=html

# Run verbose
pytest tests/ -v
```

## Adding New Features

### Adding a New Distribution

1. **Create distribution class** in `src/pyrng/distributions/`:
   ```python
   from pyrng.distributions.base import Distribution
   
   class GammaDistribution(Distribution):
       """Gamma distribution implementation."""
       
       def __init__(self, shape: float, scale: float = 1.0) -> None:
           """Initialize gamma distribution."""
           self.shape = shape
           self.scale = scale
           self._validate_parameters()
       
       def _validate_parameters(self) -> None:
           """Validate distribution parameters."""
           if self.shape <= 0:
               raise ValueError("shape must be positive")
           if self.scale <= 0:
               raise ValueError("scale must be positive")
       
       def sample(self, size: int, rng: np.random.Generator) -> np.ndarray:
           """Generate samples from gamma distribution."""
           return rng.gamma(self.shape, self.scale, size)
   ```

2. **Register in factory** (`src/pyrng/core/factory.py`):
   ```python
   DistributionFactory.register("gamma", GammaDistribution)
   ```

3. **Add tests** in `tests/unit/test_distributions.py`

4. **Update documentation** in README.md

### Adding a New Output Format

1. **Create formatter class** in `src/pyrng/output/formatters.py`
2. **Implement `OutputFormatter` interface**
3. **Add tests** in `tests/unit/test_output.py`
4. **Update documentation**

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions and classes
- Update examples if adding new features
- Consider adding entries to FAQ section

## Pull Request Process

1. **Ensure all tests pass** and coverage remains high
2. **Update documentation** as needed
3. **Create pull request** with clear description of changes
4. **Link related issues** in the PR description
5. **Respond to review feedback** promptly
6. **Squash commits** before merging if requested

### Pull Request Checklist

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Type hints are present
- [ ] Docstrings are complete
- [ ] Test coverage is maintained or improved
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated

## Questions or Need Help?

- Open an issue for bugs or feature requests
- Use discussions for questions and ideas
- Be specific and provide examples when asking for help

## Recognition

Contributors are recognized in:
- Git commit history
- CHANGELOG.md for significant contributions
- README.md acknowledgments section

Thank you for contributing to PyRng!
