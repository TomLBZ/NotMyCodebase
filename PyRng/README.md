# PyRng - Python Random Number Generator

A highly configurable command-line random number generator supporting multiple probability distributions and output formats.

## Features

- **Multiple Distributions**: uniform, normal, exponential, binomial, poisson
- **Multiple Output Formats**: text, csv, json, binary
- **Configuration File Support**: Save and load settings from JSON config files
- **Interactive Mode**: Dynamic configuration and generation in an interactive session
- **Reproducible Results**: Seed-based random number generation
- **Flexible Output**: Write to stdout or save to files

## Installation

```bash
# Clone the repository
cd /home/lbz/ai/AutoCodebase/.proj/PyRng

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Quick Start

### Basic Usage

Generate 100 random numbers from a uniform distribution:

```bash
pyrng uniform -n 100 --low 0 --high 10
```

Generate 1000 samples from a normal distribution and save to CSV:

```bash
pyrng normal -n 1000 --mu 0 --sigma 1 -f csv -o output.csv
```

### Interactive Mode

Start an interactive session:

```bash
pyrng --interactive
```

In interactive mode, you can:
- View current configuration
- Modify settings dynamically
- Generate numbers with updated parameters
- Save configuration to file

Example interactive session:

```
pyrng> show
Current Configuration:
  Distribution:  uniform
  Parameters:    {}
  Sample Count:  100
  Random Seed:   None
  Output Format: text
  Output File:   stdout
  Verbose:       False

pyrng> set distribution normal
Distribution set to normal

pyrng> set param.mu 10
Distribution parameter 'mu' set to 10.0

pyrng> set param.sigma 2
Distribution parameter 'sigma' set to 2.0

pyrng> set count 500
Sample count set to 500

pyrng> set seed 42
Random seed set to 42

pyrng> generate
Generating 500 samples from normal distribution...
Successfully generated 500 samples
Output written to stdout

pyrng> set output results.csv
Output file set to results.csv

pyrng> set format csv
Output format set to csv

pyrng> generate
Generating 500 samples from normal distribution...
Successfully generated 500 samples
Output written to stdout

pyrng> save
Configuration saved to /home/user/.pyrng/config.json

pyrng> exit
Goodbye!
```

## Configuration Files

PyRng supports configuration files to persist your settings.

### Config File Locations

PyRng looks for configuration files in these locations (in order):

1. Path specified with `--config` flag
2. `~/.pyrng/config.json` (user config directory)
3. `./pyrng_config.json` (current directory)

### Creating a Config File

Create a default configuration file:

```bash
pyrng --create-config
```

This creates a JSON file with default settings at `~/.pyrng/config.json`.

### Config File Format

```json
{
  "generation": {
    "count": 100,
    "seed": null
  },
  "distribution": {
    "name": "uniform",
    "parameters": {}
  },
  "output": {
    "format": "text",
    "file_path": null
  },
  "verbose": false
}
```

### Configuration Priority

Settings are applied in this order (later overrides earlier):

1. Config file defaults
2. Loaded config file values
3. Command-line arguments

Example:

```bash
# Use config file but override count and seed
pyrng --config my_config.json normal -n 500 -s 42
```

## Command-Line Options

### Global Options

```
-h, --help              Show help message
--version               Show version information
-i, --interactive       Start interactive mode
-c, --config PATH       Path to configuration file
--create-config         Create default config file and exit
-v, --verbose           Enable verbose logging
-s, --seed SEED         Random seed for reproducibility
-o, --output PATH       Output file path (default: stdout)
-f, --format FORMAT     Output format: text, csv, json, binary
```

### Distributions

#### Uniform Distribution

```bash
pyrng uniform -n COUNT [--low LOW] [--high HIGH]
```

Parameters:
- `--low`: Lower bound (inclusive, default: 0.0)
- `--high`: Upper bound (exclusive, default: 1.0)

#### Normal Distribution

```bash
pyrng normal -n COUNT [--mu MU] [--sigma SIGMA]
```

Parameters:
- `--mu`: Mean (default: 0.0)
- `--sigma`: Standard deviation (default: 1.0)

#### Exponential Distribution

```bash
pyrng exponential -n COUNT [--lambda LAMBDA]
```

Parameters:
- `--lambda`: Rate parameter (default: 1.0)

#### Binomial Distribution

```bash
pyrng binomial -n COUNT [--trials N] [--p P]
```

Parameters:
- `--trials`: Number of trials (default: 10)
- `--p`: Probability of success (default: 0.5)

#### Poisson Distribution

```bash
pyrng poisson -n COUNT [--lambda LAMBDA]
```

Parameters:
- `--lambda`: Rate parameter (default: 1.0)

## Examples

### Command-Line Examples

```bash
# Generate 1000 uniform random numbers between 0 and 100
pyrng uniform -n 1000 --low 0 --high 100

