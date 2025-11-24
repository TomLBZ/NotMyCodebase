# Changelog

All notable changes to PyRng will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-24

### Added

#### Core Features
- Random number generation from 5 probability distributions:
  - Uniform distribution with configurable min/max bounds
  - Normal (Gaussian) distribution with mean and standard deviation
  - Exponential distribution with rate parameter
  - Binomial distribution with trials and probability
  - Poisson distribution with rate parameter
- Seed-based reproducibility for deterministic generation
- Support for generating from 1 to 1,000,000+ samples

#### Output Formats
- Text output with configurable delimiters
- CSV output with optional headers
- JSON output with metadata support
- Binary output with configurable data types and endianness

#### CLI Interface
- Command-line interface with argparse
- Interactive mode for step-by-step configuration
- Comprehensive help system and usage examples
- File output and stdout support
- Verbose logging mode

#### Configuration System
- JSON-based configuration files
- Default config at `~/.pyrng/config.json`
- Config file loading and saving
- CLI arguments override config file settings
- Parameter validation with clear error messages

#### Architecture
- Modular design with clear separation of concerns
- Distribution factory pattern for extensibility
- Strategy pattern for output formatting
- Comprehensive type hints throughout
- Extensive error handling with custom exception hierarchy

### Testing
- 149 unit and integration tests
- 68% test coverage (baseline)
- Pytest-based test suite
- Fixtures for common test scenarios
- Parametrized tests for thorough validation

### Documentation
- Comprehensive README with quickstart and examples
- API documentation with docstrings (Google style)
- Architecture documentation
- Development conventions guide
- Contributing guidelines
- MIT License

### Fixed
- Binary format dtype string handling for proper encoding/decoding
- Config loader default path handling when custom path specified
- Distribution parameter clearing when switching distributions

### Technical Details
- Python 3.10+ support
- NumPy-based implementations for performance
- Pydantic models for configuration validation
- Type-checked with mypy
- Formatted with black
- Linux/Ubuntu primary target platform

[1.0.0]: https://github.com/yourusername/pyrng/releases/tag/v1.0.0
