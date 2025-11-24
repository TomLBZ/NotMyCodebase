# PyRng - Python Random Number Generator

A highly configurable command-line random number generator with support for multiple probability distributions and output formats.

## Features

- **Multiple Distributions**: Uniform, Normal, Exponential, Binomial, Poisson
- **Flexible Output**: Text, CSV, JSON, Binary formats
- **Reproducibility**: Seed-based generation for consistent results
- **Type Safety**: Comprehensive type hints and validation
- **Performance**: Leverages NumPy for efficient array operations
- **Extensibility**: Easy to add new distributions and formats

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/pyrng.git
cd pyrng

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Using pip

```bash
pip install pyrng
```

## Quick Start

### Basic Usage

Generate 10 random numbers from a uniform distribution:

```bash
pyrng uniform -n 10 --low 0 --high 1
```

Generate 1000 numbers from a normal distribution:

```bash
pyrng normal -n 1000 --mu 0 --sigma 1
```

### With Seed for Reproducibility

```bash
pyrng uniform -n 100 -s 42 --low 0 --high 10
```

### Output to File

```bash
# CSV format
pyrng normal -n 1000 --mu 0 --sigma 1 -o output.csv -f csv

# JSON format
pyrng exponential -n 500 --lambda 1.5 -o output.json -f json

# Binary format
pyrng uniform -n 10000 --low 0 --high 100 -o output.bin -f binary
```

## Usage Examples

### Uniform Distribution

```bash
# Generate 100 integers between 1 and 100
pyrng uniform -n 100 --low 1 --high 100

# Generate floats between 0 and 1
pyrng uniform -n 1000 --low 0.0 --high 1.0
```

### Normal Distribution

```bash
# Standard normal (mean=0, std=1)
pyrng normal -n 1000 --mu 0 --sigma 1

# Custom parameters
pyrng normal -n 500 --mu 100 --sigma 15
```

### Exponential Distribution

```bash
# Lambda = 1.0
pyrng exponential -n 1000 --lambda 1.0

# Lambda = 0.5
pyrng exponential -n 500 --lambda 0.5
```

### Binomial Distribution

```bash
# 10 trials, 50% probability
pyrng binomial -n 1000 --trials 10 --p 0.5

# 20 trials, 30% probability
pyrng binomial -n 500 --trials 20 --p 0.3
```

### Poisson Distribution

```bash
# Lambda (rate) = 5
pyrng poisson -n 1000 --lambda 5

# Lambda (rate) = 10
pyrng poisson -n 500 --lambda 10
```

## Command-Line Options

### Global Options

- `-h, --help`: Show help message
- `--version`: Show version number
- `-v, --verbose`: Enable verbose logging
- `-s, --seed SEED`: Set random seed for reproducibility

### Distribution-Specific Options

#### Uniform
- `-n, --count`: Number of samples (required)
- `--low`: Lower bound (default: 0.0)
- `--high`: Upper bound (default: 1.0)

#### Normal
- `-n, --count`: Number of samples (required)
- `--mu`: Mean (default: 0.0)
- `--sigma`: Standard deviation (default: 1.0)

#### Exponential
- `-n, --count`: Number of samples (required)
- `--lambda`: Rate parameter (default: 1.0)

#### Binomial
- `-n, --count`: Number of samples (required)
- `--trials`: Number of trials (default: 10)
- `--p`: Probability of success (default: 0.5)

#### Poisson
- `-n, --count`: Number of samples (required)
- `--lambda`: Rate parameter (default: 1.0)

### Output Options

- `-o, --output`: Output file path (default: stdout)
- `-f, --format`: Output format: `text`, `csv`, `json`, `binary` (default: text)

## Development

### Setup Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyrng --cov-report=html

# Run specific test categories
pytest -m unit         # Unit tests only
pytest -m integration  # Integration tests only
pytest -m statistical  # Statistical validation tests
```

### Code Quality

```bash
# Format code
black pyrng tests

# Lint code
ruff pyrng tests

# Type checking
mypy pyrng
```

## Project Structure

```
pyrng/
├── pyrng/                  # Main package
│   ├── __init__.py
│   ├── __main__.py        # Entry point
│   ├── cli/               # Command-line interface
│   ├── core/              # Core logic
│   ├── distributions/     # Distribution implementations
│   ├── config/            # Configuration management
│   ├── output/            # Output formatting
│   └── utils/             # Utility functions
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── data/             # Test data
├── docs/                  # Documentation
├── examples/              # Usage examples
├── setup.py              # Package setup
├── requirements.txt      # Production dependencies
└── README.md             # This file
```

## Requirements

- Python 3.10 or higher
- NumPy >= 1.24.0
- Pydantic >= 2.0.0

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for guidelines.

## Support

For bugs and feature requests, please open an issue on GitHub.

## Authors

PyRng Development Team

## Changelog

See CHANGELOG.md for version history.