# Generate 500 normal samples with custom parameters, save as JSON
pyrng normal -n 500 --mu 10 --sigma 2 -f json -o results.json

# Generate exponential samples with fixed seed
pyrng exponential -n 200 --lambda 1.5 -s 42

# Generate binomial samples (100 trials, 30% success rate)
pyrng binomial -n 1000 --trials 100 --p 0.3 -f csv -o binomial.csv

# Use verbose mode to see detailed information
pyrng poisson -n 100 --lambda 5 -v
```

### Using Config Files

```bash
# Create a config file
pyrng --create-config

# Edit ~/.pyrng/config.json to set your preferred defaults
# Then simply run:
pyrng normal -n 1000

# Use a custom config file
pyrng --config my_settings.json exponential -n 500

# Command-line args override config
pyrng -c my_settings.json uniform -n 2000 --low 10 --high 20
```

### Interactive Mode Workflow

```bash
# Start interactive mode with initial settings from config
pyrng --interactive

# Or start with CLI settings
pyrng --interactive normal --mu 5 --sigma 1.5 -s 42

# In interactive mode:
pyrng> set count 1000
pyrng> set distribution exponential
pyrng> set param.lam 2.0
pyrng> generate
pyrng> set format csv
pyrng> set output experiment_1.csv
pyrng> generate
pyrng> save
pyrng> exit
```

## Output Formats

### Text Format (default)

One number per line:

```
0.5432
0.8765
0.1234
```

### CSV Format

CSV with header:

```
value
0.5432
0.8765
0.1234
```

### JSON Format

Pretty-printed JSON array:

```json
[
  0.5432,
  0.8765,
  0.1234
]
```

### Binary Format

Raw binary data (NumPy array format).

## Development

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=pyrng --cov-report=html

# Run specific test file
pytest tests/unit/test_config_models.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code with Black
black src/pyrng tests/

# Type checking with mypy
mypy src/pyrng

# Linting with ruff
ruff check src/pyrng tests/
```

## Project Structure

```
PyRng/
├── src/
│   └── pyrng/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli/                 # Command-line interface
│       │   ├── parser.py        # Argument parsing
│       │   ├── commands.py      # Command implementations
│       │   └── interactive.py   # Interactive mode
│       ├── config/              # Configuration management
│       │   ├── models.py        # Pydantic models
│       │   └── loader.py        # Config file I/O
│       ├── core/                # Core logic
│       │   ├── generator.py     # Main generator
│       │   ├── factory.py       # Distribution factory
│       │   └── exceptions.py    # Custom exceptions
│       ├── distributions/       # Distribution implementations
│       ├── output/              # Output formatting
│       └── utils/               # Utility functions
├── tests/
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
└── README.md
```

## License

[Add license information here]

## Contributing

[Add contributing guidelines here]

## Credits

Built with:
- Python 3.10+
- NumPy for efficient numerical operations
- Pydantic for configuration validation
- pytest for testing
